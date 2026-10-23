"""Independently authored fixed-width bit algorithms in five languages."""


def basic(ref, language):
    if ref == "5.1":
        return {
            "csharp": "int width=high-low+1; uint mask=width==32?uint.MaxValue:(1u<<width)-1u; uint bits=unchecked((uint)word), replacement=unchecked((uint)insert); uint result=(bits & ~(mask<<low)) | ((replacement & mask)<<low); return unchecked((int)result);",
            "java": "int width=high-low+1; long mask=(1L<<width)-1L; long bits=word & 0xffffffffL, replacement=insert & 0xffffffffL; long result=(bits & ~(mask<<low)) | ((replacement & mask)<<low); return (int)result;",
            "cpp": "int width=high-low+1; std::uint64_t mask=(1ULL<<width)-1ULL; std::uint64_t bits=static_cast<std::uint32_t>(word), replacement=static_cast<std::uint32_t>(insert); std::uint64_t result=(bits & ~(mask<<low)) | ((replacement & mask)<<low); if(result>=2147483648ULL)return static_cast<int>(static_cast<long long>(result)-4294967296LL); return static_cast<int>(result);",
            "javascript": "const width=high-low+1, mask=(2**width-1)>>>0; return (word & ~(mask<<low)) | ((insert & mask)<<low);",
            "python": "width = high - low + 1\nmask = (1 << width) - 1\nbits = ((word & 0xffffffff) & ~(mask << low)) | ((insert & mask) << low)\nreturn bits if bits < 0x80000000 else bits - 0x100000000",
        }[language]
    if ref == "5.6":
        return {
            "csharp": "uint difference=unchecked((uint)(first^second)); int count=0; while(difference!=0){ difference &= difference-1; ++count; } return count;",
            "java": "int difference=first^second,count=0; while(difference!=0){difference &= difference-1; ++count;} return count;",
            "cpp": "std::uint32_t difference=static_cast<std::uint32_t>(first)^static_cast<std::uint32_t>(second); int count=0; while(difference!=0){difference &= difference-1; ++count;} return count;",
            "javascript": "let difference=(first^second)>>>0,count=0; while(difference!==0){difference=(difference & (difference-1))>>>0;++count;} return count;",
            "python": "difference = (first ^ second) & 0xffffffff\ncount = 0\nwhile difference:\n    difference &= difference - 1\n    count += 1\nreturn count",
        }[language]
    if ref == "5.7":
        return {
            "csharp": "uint bits=unchecked((uint)word); uint result=((bits & 0x55555555u)<<1) | ((bits & 0xaaaaaaaau)>>1); return unchecked((int)result);",
            "java": "return ((word & 0x55555555)<<1) | ((word & 0xaaaaaaaa)>>>1);",
            "cpp": "std::uint32_t bits=static_cast<std::uint32_t>(word); std::uint32_t result=((bits & 0x55555555u)<<1) | ((bits & 0xaaaaaaaau)>>1); if(result>=2147483648u)return static_cast<int>(static_cast<long long>(result)-4294967296LL); return static_cast<int>(result);",
            "javascript": "return ((word & 0x55555555)<<1) | ((word & 0xaaaaaaaa)>>>1);",
            "python": "bits = word & 0xffffffff\nresult = ((bits & 0x55555555) << 1) | ((bits & 0xaaaaaaaa) >> 1)\nreturn result if result < 0x80000000 else result - 0x100000000",
        }[language]
    raise ValueError(ref)


def body(ref, language):
    if ref in ("5.1", "5.6", "5.7"):
        return basic(ref, language)
    if ref == "5.2":
        if language == "python":
            return '''if not 0 < number < 1:
    return "ERROR"
digits = []
for _ in range(31):
    number *= 2
    bit = number >= 1
    digits.append("1" if bit else "0")
    if bit:
        number -= 1
    if number == 0:
        return "." + "".join(digits)
return "ERROR"'''
        if language == "javascript":
            return 'if(number<=0 || number>=1)return "ERROR";const digits=[];for(let i=0;i<31;++i){number*=2;const bit=number>=1;digits.push(bit?"1":"0");if(bit)--number;if(number===0)return "."+digits.join("");}return "ERROR";'
        setup = (
            'var result=new StringBuilder(".");'
            if language == "csharp"
            else 'var result=new StringBuilder(".");'
            if language == "java"
            else 'std::string result=".";'
        )
        append = (
            "result.Append(bit?'1':'0');"
            if language == "csharp"
            else "result.append(bit?'1':'0');"
            if language == "java"
            else "result.push_back(bit?'1':'0');"
        )
        result = (
            "result.ToString()"
            if language == "csharp"
            else "result.toString()"
            if language == "java"
            else "result"
        )
        boolean = "boolean" if language == "java" else "bool"
        return f'if(number<=0 || number>=1)return "ERROR";{setup}for(int i=0;i<31;++i){{number*=2;{boolean} bit=number>=1;{append}if(bit)--number;if(number==0)return {result};}}return "ERROR";'
    if ref == "5.3":
        if language == "python":
            return """bits = word & 0xffffffff
left = zeros = best = 0
for right in range(32):
    if ((bits >> right) & 1) == 0:
        zeros += 1
    while zeros > 1:
        if ((bits >> left) & 1) == 0:
            zeros -= 1
        left += 1
    best = max(best, right - left + 1)
return best"""
        if language == "javascript":
            return "const bits=word>>>0;let left=0,zeros=0,best=0;for(let right=0;right<32;++right){if(((bits>>>right)&1)===0)++zeros;while(zeros>1){if(((bits>>>left)&1)===0)--zeros;++left;}best=Math.max(best,right-left+1);}return best;"
        setup = (
            "uint bits=unchecked((uint)word);"
            if language == "csharp"
            else "int bits=word;"
            if language == "java"
            else "std::uint32_t bits=static_cast<std::uint32_t>(word);"
        )
        shift = ">>>" if language == "java" else ">>"
        maximum = (
            "Math.Max"
            if language == "csharp"
            else "Math.max"
            if language == "java"
            else "std::max"
        )
        return f"{setup}int left=0,zeros=0,best=0;for(int right=0;right<32;++right){{if(((bits{shift}right)&1)==0)++zeros;while(zeros>1){{if(((bits{shift}left)&1)==0)--zeros;++left;}}best={maximum}(best,right-left+1);}}return best;"
    if ref == "5.4":
        if language == "python":
            return """def successor(value):
    if value == 0:
        return -1
    lowest = value & -value
    raised = value + lowest
    if raised > 2147483647:
        return -1
    return raised | (((raised ^ value) // lowest) >> 2)
larger = successor(number)
reverse = successor(2147483647 ^ number)
smaller = -1 if reverse == -1 else 2147483647 ^ reverse
return [smaller, larger]"""
        if language == "javascript":
            return "function successor(value){if(value===0)return -1;const lowest=value & -value,raised=value+lowest;if(raised>2147483647)return -1;return raised | (Math.floor((raised^value)/lowest)>>>2);}const larger=successor(number),reverse=successor(2147483647^number);return [reverse===-1?-1:(2147483647^reverse),larger];"
        typ = "long long" if language == "cpp" else "long"
        logic = f"if(value==0)return {'-1LL' if language == 'cpp' else '-1L'};{typ} lowest=value & -value,raised=value+lowest;if(raised>2147483647)return {'-1LL' if language == 'cpp' else '-1L'};return raised | (((raised^value)/lowest)>>2);"
        function = (
            f"long Successor(long value){{{logic}}}"
            if language == "csharp"
            else f"java.util.function.LongUnaryOperator successor=value -> {{{logic}}};"
            if language == "java"
            else f"auto successor=[](long long value)->long long {{{logic}}};"
        )
        call = (
            "Successor"
            if language == "csharp"
            else "successor.applyAsLong"
            if language == "java"
            else "successor"
        )
        casts = "(int)" if language != "cpp" else "static_cast<int>"
        elements = f"{casts}(smaller),{casts}(larger)"
        result = (
            "new int[]{" + elements + "}" if language != "cpp" else "{" + elements + "}"
        )
        return f"{function}{typ} larger={call}(number),reverse={call}(2147483647 ^ number),smaller=reverse==-1?-1:(2147483647 ^ reverse);return {result};"
    if ref == "5.8":
        if language == "python":
            return """first, last = x1 // 8, x2 // 8
row = y * (width // 8)
for byte in range(first, last + 1):
    start = x1 % 8 if byte == first else 0
    end = x2 % 8 if byte == last else 7
    mask = (255 >> start) & ((255 << (7 - end)) & 255)
    screen[row + byte] |= mask"""
        if language == "javascript":
            return "const first=Math.floor(x1/8),last=Math.floor(x2/8),row=y*(width/8);for(let byte=first;byte<=last;++byte){const start=byte===first?x1%8:0,end=byte===last?x2%8:7,mask=(255>>>start)&((255<<(7-end))&255);screen[row+byte]|=mask;}"
        target = "screen[row+cell]"
        assignment = (
            f"{target}=static_cast<std::uint8_t>({target}|mask);"
            if language == "cpp"
            else f"{target}=(byte)({target}|mask);"
        )
        return f"int first=x1/8,last=x2/8,row=y*(width/8);for(int cell=first;cell<=last;++cell){{int start=cell==first?x1%8:0,end=cell==last?x2%8:7,mask=(255>>start)&((255<<(7-end))&255);{assignment}}}"
    raise ValueError(ref)
