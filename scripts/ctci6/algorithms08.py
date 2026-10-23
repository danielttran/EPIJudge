"""Independent initial recursion/DP algorithms with matching five-language costs."""


def body(ref, language):
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
