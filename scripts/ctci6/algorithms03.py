"""Independent stateful stack/queue implementations, not source-repo copies."""

from textwrap import dedent


def native(ref, language):
    cs, java, cpp = language == "csharp", language == "java", language == "cpp"
    error = lambda code: (
        'throw BankError("' + code + '");'
        if cpp
        else 'throw new BankError("' + code + '");'
    )
    cls = lambda name, body: (
        ("public class " if cs else "class ")
        + name
        + " {\n"
        + body
        + ("\n};" if cpp else "\n}")
    )
    access = "public:\n" if cpp else ""
    public = "" if cpp else "public "
    boolean = "bool" if not java else "boolean"
    if ref == "3.1":
        fields = (
            "private readonly int capacity; private readonly int[] values; private readonly int[] sizes = new int[3];"
            if cs
            else "private final int capacity; private final int[] values; private final int[] sizes = new int[3];"
            if java
            else "int capacity; std::vector<int> values; std::array<int,3> sizes{};"
        )
        check = (
            ("private " if not cpp else "")
            + "void Check(int stack) { if(stack<0 || stack>=3) "
            + error("index")
            + " }"
        )
        ctor = (
            "ThreeStacks(int supplied):capacity(supplied) { if(supplied<1 || supplied>256) "
            + error("capacity")
            + " values.resize(3*supplied); }"
            if cpp
            else "public ThreeStacks(int supplied) { if(supplied<1 || supplied>256) "
            + error("capacity")
            + " capacity=supplied; values=new int[3*supplied]; }"
        )
        return cls(
            "ThreeStacks",
            fields
            + "\n"
            + check
            + "\n"
            + access
            + ctor
            + f"""
{public}void Push(int stack,int value) {{ Check(stack); if(sizes[stack]==capacity) {error("full")} values[stack*capacity+sizes[stack]]=value; ++sizes[stack]; }}
{public}int Pop(int stack) {{ Check(stack); if(sizes[stack]==0) {error("empty")} --sizes[stack]; return values[stack*capacity+sizes[stack]]; }}
{public}int Peek(int stack) {{ Check(stack); if(sizes[stack]==0) {error("empty")} return values[stack*capacity+sizes[stack]-1]; }}
{public}{boolean} IsEmpty(int stack) {{ Check(stack); return sizes[stack]==0; }}
{public}{boolean} IsFull(int stack) {{ Check(stack); return sizes[stack]==capacity; }}
""",
        )
    if ref == "3.2":
        if cpp:
            return cls(
                "MinStack",
                """struct Entry { int Value,Minimum; std::unique_ptr<Entry> Next; Entry(int value,int minimum,std::unique_ptr<Entry> next):Value(value),Minimum(minimum),Next(std::move(next)){} };
std::unique_ptr<Entry> top;
public:
MinStack() = default;
void Push(int value) { int minimum=top?std::min(value,top->Minimum):value; top=std::make_unique<Entry>(value,minimum,std::move(top)); }
int Pop() { if(!top) throw BankError("empty"); auto removed=std::move(top); int value=removed->Value; top=std::move(removed->Next); return value; }
int Peek() { if(!top) throw BankError("empty"); return top->Value; }
int GetMin() { if(!top) throw BankError("empty"); return top->Minimum; }
bool IsEmpty() { return !top; }
""",
            )
        nullable = "?" if cs else ""
        entry = (
            ("private sealed class Entry" if cs else "private static class Entry")
            + f""" {{ public int Value,Minimum; public Entry{nullable} Next;
public Entry(int value,int minimum,Entry{nullable} next) {{Value=value;Minimum=minimum;Next=next;}} }}
private Entry{nullable} top;
"""
        )
        minimum = "Math.Min" if cs else "Math.min"
        return cls(
            "MinStack",
            entry
            + f"""
public MinStack() {{}}
public void Push(int value) {{ int minimum=top==null?value:{minimum}(value,top.Minimum); top=new Entry(value,minimum,top); }}
public int Pop() {{ if(top==null) {error("empty")} int value=top.Value; top=top.Next; return value; }}
public int Peek() {{ if(top==null) {error("empty")} return top.Value; }}
public int GetMin() {{ if(top==null) {error("empty")} return top.Minimum; }}
public {boolean} IsEmpty() {{ return top==null; }}
""",
        )
    if ref == "3.3":
        fields = (
            "private readonly int capacity; private readonly List<List<int>> stacks = new();"
            if cs
            else "private final int capacity; private final ArrayList<ArrayList<Integer>> stacks = new ArrayList<>();"
            if java
            else "int capacity; std::vector<std::vector<int>> stacks;"
        )
        count = (
            "stacks.Count"
            if cs
            else "stacks.size()"
            if java
            else "static_cast<int>(stacks.size())"
        )
        row = lambda index: (
            "stacks.get(" + index + ")" if java else "stacks[" + index + "]"
        )
        size = lambda array: (
            array + (".Count" if cs else ".size()" if java else ".size()")
        )
        get = lambda array, index: (
            array + ".get(" + index + ")" if java else array + "[" + index + "]"
        )
        add = lambda array, value: (
            array
            + (".Add(" if cs else ".add(" if java else ".push_back(")
            + value
            + ");"
        )
        remove = lambda array, index: (
            array
            + (
                ".RemoveAt("
                if cs
                else ".remove("
                if java
                else ".erase(" + array + ".begin()+"
            )
            + index
            + ");"
        )
        newrow = (
            "new List<int>()"
            if cs
            else "new ArrayList<>()"
            if java
            else "std::vector<int>()"
        )
        constructor = (
            (
                "SetOfStacks(int supplied):capacity(supplied)"
                if cpp
                else "public SetOfStacks(int supplied)"
            )
            + " { if(supplied<1 || supplied>256) "
            + error("capacity")
            + ("" if cpp else " capacity=supplied;")
            + " }"
        )
        last = row("last")
        nextrow = row("i+1")
        return cls(
            "SetOfStacks",
            fields
            + "\n"
            + access
            + constructor
            + f"""
{public}void Push(int value) {{ int last={count}-1; if(last<0 || {size(last)}==capacity) {{ {add("stacks", newrow)} ++last; }} {add(last, "value")} }}
{public}int Pop() {{ if({count}==0) {error("empty")} int last={count}-1; int value={get(last, size(last) + "-1")}; {remove(last, size(last) + "-1")} if({size(last)}==0) {{ {remove("stacks", "last")} }} return value; }}
{public}int PopAt(int index) {{ if(index<0 || index>={count}) {error("index")}
int value={get(row("index"), size(row("index")) + "-1")}; {remove(row("index"), size(row("index")) + "-1")}
for(int i=index;i+1<{count};++i) {{ int bottom={get(nextrow, "0")}; {remove(nextrow, "0")} {add(row("i"), "bottom")} }}
int last={count}-1; if({size(last)}==0) {{ {remove("stacks", "last")} }} return value;
}}
{public}{boolean} IsEmpty() {{ return {count}==0; }}
""",
        )
    if ref == "3.4":
        fields = (
            "private readonly Stack<int> newest=new(), oldest=new();"
            if cs
            else "private final ArrayDeque<Integer> newest=new ArrayDeque<>(), oldest=new ArrayDeque<>();"
            if java
            else "std::vector<int> newest,oldest;"
        )
        size = lambda n: n + (".Count" if cs else ".size()")
        empty = lambda n: size(n) + "==0"
        top = lambda n: (
            n + ".Peek()" if cs else n + ".peek()" if java else n + ".back()"
        )
        push = lambda n, v: (
            n + (".Push(" if cs else ".push(" if java else ".push_back(") + v + ");"
        )
        pop = lambda n: n + ".Pop()" if cs else n + ".pop()"
        transfer = (
            push("oldest", top("newest")) + " newest.pop_back();"
            if cpp
            else push("oldest", pop("newest"))
        )
        shift = (
            ("private " if not cpp else "")
            + "void Shift() { if("
            + empty("oldest")
            + ") { while(!("
            + empty("newest")
            + ")) { "
            + transfer
            + " } } }"
        )
        remove = (
            "int value=oldest.back(); oldest.pop_back(); return value;"
            if cpp
            else "return " + pop("oldest") + ";"
        )
        return cls(
            "TwoStackQueue",
            fields
            + "\n"
            + shift
            + "\n"
            + access
            + ("TwoStackQueue() = default;" if cpp else "public TwoStackQueue() {}")
            + f"""
{public}void Add(int value) {{ {push("newest", "value")} }}
{public}int Remove() {{ Shift(); if({empty("oldest")}) {error("empty")} {remove} }}
{public}int Peek() {{ Shift(); if({empty("oldest")}) {error("empty")} return {top("oldest")}; }}
{public}int Size() {{ return {("static_cast<int>(" + size("newest") + "+" + size("oldest") + ")") if cpp else size("newest") + "+" + size("oldest")}; }}
""",
        )
    if ref == "3.5":
        spare = "IntStack spare;" if cpp else "var spare = new IntStack();"
        return (
            spare
            + """
while(!stack.IsEmpty()) {
    int value=stack.Pop();
    while(!spare.IsEmpty() && spare.Peek()>value) stack.Push(spare.Pop());
    spare.Push(value);
}
while(!spare.IsEmpty()) stack.Push(spare.Pop());
"""
        )
    if ref == "3.6":
        if cpp:
            return cls(
                "AnimalShelter",
                """struct Entry { Animal* Value; int Order; std::unique_ptr<Entry> Next; Entry(Animal* value,int order):Value(value),Order(order){} };
std::array<std::unique_ptr<Entry>,2> heads;
std::array<Entry*,2> tails{};
int order=0,count=0;
int Oldest() { if(!heads[0])return 1;if(!heads[1])return 0;return heads[0]->Order<heads[1]->Order?0:1; }
Animal* Take(int slot) { if(!heads[slot])return nullptr;auto removed=std::move(heads[slot]);Animal* value=removed->Value;heads[slot]=std::move(removed->Next);if(!heads[slot])tails[slot]=nullptr;--count;return value; }
public:
AnimalShelter() = default;
void Enqueue(Animal* animal) { int slot;if(animal->Species=="dog")slot=0;else if(animal->Species=="cat")slot=1;else throw BankError("species");auto entry=std::make_unique<Entry>(animal,order++);auto raw=entry.get();if(tails[slot])tails[slot]->Next=std::move(entry);else heads[slot]=std::move(entry);tails[slot]=raw;++count; }
Animal* DequeueAny() { return Take(Oldest()); }
Animal* DequeueDog() { return Take(0); }
Animal* DequeueCat() { return Take(1); }
Animal* Peek() { auto& entry=heads[Oldest()];return entry?entry->Value:nullptr; }
int Size() { return count; }
""",
            )
        nullable = "?" if cs else ""
        entry = (
            ("private sealed class Entry" if cs else "private static class Entry")
            + f""" {{ public Animal Value;public int Order;public Entry{nullable} Next;public Entry(Animal value,int order) {{Value=value;Order=order;}} }}
private {("readonly " if cs else "final ")}Entry{nullable}[] heads=new Entry{nullable}[2], tails=new Entry{nullable}[2];
private int order=0,count=0;
private int Oldest() {{ if(heads[0]==null)return 1;if(heads[1]==null)return 0;return heads[0]{"!" if cs else ""}.Order<heads[1]{"!" if cs else ""}.Order?0:1; }}
private Animal{nullable} Take(int slot) {{ var entry=heads[slot];if(entry==null)return null;heads[slot]=entry.Next;if(heads[slot]==null)tails[slot]=null;--count;return entry.Value; }}
"""
        )
        species = 'animal.Species=="dog"' if cs else 'animal.Species.equals("dog")'
        cat = 'animal.Species=="cat"' if cs else 'animal.Species.equals("cat")'
        peek = (
            "heads[Oldest()]?.Value"
            if cs
            else "heads[Oldest()]==null?null:heads[Oldest()].Value"
        )
        return cls(
            "AnimalShelter",
            entry
            + f"""
public AnimalShelter() {{}}
public void Enqueue(Animal animal) {{ int slot;if({species})slot=0;else if({cat})slot=1;else {error("species")} var entry=new Entry(animal,order++);if(tails[slot]==null)heads[slot]=entry;else tails[slot]{"!" if cs else ""}.Next=entry;tails[slot]=entry;++count; }}
public Animal{nullable} DequeueAny() {{ return Take(Oldest()); }}
public Animal{nullable} DequeueDog() {{ return Take(0); }}
public Animal{nullable} DequeueCat() {{ return Take(1); }}
public Animal{nullable} Peek() {{ return {peek}; }}
public int Size() {{ return count; }}
""",
        )
    raise ValueError(ref)


PYTHON = {
    "3.1": """
class ThreeStacks:
    def __init__(self, capacity: int):
        if not 1 <= capacity <= 256:
            raise BankError('capacity')
        self._capacity = capacity
        self._values = [0] * (3 * capacity)
        self._sizes = [0, 0, 0]
    def _check(self, stack: int):
        if not 0 <= stack < 3:
            raise BankError('index')
    def Push(self, stack: int, value: int):
        self._check(stack)
        if self._sizes[stack] == self._capacity:
            raise BankError('full')
        self._values[stack * self._capacity + self._sizes[stack]] = value
        self._sizes[stack] += 1
    def Pop(self, stack: int) -> int:
        self._check(stack)
        if self._sizes[stack] == 0:
            raise BankError('empty')
        self._sizes[stack] -= 1
        return self._values[stack * self._capacity + self._sizes[stack]]
    def Peek(self, stack: int) -> int:
        self._check(stack)
        if self._sizes[stack] == 0:
            raise BankError('empty')
        return self._values[stack * self._capacity + self._sizes[stack] - 1]
    def IsEmpty(self, stack: int) -> bool:
        self._check(stack)
        return self._sizes[stack] == 0
    def IsFull(self, stack: int) -> bool:
        self._check(stack)
        return self._sizes[stack] == self._capacity
""",
    "3.2": """
class MinStack:
    class _Entry:
        def __init__(self, value, minimum, next):
            self.value, self.minimum, self.next = value, minimum, next
    def __init__(self):
        self._top = None
    def Push(self, value: int):
        minimum = value if self._top is None else min(value, self._top.minimum)
        self._top = self._Entry(value, minimum, self._top)
    def Pop(self) -> int:
        if self._top is None:
            raise BankError('empty')
        value = self._top.value
        self._top = self._top.next
        return value
    def Peek(self) -> int:
        if self._top is None:
            raise BankError('empty')
        return self._top.value
    def GetMin(self) -> int:
        if self._top is None:
            raise BankError('empty')
        return self._top.minimum
    def IsEmpty(self) -> bool:
        return self._top is None
""",
    "3.3": """
class SetOfStacks:
    def __init__(self, capacity: int):
        if not 1 <= capacity <= 256:
            raise BankError('capacity')
        self._capacity, self._stacks = capacity, []
    def Push(self, value: int):
        if not self._stacks or len(self._stacks[-1]) == self._capacity:
            self._stacks.append([])
        self._stacks[-1].append(value)
    def Pop(self) -> int:
        if not self._stacks:
            raise BankError('empty')
        value = self._stacks[-1].pop()
        if not self._stacks[-1]:
            self._stacks.pop()
        return value
    def PopAt(self, index: int) -> int:
        if not 0 <= index < len(self._stacks):
            raise BankError('index')
        value = self._stacks[index].pop()
        for i in range(index, len(self._stacks) - 1):
            self._stacks[i].append(self._stacks[i + 1].pop(0))
        if not self._stacks[-1]:
            self._stacks.pop()
        return value
    def IsEmpty(self) -> bool:
        return not self._stacks
""",
    "3.4": """
class TwoStackQueue:
    def __init__(self):
        self._newest, self._oldest = [], []
    def _shift(self):
        if not self._oldest:
            while self._newest:
                self._oldest.append(self._newest.pop())
    def Add(self, value: int):
        self._newest.append(value)
    def Remove(self) -> int:
        self._shift()
        if not self._oldest:
            raise BankError('empty')
        return self._oldest.pop()
    def Peek(self) -> int:
        self._shift()
        if not self._oldest:
            raise BankError('empty')
        return self._oldest[-1]
    def Size(self) -> int:
        return len(self._newest) + len(self._oldest)
""",
    "3.5": """
spare = IntStack()
while not stack.IsEmpty():
    value = stack.Pop()
    while not spare.IsEmpty() and spare.Peek() > value:
        stack.Push(spare.Pop())
    spare.Push(value)
while not spare.IsEmpty():
    stack.Push(spare.Pop())
""",
    "3.6": """
class AnimalShelter:
    class _Entry:
        def __init__(self, value, order):
            self.value, self.order, self.next = value, order, None
    def __init__(self):
        self._heads, self._tails = [None, None], [None, None]
        self._order = self._count = 0
    def _oldest(self):
        if self._heads[0] is None:
            return 1
        if self._heads[1] is None:
            return 0
        return 0 if self._heads[0].order < self._heads[1].order else 1
    def _take(self, slot):
        entry = self._heads[slot]
        if entry is None:
            return None
        self._heads[slot] = entry.next
        if self._heads[slot] is None:
            self._tails[slot] = None
        self._count -= 1
        return entry.value
    def Enqueue(self, animal: Animal):
        if animal.Species == 'dog':
            slot = 0
        elif animal.Species == 'cat':
            slot = 1
        else:
            raise BankError('species')
        entry = self._Entry(animal, self._order)
        self._order += 1
        if self._tails[slot] is None:
            self._heads[slot] = entry
        else:
            self._tails[slot].next = entry
        self._tails[slot] = entry
        self._count += 1
    def DequeueAny(self) -> Animal | None:
        return self._take(self._oldest())
    def DequeueDog(self) -> Animal | None:
        return self._take(0)
    def DequeueCat(self) -> Animal | None:
        return self._take(1)
    def Peek(self) -> Animal | None:
        entry = self._heads[self._oldest()]
        return None if entry is None else entry.value
    def Size(self) -> int:
        return self._count
""",
}


JAVASCRIPT = {
    "3.1": """
class ThreeStacks {
    constructor(capacity) {
        if(capacity<1 || capacity>256) throw new BankError('capacity');
        this._capacity=capacity; this._values=Array(3*capacity).fill(0); this._sizes=[0,0,0];
    }
    _check(stack) { if(stack<0 || stack>=3) throw new BankError('index'); }
    Push(stack,value) { this._check(stack);if(this._sizes[stack]===this._capacity)throw new BankError('full');this._values[stack*this._capacity+this._sizes[stack]]=value;++this._sizes[stack]; }
    Pop(stack) { this._check(stack);if(!this._sizes[stack])throw new BankError('empty');--this._sizes[stack];return this._values[stack*this._capacity+this._sizes[stack]]; }
    Peek(stack) { this._check(stack);if(!this._sizes[stack])throw new BankError('empty');return this._values[stack*this._capacity+this._sizes[stack]-1]; }
    IsEmpty(stack) { this._check(stack);return this._sizes[stack]===0; }
    IsFull(stack) { this._check(stack);return this._sizes[stack]===this._capacity; }
}
""",
    "3.2": """
class MinStack {
    constructor() { this._top=null; }
    Push(value) { const minimum=this._top===null?value:Math.min(value,this._top.minimum);this._top={value,minimum,next:this._top}; }
    Pop() { if(this._top===null)throw new BankError('empty');const value=this._top.value;this._top=this._top.next;return value; }
    Peek() { if(this._top===null)throw new BankError('empty');return this._top.value; }
    GetMin() { if(this._top===null)throw new BankError('empty');return this._top.minimum; }
    IsEmpty() { return this._top===null; }
}
""",
    "3.3": """
class SetOfStacks {
    constructor(capacity) { if(capacity<1 || capacity>256)throw new BankError('capacity');this._capacity=capacity;this._stacks=[]; }
    Push(value) { if(!this._stacks.length || this._stacks.at(-1).length===this._capacity)this._stacks.push([]);this._stacks.at(-1).push(value); }
    Pop() { if(!this._stacks.length)throw new BankError('empty');const value=this._stacks.at(-1).pop();if(!this._stacks.at(-1).length)this._stacks.pop();return value; }
    PopAt(index) { if(index<0 || index>=this._stacks.length)throw new BankError('index');const value=this._stacks[index].pop();for(let i=index;i+1<this._stacks.length;++i)this._stacks[i].push(this._stacks[i+1].shift());if(!this._stacks.at(-1).length)this._stacks.pop();return value; }
    IsEmpty() { return this._stacks.length===0; }
}
""",
    "3.4": """
class TwoStackQueue {
    constructor() { this._newest=[];this._oldest=[]; }
    _shift() { if(!this._oldest.length)while(this._newest.length)this._oldest.push(this._newest.pop()); }
    Add(value) { this._newest.push(value); }
    Remove() { this._shift();if(!this._oldest.length)throw new BankError('empty');return this._oldest.pop(); }
    Peek() { this._shift();if(!this._oldest.length)throw new BankError('empty');return this._oldest.at(-1); }
    Size() { return this._newest.length+this._oldest.length; }
}
""",
    "3.5": """
const spare = new IntStack();
while(!stack.IsEmpty()) {
    const value=stack.Pop();
    while(!spare.IsEmpty() && spare.Peek()>value) stack.Push(spare.Pop());
    spare.Push(value);
}
while(!spare.IsEmpty()) stack.Push(spare.Pop());
""",
    "3.6": """
class AnimalShelter {
    constructor() { this._heads=[null,null];this._tails=[null,null];this._order=0;this._count=0; }
    _oldest() { if(this._heads[0]===null)return 1;if(this._heads[1]===null)return 0;return this._heads[0].order<this._heads[1].order?0:1; }
    _take(slot) { const entry=this._heads[slot];if(entry===null)return null;this._heads[slot]=entry.next;if(this._heads[slot]===null)this._tails[slot]=null;--this._count;return entry.value; }
    Enqueue(animal) { let slot;if(animal.Species==='dog')slot=0;else if(animal.Species==='cat')slot=1;else throw new BankError('species');const entry={value:animal,order:this._order++,next:null};if(this._tails[slot]===null)this._heads[slot]=entry;else this._tails[slot].next=entry;this._tails[slot]=entry;++this._count; }
    DequeueAny() { return this._take(this._oldest()); }
    DequeueDog() { return this._take(0); }
    DequeueCat() { return this._take(1); }
    Peek() { return this._heads[this._oldest()]?.value??null; }
    Size() { return this._count; }
}
""",
}


def body(ref, language):
    if language == "python":
        return dedent(PYTHON[ref]).strip() + "\n"
    if language == "javascript":
        return dedent(JAVASCRIPT[ref]).strip() + "\n"
    return native(ref, language)
