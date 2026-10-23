"""Independent initial recursion/DP algorithms with matching five-language costs."""


def basic(ref, language):
    if ref == "8.1":
        if language == "python":
            return """if steps < 0:
    return 0
previous, older, oldest = 1, 0, 0
for _ in range(steps):
    current = previous + older + oldest
    oldest, older, previous = older, previous, current
return previous"""
        if language == "javascript":
            return "if(steps<0)return 0;let previous=1,older=0,oldest=0;for(let i=0;i<steps;++i){const current=previous+older+oldest;oldest=older;older=previous;previous=current;}return previous;"
        return "if(steps<0)return 0;int previous=1,older=0,oldest=0;for(int i=0;i<steps;++i){int current=previous+older+oldest;oldest=older;older=previous;previous=current;}return previous;"
    if ref == "8.5":
        if language == "python":
            return """smaller, larger = min(first, second), max(first, second)
if smaller == 0:
    return 0
half = RecursiveMultiply(smaller >> 1, larger)
return half + half + (larger if smaller & 1 else 0)"""
        if language == "javascript":
            return "const smaller=Math.min(first,second),larger=Math.max(first,second);if(smaller===0)return 0;const half=RecursiveMultiply(smaller>>>1,larger);return half+half+((smaller&1)!==0?larger:0);"
        minimum = (
            "Math.Min"
            if language == "csharp"
            else "Math.min"
            if language == "java"
            else "std::min"
        )
        maximum = (
            "Math.Max"
            if language == "csharp"
            else "Math.max"
            if language == "java"
            else "std::max"
        )
        return f"int smaller={minimum}(first,second),larger={maximum}(first,second);if(smaller==0)return 0;int half=RecursiveMultiply(smaller>>1,larger);return half+half+((smaller&1)!=0?larger:0);"
    if ref == "8.11":
        if language == "python":
            return """ways = [0] * (amount + 1)
ways[0] = 1
for coin in (1, 5, 10, 25):
    for value in range(coin, amount + 1):
        ways[value] += ways[value - coin]
return ways[amount]"""
        if language == "javascript":
            return "const ways=Array(amount+1).fill(0);ways[0]=1;for(const coin of [1,5,10,25]){for(let value=coin;value<=amount;++value)ways[value]+=ways[value-coin];}return ways[amount];"
        setup = (
            "int[] ways=new int[amount+1];"
            if language != "cpp"
            else "std::vector<int> ways(amount+1);"
        )
        outer = (
            "foreach(int coin in new[]{1,5,10,25})"
            if language == "csharp"
            else "for(int coin:new int[]{1,5,10,25})"
            if language == "java"
            else "for(int coin:std::array<int,4>{1,5,10,25})"
        )
        return (
            setup
            + "ways[0]=1;"
            + outer
            + "{for(int value=coin;value<=amount;++value)ways[value]+=ways[value-coin];}return ways[amount];"
        )
    raise ValueError(ref)


def body(ref, language):
    if ref in ("8.1", "8.5", "8.11"):
        return basic(ref, language)
    if ref == "8.4":
        return {
            "python": """result = [[]]
for value in values:
    original = len(result)
    for index in range(original):
        result.append(result[index] + [value])
return result""",
            "javascript": "const result=[[]];for(const value of values){const original=result.length;for(let i=0;i<original;++i)result.push([...result[i],value]);}return result;",
            "csharp": "var result=new List<List<int>> {new()};foreach(int value in values){int original=result.Count;for(int i=0;i<original;++i){var subset=new List<int>(result[i]);subset.Add(value);result.Add(subset);}}return result;",
            "java": "List<List<Integer>> result=new ArrayList<>();result.add(new ArrayList<>());for(int value:values){int original=result.size();for(int i=0;i<original;++i){var subset=new ArrayList<>(result.get(i));subset.add(value);result.add(subset);}}return result;",
            "cpp": "std::vector<std::vector<int>> result(1);for(int value:values){auto original=result.size();for(std::size_t i=0;i<original;++i){auto subset=result[i];subset.push_back(value);result.push_back(std::move(subset));}}return result;",
        }[language]
    if language == "python":
        if ref == "8.7":
            return """chars = list(text)
result = []
def visit(depth):
    if depth == len(chars):
        result.append("".join(chars))
        return
    for index in range(depth, len(chars)):
        chars[depth], chars[index] = chars[index], chars[depth]
        visit(depth + 1)
        chars[depth], chars[index] = chars[index], chars[depth]
visit(0)
return result"""
        if ref == "8.8":
            return """counts = [0] * 26
for char in text:
    counts[ord(char) - ord('a')] += 1
buffer = [''] * len(text)
result = []
def visit(depth):
    if depth == len(buffer):
        result.append("".join(buffer))
        return
    for letter in range(26):
        if counts[letter]:
            counts[letter] -= 1
            buffer[depth] = chr(ord('a') + letter)
            visit(depth + 1)
            counts[letter] += 1
visit(0)
return result"""
        if ref == "8.9":
            return """buffer = [''] * (2 * pairs)
result = []
def visit(opened, closed):
    position = opened + closed
    if position == len(buffer):
        result.append("".join(buffer))
        return
    if opened < pairs:
        buffer[position] = '('
        visit(opened + 1, closed)
    if closed < opened:
        buffer[position] = ')'
        visit(opened, closed + 1)
visit(0, 0)
return result"""
    if language == "javascript":
        if ref == "8.7":
            return 'const chars=Array.from(text),result=[];function visit(depth){if(depth===chars.length){result.push(chars.join(""));return;}for(let i=depth;i<chars.length;++i){[chars[depth],chars[i]]=[chars[i],chars[depth]];visit(depth+1);[chars[depth],chars[i]]=[chars[i],chars[depth]];}}visit(0);return result;'
        if ref == "8.8":
            return 'const counts=Array(26).fill(0),buffer=Array(text.length),result=[];for(const char of text)++counts[char.charCodeAt(0)-97];function visit(depth){if(depth===buffer.length){result.push(buffer.join(""));return;}for(let letter=0;letter<26;++letter){if(counts[letter]>0){--counts[letter];buffer[depth]=String.fromCharCode(97+letter);visit(depth+1);++counts[letter];}}}visit(0);return result;'
        if ref == "8.9":
            return 'const buffer=Array(2*pairs),result=[];function visit(opened,closed){const position=opened+closed;if(position===buffer.length){result.push(buffer.join(""));return;}if(opened<pairs){buffer[position]="(";visit(opened+1,closed);}if(closed<opened){buffer[position]=")";visit(opened,closed+1);}}visit(0,0);return result;'
    cs, java, cpp = language == "csharp", language == "java", language == "cpp"
    result = (
        "var result=new List<string>();"
        if cs
        else "List<String> result=new ArrayList<>();"
        if java
        else "std::vector<std::string> result;"
    )
    if ref == "8.7":
        setup = (
            "char[] chars=text.ToCharArray();"
            if cs
            else "char[] chars=text.toCharArray();"
            if java
            else "std::string chars=text;"
        )
        length = (
            "chars.Length"
            if cs
            else "chars.length"
            if java
            else "static_cast<int>(chars.size())"
        )
        append = (
            "result.Add(new string(chars));"
            if cs
            else "result.add(new String(chars));"
            if java
            else "result.push_back(chars);"
        )
        swap = "char temporary=chars[depth];chars[depth]=chars[i];chars[i]=temporary;"
        restore = "temporary=chars[depth];chars[depth]=chars[i];chars[i]=temporary;"
        logic = f"if(depth=={length}){{{append}return;}}for(int i=depth;i<{length};++i){{{swap}VISIT(depth+1);{restore}}}"
        signature = "int depth"
        call = "0"
    elif ref == "8.8":
        setup = (
            "int[] counts=new int[26];foreach(char c in text)++counts[c-'a'];char[] buffer=new char[text.Length];"
            if cs
            else "int[] counts=new int[26];for(char c:text.toCharArray())++counts[c-'a'];char[] buffer=new char[text.length()];"
            if java
            else "std::array<int,26> counts{};for(char c:text)++counts[c-'a'];std::string buffer(text.size(),' ');"
        )
        length = (
            "buffer.Length"
            if cs
            else "buffer.length"
            if java
            else "static_cast<int>(buffer.size())"
        )
        append = (
            "result.Add(new string(buffer));"
            if cs
            else "result.add(new String(buffer));"
            if java
            else "result.push_back(buffer);"
        )
        character = "(char)('a'+letter)" if not cpp else "static_cast<char>('a'+letter)"
        logic = f"if(depth=={length}){{{append}return;}}for(int letter=0;letter<26;++letter){{if(counts[letter]>0){{--counts[letter];buffer[depth]={character};VISIT(depth+1);++counts[letter];}}}}"
        signature = "int depth"
        call = "0"
    elif ref == "8.9":
        setup = (
            "char[] buffer=new char[2*pairs];"
            if not cpp
            else "std::string buffer(2*pairs,' ');"
        )
        length = (
            "buffer.Length"
            if cs
            else "buffer.length"
            if java
            else "static_cast<int>(buffer.size())"
        )
        append = (
            "result.Add(new string(buffer));"
            if cs
            else "result.add(new String(buffer));"
            if java
            else "result.push_back(buffer);"
        )
        logic = f"int position=opened+closed;if(position=={length}){{{append}return;}}if(opened<pairs){{buffer[position]='(';VISIT(opened+1,closed);}}if(closed<opened){{buffer[position]=')';VISIT(opened,closed+1);}}"
        signature = "int opened,int closed"
        call = "0,0"
    else:
        raise ValueError(ref)
    logic = logic.replace("VISIT", "Visit" if not cpp else "visit")
    helper = (
        f"void Visit({signature}){{{logic}}}Visit({call});"
        if cs
        else f"class Search {{void Visit({signature}){{{logic}}}}}new Search().Visit({call});"
        if java
        else f"std::function<void({'int,int' if ref == '8.9' else 'int'})> visit=[&]({signature}){{{logic}}};visit({call});"
    )
    return setup + result + helper + "return result;"
