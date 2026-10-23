"""Original list algorithms. Identity comparisons never compare node payloads."""

from textwrap import dedent

from models02 import NODE_TYPES


def native(ref, language):
    null = "nullptr" if language == "cpp" else "null"
    node = NODE_TYPES[language]

    def field(value, key, assured=False):
        if assured and language == "csharp":
            value += "!"
        return value + ("->" if language == "cpp" else ".") + key

    def variable(name, value):
        return node + " " + name + " = " + value + ";"

    if ref == "2.1":
        seen = {
            "csharp": "var seen = new HashSet<int>();",
            "java": "var seen = new HashSet<Integer>();",
            "cpp": "std::unordered_set<int> seen;",
        }[language]
        insert = {
            "csharp": f"seen.Add({field('current', 'Value')})",
            "java": f"seen.add({field('current', 'Value')})",
            "cpp": f"seen.insert({field('current', 'Value')}).second",
        }[language]
        return f"""{seen}
{variable("previous", null)}
{variable("current", "head")}
while (current != {null}) {{
    if (!({insert})) {field("previous", "Next", True)} = {field("current", "Next")};
    else previous = current;
    current = {field("current", "Next")};
}}"""
    if ref == "2.2":
        return f"""if (k <= 0) return {null};
{variable("lead", "head")}
for (int i = 0; i < k; ++i) {{
    if (lead == {null}) return {null};
    lead = {field("lead", "Next")};
}}
{variable("follow", "head")}
while (lead != {null}) {{
    lead = {field("lead", "Next")};
    follow = {field("follow", "Next", True)};
}}
return follow;"""
    if ref == "2.3":
        return f"""if (target == {null} || {field("target", "Next")} == {null}) return false;
{variable("successor", field("target", "Next"))}
{field("target", "Value")} = {field("successor", "Value", True)};
{field("target", "Next")} = {field("successor", "Next", True)};
return true;"""
    if ref == "2.4":
        return f"""{variable("smallHead", null)}
{variable("smallTail", null)}
{variable("largeHead", null)}
{variable("largeTail", null)}
{variable("current", "head")}
while (current != {null}) {{
    {variable("next", field("current", "Next"))}
    {field("current", "Next")} = {null};
    if ({field("current", "Value")} < pivot) {{
        if (smallTail == {null}) smallHead = current;
        else {field("smallTail", "Next")} = current;
        smallTail = current;
    }} else {{
        if (largeTail == {null}) largeHead = current;
        else {field("largeTail", "Next")} = current;
        largeTail = current;
    }}
    current = next;
}}
if (smallHead == {null}) return largeHead;
{field("smallTail", "Next", True)} = largeHead;
return smallHead;"""
    if ref == "2.5":
        new = "new LinkedListNode"
        stacks = {
            "csharp": "var left = new Stack<int>(); var right = new Stack<int>();",
            "java": "var left = new ArrayDeque<Integer>(); var right = new ArrayDeque<Integer>();",
            "cpp": "std::vector<int> left, right;",
        }[language]
        push = {"csharp": "Push", "java": "push", "cpp": "push_back"}[language]
        more = {
            "csharp": "left.Count > 0 || right.Count > 0",
            "java": "!left.isEmpty() || !right.isEmpty()",
            "cpp": "!left.empty() || !right.empty()",
        }[language]
        consume = {
            "csharp": "if (left.Count > 0) total += left.Pop(); if (right.Count > 0) total += right.Pop();",
            "java": "if (!left.isEmpty()) total += left.pop(); if (!right.isEmpty()) total += right.pop();",
            "cpp": "if (!left.empty()) { total += left.back(); left.pop_back(); } if (!right.empty()) { total += right.back(); right.pop_back(); }",
        }[language]
        dummy = (
            "LinkedListNode dummy(0); LinkedListNode* tail = &dummy;"
            if language == "cpp"
            else "var dummy = new LinkedListNode(0); " + variable("tail", "dummy")
        )
        dummy_next = "dummy.Next"
        return f"""if (mostSignificantFirst) {{
    {stacks}
    for ({variable("scan", "first")[:-1]}; scan != {null}; scan = {field("scan", "Next")}) left.{push}({field("scan", "Value")});
    for ({variable("scan", "second")[:-1]}; scan != {null}; scan = {field("scan", "Next")}) right.{push}({field("scan", "Value")});
    {variable("result", null)}
    int forwardCarry = 0;
    while ({more} || forwardCarry != 0) {{
        int total = forwardCarry;
        {consume}
        result = {new}(total % 10, result);
        forwardCarry = total / 10;
    }}
    return result;
}}
{dummy}
{variable("p", "first")}
{variable("q", "second")}
int carry = 0;
while (p != {null} || q != {null} || carry != 0) {{
    int total = carry;
    if (p != {null}) {{ total += {field("p", "Value")}; p = {field("p", "Next")}; }}
    if (q != {null}) {{ total += {field("q", "Value")}; q = {field("q", "Next")}; }}
    {field("tail", "Next", True)} = {new}(total % 10);
    tail = {field("tail", "Next", True)};
    carry = total / 10;
}}
return {dummy_next};"""
    if ref == "2.6":
        array = {
            "csharp": "var values = new List<int>();",
            "java": "var values = new ArrayList<Integer>();",
            "cpp": "std::vector<int> values;",
        }[language]
        append = {"csharp": "Add", "java": "add", "cpp": "push_back"}[language]
        length = {
            "csharp": "values.Count",
            "java": "values.size()",
            "cpp": "static_cast<int>(values.size())",
        }[language]
        lhs, rhs = (
            ("values.get(i)", "values.get(n-1-i)")
            if language == "java"
            else ("values[i]", "values[n-1-i]")
        )
        # Java Integer references must be unboxed before value comparison.
        if language == "java":
            lhs, rhs = lhs + ".intValue()", rhs + ".intValue()"
        return f"""{array}
for ({variable("p", "head")[:-1]}; p != {null}; p = {field("p", "Next")}) values.{append}({field("p", "Value")});
int n = {length};
for (int i = 0; i < n / 2; ++i) if ({lhs} != {rhs}) return false;
return true;"""
    if ref == "2.7":
        return f"""{variable("p", "first")}
{variable("q", "second")}
while (p != q) {{
    p = p == {null} ? second : {field("p", "Next")};
    q = q == {null} ? first : {field("q", "Next")};
}}
return p;"""
    if ref == "2.8":
        return f"""{variable("slow", "head")}
{variable("fast", "head")}
while (fast != {null} && {field("fast", "Next")} != {null}) {{
    slow = {field("slow", "Next", True)};
    fast = {field(field("fast", "Next", True), "Next", True)};
    if (slow == fast) break;
}}
if (fast == {null} || {field("fast", "Next")} == {null}) return {null};
slow = head;
while (slow != fast) {{
    slow = {field("slow", "Next", True)};
    fast = {field("fast", "Next", True)};
}}
return slow;"""
    raise ValueError(ref)


PYTHON = {
    "2.1": """
seen = set()
previous, current = None, head
while current is not None:
    if current.Value in seen:
        previous.Next = current.Next
    else:
        seen.add(current.Value)
        previous = current
    current = current.Next
""",
    "2.2": """
if k <= 0:
    return None
lead = head
for _ in range(k):
    if lead is None:
        return None
    lead = lead.Next
follow = head
while lead is not None:
    lead, follow = lead.Next, follow.Next
return follow
""",
    "2.3": """
if target is None or target.Next is None:
    return False
successor = target.Next
target.Value, target.Next = successor.Value, successor.Next
return True
""",
    "2.4": """
small_head = small_tail = large_head = large_tail = None
current = head
while current is not None:
    next_node = current.Next
    current.Next = None
    if current.Value < pivot:
        if small_tail is None:
            small_head = current
        else:
            small_tail.Next = current
        small_tail = current
    else:
        if large_tail is None:
            large_head = current
        else:
            large_tail.Next = current
        large_tail = current
    current = next_node
if small_head is None:
    return large_head
small_tail.Next = large_head
return small_head
""",
    "2.5": """
if mostSignificantFirst:
    left, right = [], []
    current = first
    while current is not None:
        left.append(current.Value)
        current = current.Next
    current = second
    while current is not None:
        right.append(current.Value)
        current = current.Next
    result, carry = None, 0
    while left or right or carry:
        total = carry + (left.pop() if left else 0) + (right.pop() if right else 0)
        result = LinkedListNode(total % 10, result)
        carry = total // 10
    return result
dummy = LinkedListNode(0)
tail = dummy
p, q, carry = first, second, 0
while p is not None or q is not None or carry:
    total = carry
    if p is not None:
        total += p.Value
        p = p.Next
    if q is not None:
        total += q.Value
        q = q.Next
    tail.Next = LinkedListNode(total % 10)
    tail = tail.Next
    carry = total // 10
return dummy.Next
""",
    "2.6": """
values = []
current = head
while current is not None:
    values.append(current.Value)
    current = current.Next
for i in range(len(values) // 2):
    if values[i] != values[len(values) - 1 - i]:
        return False
return True
""",
    "2.7": """
p, q = first, second
while p is not q:
    p = second if p is None else p.Next
    q = first if q is None else q.Next
return p
""",
    "2.8": """
slow = fast = head
while fast is not None and fast.Next is not None:
    slow, fast = slow.Next, fast.Next.Next
    if slow is fast:
        break
if fast is None or fast.Next is None:
    return None
slow = head
while slow is not fast:
    slow, fast = slow.Next, fast.Next
return slow
""",
}

JAVASCRIPT = {
    "2.1": """
const seen = new Set();
let previous = null, current = head;
while (current !== null) {
    if (seen.has(current.Value)) previous.Next = current.Next;
    else { seen.add(current.Value); previous = current; }
    current = current.Next;
}
""",
    "2.2": """
if (k <= 0) return null;
let lead = head;
for (let i = 0; i < k; ++i) {
    if (lead === null) return null;
    lead = lead.Next;
}
let follow = head;
while (lead !== null) { lead = lead.Next; follow = follow.Next; }
return follow;
""",
    "2.3": """
if (target === null || target.Next === null) return false;
const successor = target.Next;
target.Value = successor.Value;
target.Next = successor.Next;
return true;
""",
    "2.4": """
let smallHead = null, smallTail = null, largeHead = null, largeTail = null;
let current = head;
while (current !== null) {
    const next = current.Next;
    current.Next = null;
    if (current.Value < pivot) {
        if (smallTail === null) smallHead = current;
        else smallTail.Next = current;
        smallTail = current;
    } else {
        if (largeTail === null) largeHead = current;
        else largeTail.Next = current;
        largeTail = current;
    }
    current = next;
}
if (smallHead === null) return largeHead;
smallTail.Next = largeHead;
return smallHead;
""",
    "2.5": """
if (mostSignificantFirst) {
    const left = [], right = [];
    for (let p = first; p !== null; p = p.Next) left.push(p.Value);
    for (let p = second; p !== null; p = p.Next) right.push(p.Value);
    let result = null, carry = 0;
    while (left.length || right.length || carry) {
        const total = carry + (left.length ? left.pop() : 0) + (right.length ? right.pop() : 0);
        result = new LinkedListNode(total % 10, result);
        carry = Math.floor(total / 10);
    }
    return result;
}
const dummy = new LinkedListNode(0);
let tail = dummy, p = first, q = second, carry = 0;
while (p !== null || q !== null || carry) {
    let total = carry;
    if (p !== null) { total += p.Value; p = p.Next; }
    if (q !== null) { total += q.Value; q = q.Next; }
    tail.Next = new LinkedListNode(total % 10);
    tail = tail.Next;
    carry = Math.floor(total / 10);
}
return dummy.Next;
""",
    "2.6": """
const values = [];
for (let p = head; p !== null; p = p.Next) values.push(p.Value);
for (let i = 0; i < Math.floor(values.length / 2); ++i) {
    if (values[i] !== values[values.length - 1 - i]) return false;
}
return true;
""",
    "2.7": """
let p = first, q = second;
while (p !== q) {
    p = p === null ? second : p.Next;
    q = q === null ? first : q.Next;
}
return p;
""",
    "2.8": """
let slow = head, fast = head;
while (fast !== null && fast.Next !== null) {
    slow = slow.Next;
    fast = fast.Next.Next;
    if (slow === fast) break;
}
if (fast === null || fast.Next === null) return null;
slow = head;
while (slow !== fast) { slow = slow.Next; fast = fast.Next; }
return slow;
""",
}


def body(ref, language):
    if language == "python":
        return dedent(PYTHON[ref]).strip()
    if language == "javascript":
        return dedent(JAVASCRIPT[ref]).strip()
    return native(ref, language)
