"""Independent moderate-task algorithms, not public repository code copies."""

def body(ref, language):
    if ref=='16.5':
        if language=='python':return 'count = 0\nwhile n:\n    n //= 5\n    count += n\nreturn count'
        if language=='javascript':return 'let count=0;while(n!==0){n=Math.floor(n/5);count+=n;}return count;'
        return 'int count=0;while(n!=0){n/=5;count+=n;}return count;'
    if ref=='16.7':
        if language=='python':return '''negative_first = (first >> 31) & 1
negative_second = (second >> 31) & 1
negative_difference = ((first - second) & 0xffffffff) >> 31
different = negative_first ^ negative_second
choose_first = different * (negative_first ^ 1) + (different ^ 1) * (negative_difference ^ 1)
mask = -choose_first
return (first & mask) | (second & ~mask)'''
        if language=='javascript':return 'const negativeFirst=first>>>31,negativeSecond=second>>>31,negativeDifference=(first-second)>>>31,different=negativeFirst^negativeSecond,chooseFirst=different*(negativeFirst^1)+(different^1)*(negativeDifference^1),mask=-chooseFirst;return (first&mask)|(second&~mask);'
        if language=='cpp':return 'auto a=static_cast<std::uint32_t>(first),b=static_cast<std::uint32_t>(second);int negativeFirst=a>>31,negativeSecond=b>>31,negativeDifference=(a-b)>>31,different=negativeFirst^negativeSecond,chooseFirst=different*(negativeFirst^1)+(different^1)*(negativeDifference^1);return first*chooseFirst+second*(chooseFirst^1);'
        signs = 'int negativeFirst=(int)((uint)first>>31),negativeSecond=(int)((uint)second>>31),negativeDifference=(int)(unchecked((uint)first-(uint)second)>>31);' if language=='csharp' else 'int negativeFirst=first>>>31,negativeSecond=second>>>31,negativeDifference=(first-second)>>>31;'
        return signs+'int different=negativeFirst^negativeSecond,chooseFirst=different*(negativeFirst^1)+(different^1)*(negativeDifference^1),mask=-chooseFirst;return (first&mask)|(second&~mask);'
    if ref=='16.11':
        if language=='python':return 'if shorter == longer:\n    return [planks * shorter]\nreturn [planks * shorter + count * (longer - shorter) for count in range(planks + 1)]'
        if language=='javascript':return 'if(shorter===longer)return [planks*shorter];return Array.from({length:planks+1},(_,count)=>planks*shorter+count*(longer-shorter));'
        if language=='cpp':return 'if(shorter==longer)return {planks*shorter};std::vector<int> result;result.reserve(planks+1);for(int count=0;count<=planks;++count)result.push_back(planks*shorter+count*(longer-shorter));return result;'
        singleton = '[planks*shorter]' if language=='csharp' else 'new int[]{planks*shorter}'
        return f'if(shorter==longer)return {singleton};int[] result=new int[planks+1];for(int count=0;count<=planks;++count)result[count]=planks*shorter+count*(longer-shorter);return result;'
    if ref=='16.15':
        if language=='python':return '''remaining = [0] * 4
hits = 0
for index in range(4):
    if guess[index] == secret[index]:
        hits += 1
    else:
        remaining['RGBY'.index(secret[index])] += 1
pseudo_hits = 0
for index in range(4):
    if guess[index] == secret[index]:
        continue
    color = 'RGBY'.index(guess[index])
    if remaining[color]:
        remaining[color] -= 1
        pseudo_hits += 1
return [hits, pseudo_hits]'''
        if language=='javascript':return 'const remaining=Array(4).fill(0);let hits=0,pseudoHits=0;for(let i=0;i<4;++i){if(guess[i]===secret[i])++hits;else ++remaining["RGBY".indexOf(secret[i])];}for(let i=0;i<4;++i){if(guess[i]===secret[i])continue;const color="RGBY".indexOf(guess[i]);if(remaining[color]>0){--remaining[color];++pseudoHits;}}return [hits,pseudoHits];'
        arrays = 'int[] remaining=new int[4];' if language!='cpp' else 'int remaining[4]={};'
        char = lambda text,index: f'{text}.charAt({index})' if language=='java' else f'{text}[{index}]'
        color = lambda expr: '"RGBY".IndexOf('+expr+')' if language=='csharp' else '"RGBY".indexOf('+expr+')' if language=='java' else 'static_cast<int>(std::string("RGBY").find('+expr+'))'
        result = '[hits,pseudoHits]' if language=='csharp' else 'new int[]{hits,pseudoHits}' if language=='java' else '{hits,pseudoHits}'
        return f'{arrays}int hits=0,pseudoHits=0;for(int i=0;i<4;++i){{if({char("guess","i")}=={char("secret","i")})++hits;else ++remaining[{color(char("secret","i"))}];}}for(int i=0;i<4;++i){{if({char("guess","i")}=={char("secret","i")})continue;int color={color(char("guess","i"))};if(remaining[color]>0){{--remaining[color];++pseudoHits;}}}}return {result};'
    if ref=='16.16':
        if language=='python':return '''if not values:
    return [-1, -1]
right = -1
maximum = values[0]
for index, value in enumerate(values):
    if value < maximum:
        right = index
    maximum = max(maximum, value)
if right == -1:
    return [-1, -1]
left = -1
minimum = values[-1]
for index in range(len(values) - 1, -1, -1):
    if values[index] > minimum:
        left = index
    minimum = min(minimum, values[index])
return [left, right]'''
        if language=='javascript':return 'if(values.length===0)return [-1,-1];let right=-1,maximum=values[0];for(let i=0;i<values.length;++i){if(values[i]<maximum)right=i;maximum=Math.max(maximum,values[i]);}if(right===-1)return [-1,-1];let left=-1,minimum=values[values.length-1];for(let i=values.length-1;i>=0;--i){if(values[i]>minimum)left=i;minimum=Math.min(minimum,values[i]);}return [left,right];'
        size='values.Length' if language=='csharp' else 'values.length' if language=='java' else 'static_cast<int>(values.size())'
        make = lambda a,b: '['+a+','+b+']' if language=='csharp' else 'new int[]{'+a+','+b+'}' if language=='java' else '{'+a+','+b+'}'
        maximum='Math.Max' if language=='csharp' else 'Math.max' if language=='java' else 'std::max'
        minimum='Math.Min' if language=='csharp' else 'Math.min' if language=='java' else 'std::min'
        return f'int n={size};if(n==0)return {make("-1","-1")};int right=-1,maximum=values[0];for(int i=0;i<n;++i){{if(values[i]<maximum)right=i;maximum={maximum}(maximum,values[i]);}}if(right==-1)return {make("-1","-1")};int left=-1,minimum=values[n-1];for(int i=n-1;i>=0;--i){{if(values[i]>minimum)left=i;minimum={minimum}(minimum,values[i]);}}return {make("left","right")};'
    if ref=='16.17':
        if language=='python':return 'running = 0\nbest = 0\nfor value in values:\n    running = max(0, running + value)\n    best = max(best, running)\nreturn best'
        if language=='javascript':return 'let running=0,best=0;for(const value of values){running=Math.max(0,running+value);best=Math.max(best,running);}return best;'
        maximum='Math.Max' if language=='csharp' else 'Math.max' if language=='java' else 'std::max'
        loop='foreach(int value in values)' if language=='csharp' else 'for(int value:values)'
        return f'int running=0,best=0;{loop}{{running={maximum}(0,running+value);best={maximum}(best,running);}}return best;'
    raise ValueError(ref)
