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

_previous_body=body

def body(ref,language):
    if ref not in ('16.1','16.4','16.10','16.19'):
        return _previous_body(ref,language)
    if ref=='16.1':
        if language=='python':return 'first ^= second\nsecond ^= first\nfirst ^= second\nreturn [first, second]'
        pair='[first,second]' if language in ('csharp','javascript') else 'new int[]{first,second}' if language=='java' else '{first,second}'
        return 'first^=second;second^=first;first^=second;return '+pair+';'
    if ref=='16.4':
        if language=='python':return '''n = len(board)
if n == 0:
    return 0
for index in range(n):
    row_player = board[index][0]
    column_player = board[0][index]
    if row_player and all(board[index][j] == row_player for j in range(n)):
        return row_player
    if column_player and all(board[j][index] == column_player for j in range(n)):
        return column_player
main = board[0][0]
other = board[0][n - 1]
if main and all(board[i][i] == main for i in range(n)):
    return main
if other and all(board[i][n - 1 - i] == other for i in range(n)):
    return other
return 0'''
        if language=='javascript':return 'const n=board.length;if(n===0)return 0;for(let i=0;i<n;++i){let row=board[i][0],column=board[0][i];for(let j=0;j<n;++j){if(board[i][j]!==row)row=0;if(board[j][i]!==column)column=0;}if(row)return row;if(column)return column;}let main=board[0][0],other=board[0][n-1];for(let i=0;i<n;++i){if(board[i][i]!==main)main=0;if(board[i][n-1-i]!==other)other=0;}if(main)return main;return other;'
        size='board.Length' if language=='csharp' else 'board.length' if language=='java' else 'static_cast<int>(board.size())'
        return f'int n={size};if(n==0)return 0;for(int i=0;i<n;++i){{int row=board[i][0],column=board[0][i];for(int j=0;j<n;++j){{if(board[i][j]!=row)row=0;if(board[j][i]!=column)column=0;}}if(row!=0)return row;if(column!=0)return column;}}int main=board[0][0],other=board[0][n-1];for(int i=0;i<n;++i){{if(board[i][i]!=main)main=0;if(board[i][n-1-i]!=other)other=0;}}if(main!=0)return main;return other;'
    if ref=='16.10':
        if language=='python':return '''changes = [0] * 102
for birth, death in people:
    changes[birth - 1900] += 1
    changes[death - 1900 + 1] -= 1
alive = 0
best = 0
answer = 1900
for offset in range(101):
    alive += changes[offset]
    if alive > best:
        best = alive
        answer = 1900 + offset
return answer'''
        if language=='javascript':return 'const changes=Array(102).fill(0);for(const [birth,death] of people){++changes[birth-1900];--changes[death-1900+1];}let alive=0,best=0,answer=1900;for(let offset=0;offset<101;++offset){alive+=changes[offset];if(alive>best){best=alive;answer=1900+offset;}}return answer;'
        table='int[] changes=new int[102];' if language!='cpp' else 'int changes[102]={};'
        loop='foreach(var person in people)' if language=='csharp' else 'for(int[] person:people)' if language=='java' else 'for(const auto& person:people)'
        return table+loop+'{++changes[person[0]-1900];--changes[person[1]-1900+1];}int alive=0,best=0,answer=1900;for(int offset=0;offset<101;++offset){alive+=changes[offset];if(alive>best){best=alive;answer=1900+offset;}}return answer;'
    if language=='python':return '''rows = len(land)
columns = len(land[0]) if rows else 0
seen = [[False] * columns for _ in range(rows)]
sizes = []
for row in range(rows):
    for column in range(columns):
        if land[row][column] != 0 or seen[row][column]:
            continue
        seen[row][column] = True
        work = [(row, column)]
        size = 0
        while work:
            r, c = work.pop()
            size += 1
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < columns and land[nr][nc] == 0 and not seen[nr][nc]:
                        seen[nr][nc] = True
                        work.append((nr, nc))
        sizes.append(size)
sizes.sort()
return sizes'''
    if language=='javascript':return 'const rows=land.length,columns=rows?land[0].length:0,seen=Array.from({length:rows},()=>Array(columns).fill(false)),sizes=[];for(let row=0;row<rows;++row){for(let column=0;column<columns;++column){if(land[row][column]!==0||seen[row][column])continue;seen[row][column]=true;const work=[[row,column]];let size=0;while(work.length){const [r,c]=work.pop();++size;for(let dr=-1;dr<=1;++dr){for(let dc=-1;dc<=1;++dc){if(dr===0&&dc===0)continue;const nr=r+dr,nc=c+dc;if(nr>=0&&nr<rows&&nc>=0&&nc<columns&&land[nr][nc]===0&&!seen[nr][nc]){seen[nr][nc]=true;work.push([nr,nc]);}}}}sizes.push(size);}}sizes.sort((a,b)=>a-b);return sizes;'
    rows='land.Length' if language=='csharp' else 'land.length' if language=='java' else 'static_cast<int>(land.size())'
    cols='land[0].Length' if language=='csharp' else 'land[0].length' if language=='java' else 'static_cast<int>(land[0].size())'
    setup='bool[,] seen=new bool[rows,columns];var sizes=new List<int>();' if language=='csharp' else 'boolean[][] seen=new boolean[rows][columns];List<Integer> sizes=new ArrayList<>();' if language=='java' else 'std::vector<std::vector<bool>> seen(rows,std::vector<bool>(columns));std::vector<int> sizes;'
    at=lambda r,c:f'seen[{r},{c}]' if language=='csharp' else f'seen[{r}][{c}]'
    work='var work=new Stack<(int,int)>();work.Push((row,column));' if language=='csharp' else 'Deque<int[]> work=new ArrayDeque<>();work.push(new int[]{row,column});' if language=='java' else 'std::vector<std::pair<int,int>> work{{row,column}};'
    count='work.Count>0' if language=='csharp' else '!work.isEmpty()' if language=='java' else '!work.empty()'
    pop='var (r,c)=work.Pop();' if language=='csharp' else 'var cell=work.pop();int r=cell[0],c=cell[1];' if language=='java' else 'auto [r,c]=work.back();work.pop_back();'
    push='work.Push((nr,nc));' if language=='csharp' else 'work.push(new int[]{nr,nc});' if language=='java' else 'work.push_back({nr,nc});'
    add='sizes.Add(size);' if language=='csharp' else 'sizes.add(size);' if language=='java' else 'sizes.push_back(size);'
    finish='sizes.Sort();return sizes.ToArray();' if language=='csharp' else 'Collections.sort(sizes);int[] result=new int[sizes.size()];for(int i=0;i<result.length;++i)result[i]=sizes.get(i);return result;' if language=='java' else 'std::sort(sizes.begin(),sizes.end());return sizes;'
    return f'int rows={rows},columns=rows==0?0:{cols};{setup}for(int row=0;row<rows;++row){{for(int column=0;column<columns;++column){{if(land[row][column]!=0||{at("row","column")})continue;{at("row","column")}=true;{work}int size=0;while({count}){{{pop}++size;for(int dr=-1;dr<=1;++dr){{for(int dc=-1;dc<=1;++dc){{if(dr==0&&dc==0)continue;int nr=r+dr,nc=c+dc;if(nr>=0&&nr<rows&&nc>=0&&nc<columns&&land[nr][nc]==0&&!{at("nr","nc")}){{{at("nr","nc")}=true;{push}}}}}}}}}{add}}}}}{finish}'

_previous_batch_body=body

def body(ref,language):
    if ref=='16.2':
        if language=='python':return '''counts = {}
for word in book:
    key = word.lower()
    counts[key] = counts.get(key, 0) + 1
return [counts.get(word.lower(), 0) for word in queries]'''
        if language=='javascript':return 'const counts=new Map();for(const word of book){const key=word.toLowerCase();counts.set(key,(counts.get(key)||0)+1);}return queries.map(word=>counts.get(word.toLowerCase())||0);'
        if language=='csharp':return 'var counts=new Dictionary<string,int>(StringComparer.Ordinal);foreach(string word in book){string key=word.ToLowerInvariant();counts.TryGetValue(key,out int count);counts[key]=count+1;}int[] result=new int[queries.Length];for(int i=0;i<queries.Length;++i){counts.TryGetValue(queries[i].ToLowerInvariant(),out int count);result[i]=count;}return result;'
        if language=='java':return 'Map<String,Integer> counts=new HashMap<>();for(String word:book){String key=word.toLowerCase(Locale.ROOT);counts.put(key,counts.getOrDefault(key,0)+1);}int[] result=new int[queries.length];for(int i=0;i<queries.length;++i)result[i]=counts.getOrDefault(queries[i].toLowerCase(Locale.ROOT),0);return result;'
        return 'std::unordered_map<std::string,int> counts;for(auto word:book){for(char& c:word)if(c>=\'A\'&&c<=\'Z\')c=static_cast<char>(c-\'A\'+\'a\');++counts[word];}std::vector<int> result;result.reserve(queries.size());for(auto word:queries){for(char& c:word)if(c>=\'A\'&&c<=\'Z\')c=static_cast<char>(c-\'A\'+\'a\');auto found=counts.find(word);result.push_back(found==counts.end()?0:found->second);}return result;'
    if ref=='16.6':
        if language=='python':return '''if not first or not second:
    return -1
a, b = sorted(first), sorted(second)
i = j = 0
best = 4294967295
while i < len(a) and j < len(b):
    difference = a[i] - b[j]
    best = min(best, abs(difference))
    if difference == 0:
        return 0
    if difference < 0:
        i += 1
    else:
        j += 1
return best'''
        if language=='javascript':return 'if(!first.length||!second.length)return -1;const a=first.slice().sort((x,y)=>x-y),b=second.slice().sort((x,y)=>x-y);let i=0,j=0,best=4294967295;while(i<a.length&&j<b.length){const difference=a[i]-b[j];best=Math.min(best,Math.abs(difference));if(difference===0)return 0;if(difference<0)++i;else ++j;}return best;'
        if language=='cpp':return 'if(first.empty()||second.empty())return -1;auto a=first,b=second;std::sort(a.begin(),a.end());std::sort(b.begin(),b.end());size_t i=0,j=0;long long best=4294967295LL;while(i<a.size()&&j<b.size()){long long difference=static_cast<long long>(a[i])-b[j];best=std::min(best,difference<0?-difference:difference);if(difference==0)return 0;if(difference<0)++i;else ++j;}return best;'
        size='Length' if language=='csharp' else 'length';clone='(int[])first.Clone(),b=(int[])second.Clone()' if language=='csharp' else 'first.clone(),b=second.clone()';sort='Array.Sort(a);Array.Sort(b);' if language=='csharp' else 'Arrays.sort(a);Arrays.sort(b);';minimum='Math.Min' if language=='csharp' else 'Math.min';absolute='Math.Abs' if language=='csharp' else 'Math.abs'
        return f'if(first.{size}==0||second.{size}==0)return -1;int[] a={clone};{sort}int i=0,j=0;long best=4294967295L;while(i<a.{size}&&j<b.{size}){{long difference=(long)a[i]-b[j];best={minimum}(best,{absolute}(difference));if(difference==0)return 0;if(difference<0)++i;else ++j;}}return best;'
    if ref=='16.21':
        if language=='python':return '''difference = sum(first) - sum(second)
if difference % 2:
    return []
half = difference // 2
contents = set(second)
for value in first:
    required = value - half
    if required in contents:
        return [value, required]
return []'''
        if language=='javascript':return 'let difference=0;for(const value of first)difference+=value;for(const value of second)difference-=value;if(difference%2!==0)return [];const half=difference/2,contents=new Set(second);for(const value of first){const required=value-half;if(contents.has(required))return [value,required];}return [];'
        if language=='cpp':return 'long long difference=0;for(int value:first)difference+=value;for(int value:second)difference-=value;if(difference%2!=0)return {};long long half=difference/2;std::unordered_set<int> contents(second.begin(),second.end());for(int value:first){long long required=static_cast<long long>(value)-half;if(required>=-2147483648LL&&required<=2147483647LL&&contents.count(static_cast<int>(required)))return {value,static_cast<int>(required)};}return {};'
        loop='foreach(int value in ' if language=='csharp' else 'for(int value:';contains='contents.Contains((int)required)' if language=='csharp' else 'contents.contains((int)required)';sets='var contents=new HashSet<int>(second);' if language=='csharp' else 'Set<Integer> contents=new HashSet<>();for(int value:second)contents.add(value);';pair='return [value,(int)required];' if language=='csharp' else 'return new int[]{value,(int)required};';empty='return [];' if language=='csharp' else 'return new int[0];'
        return f'long difference=0;{loop}first)difference+=value;{loop}second)difference-=value;if(difference%2!=0){{{empty}}}long half=difference/2;{sets}{loop}first){{long required=(long)value-half;if(required>=-2147483648L&&required<=2147483647L&&{contains}){{{pair}}}}}{empty}'
    if ref=='16.24':
        if language=='python':return '''ordered = sorted(values)
left, right = 0, len(ordered) - 1
result = []
while left < right:
    total = ordered[left] + ordered[right]
    if total == target:
        result.append([ordered[left], ordered[right]])
        left += 1
        right -= 1
    elif total < target:
        left += 1
    else:
        right -= 1
return result'''
        if language=='javascript':return 'const ordered=values.slice().sort((a,b)=>a-b),result=[];let left=0,right=ordered.length-1;while(left<right){const total=ordered[left]+ordered[right];if(total===target){result.push([ordered[left],ordered[right]]);++left;--right;}else if(total<target)++left;else --right;}return result;'
        if language=='cpp':return 'auto ordered=values;std::sort(ordered.begin(),ordered.end());std::vector<std::vector<int>> result;int left=0,right=static_cast<int>(ordered.size())-1;while(left<right){long long total=static_cast<long long>(ordered[left])+ordered[right];if(total==target){result.push_back({ordered[left],ordered[right]});++left;--right;}else if(total<target)++left;else --right;}return result;'
        clone='(int[])values.Clone();Array.Sort(ordered);var result=new List<int[]>();' if language=='csharp' else 'values.clone();Arrays.sort(ordered);List<int[]> result=new ArrayList<>();';size='Length' if language=='csharp' else 'length';append='result.Add([ordered[left],ordered[right]]);' if language=='csharp' else 'result.add(new int[]{ordered[left],ordered[right]});';finish='return result.ToArray();' if language=='csharp' else 'return result.toArray(new int[0][]);'
        return f'int[] ordered={clone}int left=0,right=ordered.{size}-1;while(left<right){{long total=(long)ordered[left]+ordered[right];if(total==target){{{append}++left;--right;}}else if(total<target)++left;else --right;}}{finish}'
    return _previous_batch_body(ref,language)

_previous_language_body=body

def body(ref,language):
    if ref=='16.8':
        small=['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen'];tens=['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety'];scales=['','Thousand','Million','Billion']
        import json
        if language=='python':return f'''if value == 0:
    return "Zero"
small = {small!r}
tens = {tens!r}
scales = {scales!r}
magnitude = abs(value)
groups = []
scale = 0
while magnitude:
    chunk = magnitude % 1000
    if chunk:
        words = []
        if chunk >= 100:
            words.extend([small[chunk // 100], "Hundred"])
            chunk %= 100
        if chunk >= 20:
            words.append(tens[chunk // 10])
            chunk %= 10
        if chunk:
            words.append(small[chunk])
        if scale:
            words.append(scales[scale])
        groups.append(" ".join(words))
    magnitude //= 1000
    scale += 1
return ("Negative " if value < 0 else "") + " ".join(reversed(groups))'''
        if language=='javascript':return f'if(value===0)return "Zero";const small={json.dumps(small)},tens={json.dumps(tens)},scales={json.dumps(scales)},groups=[];let magnitude=Math.abs(value),scale=0;while(magnitude>0){{let chunk=magnitude%1000;if(chunk!==0){{const words=[];if(chunk>=100){{words.push(small[Math.floor(chunk/100)],"Hundred");chunk%=100;}}if(chunk>=20){{words.push(tens[Math.floor(chunk/10)]);chunk%=10;}}if(chunk!==0)words.push(small[chunk]);if(scale!==0)words.push(scales[scale]);groups.push(words.join(" "));}}magnitude=Math.floor(magnitude/1000);++scale;}}return (value<0?"Negative ":"")+groups.reverse().join(" ");'
        array=lambda a:'{'+','.join(json.dumps(w) for w in a)+'}'
        if language=='cpp':return f'if(value==0)return "Zero";const std::vector<std::string> small={array(small)},tens={array(tens)},scales={array(scales)};long long magnitude=value;if(magnitude<0)magnitude=-magnitude;std::vector<std::string> groups;int scale=0;while(magnitude>0){{int chunk=static_cast<int>(magnitude%1000);if(chunk!=0){{std::vector<std::string> words;if(chunk>=100){{words.push_back(small[chunk/100]);words.push_back("Hundred");chunk%=100;}}if(chunk>=20){{words.push_back(tens[chunk/10]);chunk%=10;}}if(chunk!=0)words.push_back(small[chunk]);if(scale!=0)words.push_back(scales[scale]);std::string part;for(const auto& word:words){{if(!part.empty())part+=" ";part+=word;}}groups.push_back(part);}}magnitude/=1000;++scale;}}std::string result=value<0?"Negative ":"";for(auto it=groups.rbegin();it!=groups.rend();++it){{if(it!=groups.rbegin())result+=" ";result+=*it;}}return result;'
        csharp=language=='csharp';typ='string' if csharp else 'String';listType='List<string>' if csharp else 'List<String>';make='new List<string>()' if csharp else 'new ArrayList<>()';add='Add' if csharp else 'add';join=lambda expr:('string.Join' if csharp else 'String.join')+'(" ",'+expr+')';reverse='groups.Reverse();' if csharp else 'Collections.reverse(groups);'
        return f'if(value==0)return "Zero";{typ}[] small={array(small)},tens={array(tens)},scales={array(scales)};long magnitude=value;if(magnitude<0)magnitude=-magnitude;{listType} groups={make};int scale=0;while(magnitude>0){{int chunk=(int)(magnitude%1000);if(chunk!=0){{{listType} words={make};if(chunk>=100){{words.{add}(small[chunk/100]);words.{add}("Hundred");chunk%=100;}}if(chunk>=20){{words.{add}(tens[chunk/10]);chunk%=10;}}if(chunk!=0)words.{add}(small[chunk]);if(scale!=0)words.{add}(scales[scale]);groups.{add}({join("words")});}}magnitude/=1000;++scale;}}{reverse}return (value<0?"Negative ":"")+{join("groups")};'
    if ref=='16.18':
        if language=='python':return '''if not pattern:
    return not text
count_a = pattern.count("a")
count_b = len(pattern) - count_a
maximum = len(text) // count_a if count_a else 0
for length_a in range(maximum + 1):
    remaining = len(text) - count_a * length_a
    if count_b == 0:
        if remaining != 0:
            continue
        length_b = 0
    else:
        if remaining % count_b:
            continue
        length_b = remaining // count_b
    a = b = None
    offset = 0
    valid = True
    for symbol in pattern:
        length = length_a if symbol == "a" else length_b
        part = text[offset:offset + length]
        if symbol == "a":
            if a is None:
                a = part
            elif a != part:
                valid = False
                break
        else:
            if b is None:
                b = part
            elif b != part:
                valid = False
                break
        offset += length
    if valid and offset == len(text):
        return True
return False'''
        if language=='javascript':return 'if(pattern.length===0)return text.length===0;let countA=0;for(const symbol of pattern)if(symbol==="a")++countA;const countB=pattern.length-countA,maximum=countA?Math.floor(text.length/countA):0;for(let lengthA=0;lengthA<=maximum;++lengthA){const remaining=text.length-countA*lengthA;if(countB===0?remaining!==0:remaining%countB!==0)continue;const lengthB=countB===0?0:remaining/countB;let a=null,b=null,offset=0,valid=true;for(const symbol of pattern){const length=symbol==="a"?lengthA:lengthB,part=text.slice(offset,offset+length);if(symbol==="a"){if(a===null)a=part;else if(a!==part){valid=false;break;}}else{if(b===null)b=part;else if(b!==part){valid=false;break;}}offset+=length;}if(valid&&offset===text.length)return true;}return false;'
        if language=='cpp':return 'if(pattern.empty())return text.empty();int countA=0;for(char symbol:pattern)if(symbol==\'a\')++countA;int countB=static_cast<int>(pattern.size())-countA,n=static_cast<int>(text.size()),maximum=countA?n/countA:0;for(int lengthA=0;lengthA<=maximum;++lengthA){int remaining=n-countA*lengthA;if(countB==0?remaining!=0:remaining%countB!=0)continue;int lengthB=countB==0?0:remaining/countB;std::string a,b;bool haveA=false,haveB=false,valid=true;int offset=0;for(char symbol:pattern){int length=symbol==\'a\'?lengthA:lengthB;auto part=text.substr(offset,length);if(symbol==\'a\'){if(!haveA){a=part;haveA=true;}else if(a!=part){valid=false;break;}}else{if(!haveB){b=part;haveB=true;}else if(b!=part){valid=false;break;}}offset+=length;}if(valid&&offset==n)return true;}return false;'
        cs=language=='csharp';plen='pattern.Length' if cs else 'pattern.length()';n='text.Length' if cs else 'text.length()';iteration='foreach(char symbol in pattern)' if cs else 'for(char symbol:pattern.toCharArray())';typ='string?' if cs else 'String';part='text.Substring(offset,length)' if cs else 'text.substring(offset,offset+length)';eq=lambda v:f'{v}!=part' if cs else f'!{v}.equals(part)'
        return f'if({plen}==0)return {n}==0;int countA=0;{iteration}if(symbol==\'a\')++countA;int countB={plen}-countA,maximum=countA==0?0:{n}/countA;for(int lengthA=0;lengthA<=maximum;++lengthA){{int remaining={n}-countA*lengthA;if(countB==0?remaining!=0:remaining%countB!=0)continue;int lengthB=countB==0?0:remaining/countB;{typ} a=null,b=null;int offset=0;bool valid=true;{iteration}{{int length=symbol==\'a\'?lengthA:lengthB;{typ} part={part};if(symbol==\'a\'){{if(a==null)a=part;else if({eq("a")}){{valid=false;break;}}}}else{{if(b==null)b=part;else if({eq("b")}){{valid=false;break;}}}}offset+=length;}}if(valid&&offset=={n})return true;}}return false;'.replace('bool valid','boolean valid' if not cs else 'bool valid')
    if ref=='16.20':
        mapping='22233344455566677778889999'
        if language=='python':return f'''mapping = "{mapping}"
result = []
for word in dictionary:
    if len(word) == len(digits) and all(mapping[ord(letter) - ord("a")] == digit for letter, digit in zip(word, digits)):
        result.append(word)
return result'''
        if language=='javascript':return f'const mapping="{mapping}",result=[];for(const word of dictionary){{if(word.length!==digits.length)continue;let valid=true;for(let i=0;i<word.length;++i)if(mapping[word.charCodeAt(i)-97]!==digits[i]){{valid=false;break;}}if(valid)result.push(word);}}return result;'
        if language=='cpp':return f'const std::string mapping="{mapping}";std::vector<std::string> result;for(const auto& word:dictionary){{if(word.size()!=digits.size())continue;bool valid=true;for(size_t i=0;i<word.size();++i)if(mapping[word[i]-\'a\']!=digits[i]){{valid=false;break;}}if(valid)result.push_back(word);}}return result;'
        if language=='csharp':return f'const string mapping="{mapping}";var result=new List<string>();foreach(string word in dictionary){{if(word.Length!=digits.Length)continue;bool valid=true;for(int i=0;i<word.Length;++i)if(mapping[word[i]-\'a\']!=digits[i]){{valid=false;break;}}if(valid)result.Add(word);}}return result;'
        return f'String mapping="{mapping}";List<String> result=new ArrayList<>();for(String word:dictionary){{if(word.length()!=digits.length())continue;boolean valid=true;for(int i=0;i<word.length();++i)if(mapping.charAt(word.charAt(i)-\'a\')!=digits.charAt(i)){{valid=false;break;}}if(valid)result.add(word);}}return result;'
    return _previous_language_body(ref,language)

_previous_simulation_body=body

def body(ref,language):
    if ref=='16.9':
        if language=='python':return '''def opposite(value):
    step = 1 if value < 0 else -1
    result = 0
    while value != 0:
        value += step
        result += step
    return result
if operation == "subtract":
    return first + opposite(second)
if operation == "multiply":
    count = opposite(second) if second < 0 else second
    addend = opposite(first) if second < 0 else first
    result = 0
    while count > 0:
        result += addend
        count += -1
    return result
remaining = opposite(first) if first < 0 else first
divisor = opposite(second) if second < 0 else second
remove = opposite(divisor)
step = 1 if (first < 0) == (second < 0) else -1
result = 0
while remaining + remove >= 0:
    remaining += remove
    result += step
return result'''
        if language=='javascript':return 'function opposite(value){const step=value<0?1:-1;let result=0;while(value!==0){value+=step;result+=step;}return result;}if(operation==="subtract")return first+opposite(second);if(operation==="multiply"){let count=second<0?opposite(second):second;const addend=second<0?opposite(first):first;let result=0;while(count>0){result+=addend;count+=-1;}return result;}let remaining=first<0?opposite(first):first;const divisor=second<0?opposite(second):second,remove=opposite(divisor),step=(first<0)===(second<0)?1:-1;let result=0;while(remaining+remove>=0){remaining+=remove;result+=step;}return result;'
        helper='int Opposite(int value){int step=value<0?1:-1,result=0;while(value!=0){value+=step;result+=step;}return result;}' if language=='csharp' else 'auto opposite=[](int value){int step=value<0?1:-1,result=0;while(value!=0){value+=step;result+=step;}return result;};' if language=='cpp' else 'class Negator {int opposite(int value){int step=value<0?1:-1,result=0;while(value!=0){value+=step;result+=step;}return result;}}Negator negator=new Negator();'
        call='Opposite' if language=='csharp' else 'opposite' if language=='cpp' else 'negator.opposite';eq=lambda operation:'operation.equals("'+operation+'")' if language=='java' else 'operation=="'+operation+'"'
        return helper+f'if({eq("subtract")})return first+{call}(second);if({eq("multiply")}){{int count=second<0?{call}(second):second,addend=second<0?{call}(first):first,result=0;while(count>0){{result+=addend;count+=-1;}}return result;}}int remaining=first<0?{call}(first):first,divisor=second<0?{call}(second):second,remove={call}(divisor),step=(first<0)==(second<0)?1:-1,quotient=0;while(remaining+remove>=0){{remaining+=remove;quotient+=step;}}return quotient;'
    if ref=='16.22':
        if language=='python':return '''black = set()
row = column = direction = 0
min_row = max_row = min_column = max_column = 0
dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]
for _ in range(steps):
    position = (row, column)
    if position in black:
        direction = (direction + 3) % 4
        black.remove(position)
    else:
        direction = (direction + 1) % 4
        black.add(position)
    row += dr[direction]
    column += dc[direction]
    min_row, max_row = min(min_row, row), max(max_row, row)
    min_column, max_column = min(min_column, column), max(max_column, column)
result = []
for r in range(min_row, max_row + 1):
    line = []
    for c in range(min_column, max_column + 1):
        line.append("RDLU"[direction] if (r, c) == (row, column) else "#" if (r, c) in black else ".")
    result.append("".join(line))
return result'''
        if language=='javascript':return 'const width=2*steps+1,black=new Set(),dr=[0,1,0,-1],dc=[1,0,-1,0];let row=0,column=0,direction=0,minRow=0,maxRow=0,minColumn=0,maxColumn=0;for(let turn=0;turn<steps;++turn){const key=(row+steps)*width+column+steps;if(black.has(key)){direction=(direction+3)%4;black.delete(key);}else{direction=(direction+1)%4;black.add(key);}row+=dr[direction];column+=dc[direction];minRow=Math.min(minRow,row);maxRow=Math.max(maxRow,row);minColumn=Math.min(minColumn,column);maxColumn=Math.max(maxColumn,column);}const result=[];for(let r=minRow;r<=maxRow;++r){const line=[];for(let c=minColumn;c<=maxColumn;++c)line.push(r===row&&c===column?"RDLU"[direction]:black.has((r+steps)*width+c+steps)?"#":".");result.push(line.join(""));}return result;'
        if language=='cpp':return 'int width=2*steps+1,row=0,column=0,direction=0,minRow=0,maxRow=0,minColumn=0,maxColumn=0;std::unordered_set<int> black;const std::array<int,4> dr={0,1,0,-1},dc={1,0,-1,0};for(int turn=0;turn<steps;++turn){int key=(row+steps)*width+column+steps;if(black.count(key)){direction=(direction+3)%4;black.erase(key);}else{direction=(direction+1)%4;black.insert(key);}row+=dr[direction];column+=dc[direction];minRow=std::min(minRow,row);maxRow=std::max(maxRow,row);minColumn=std::min(minColumn,column);maxColumn=std::max(maxColumn,column);}std::vector<std::string> result;for(int r=minRow;r<=maxRow;++r){std::string line;for(int c=minColumn;c<=maxColumn;++c)line+=r==row&&c==column?std::string("RDLU")[direction]:black.count((r+steps)*width+c+steps)?\'#\':\'.\';result.push_back(line);}return result;'
        cs=language=='csharp';setup='var black=new HashSet<int>();' if cs else 'Set<Integer> black=new HashSet<>();';contains='black.Contains' if cs else 'black.contains';remove='black.Remove' if cs else 'black.remove';add='black.Add' if cs else 'black.add';minimum='Math.Min' if cs else 'Math.min';maximum='Math.Max' if cs else 'Math.max';result='var result=new List<string>();' if cs else 'List<String> result=new ArrayList<>();';append='Append' if cs else 'append';finish='result.Add(line.ToString());' if cs else 'result.add(line.toString());';marker='"RDLU"[direction]' if cs else '"RDLU".charAt(direction)'
        return f'int width=2*steps+1,row=0,column=0,direction=0,minRow=0,maxRow=0,minColumn=0,maxColumn=0;{setup}int[] dr={{0,1,0,-1}},dc={{1,0,-1,0}};for(int turn=0;turn<steps;++turn){{int key=(row+steps)*width+column+steps;if({contains}(key)){{direction=(direction+3)%4;{remove}(key);}}else{{direction=(direction+1)%4;{add}(key);}}row+=dr[direction];column+=dc[direction];minRow={minimum}(minRow,row);maxRow={maximum}(maxRow,row);minColumn={minimum}(minColumn,column);maxColumn={maximum}(maxColumn,column);}}{result}for(int r=minRow;r<=maxRow;++r){{var line=new StringBuilder();for(int c=minColumn;c<=maxColumn;++c)line.{append}(r==row&&c==column?{marker}:{contains}((r+steps)*width+c+steps)?\'#\':\'.\');{finish}}}return result;'
    return _previous_simulation_body(ref,language)

_previous_cache_body=body

def body(ref,language):
    if ref!='16.25':return _previous_cache_body(ref,language)
    if language=='python':return '''from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._entries = OrderedDict()

    def Get(self, key: int) -> str | None:
        if key not in self._entries:
            return None
        self._entries.move_to_end(key)
        return self._entries[key]

    def Set(self, key: int, value: str) -> None:
        self._entries[key] = value
        self._entries.move_to_end(key)
        if len(self._entries) > self._capacity:
            self._entries.popitem(last=False)
'''
    if language=='javascript':return 'class LRUCache {constructor(capacity){this.capacity=capacity;this.entries=new Map();}Get(key){if(!this.entries.has(key))return null;const value=this.entries.get(key);this.entries.delete(key);this.entries.set(key,value);return value;}Set(key,value){this.entries.delete(key);this.entries.set(key,value);if(this.entries.size>this.capacity)this.entries.delete(this.entries.keys().next().value);}}'
    if language=='csharp':return 'public class LRUCache {private readonly int capacity;private readonly LinkedList<(int Key,string Text)> order=new();private readonly Dictionary<int,LinkedListNode<(int Key,string Text)>> index=new();public LRUCache(int capacity){this.capacity=capacity;}public string? Get(int key){if(!index.TryGetValue(key,out var node))return null;order.Remove(node);order.AddLast(node);return node.Value.Text;}public void Set(int key,string value){if(index.TryGetValue(key,out var node)){node.Value=(key,value);order.Remove(node);order.AddLast(node);}else{index[key]=order.AddLast((key,value));if(index.Count>capacity){var oldest=order.First!;order.RemoveFirst();index.Remove(oldest.Value.Key);}}}}'
    if language=='java':return 'class LRUCache {private final int capacity;private final LinkedHashMap<Integer,String> entries=new LinkedHashMap<>(16,0.75f,true);public LRUCache(int capacity){this.capacity=capacity;}public String Get(int key){return entries.get(key);}public void Set(int key,String value){entries.put(key,value);if(entries.size()>capacity)entries.remove(entries.keySet().iterator().next());}}'
    return '#include <list>\n#include <optional>\n#include <iterator>\n#include <unordered_map>\nclass LRUCache {using Entry=std::pair<int,std::string>;int capacity;std::list<Entry> order;std::unordered_map<int,std::list<Entry>::iterator> index;public:explicit LRUCache(int capacity):capacity(capacity){}std::optional<std::string> Get(int key){auto found=index.find(key);if(found==index.end())return std::nullopt;order.splice(order.end(),order,found->second);return found->second->second;}void Set(int key,const std::string& value){auto found=index.find(key);if(found!=index.end()){found->second->second=value;order.splice(order.end(),order,found->second);}else{order.emplace_back(key,value);index[key]=std::prev(order.end());if(order.size()>static_cast<size_t>(capacity)){index.erase(order.front().first);order.pop_front();}}}};'

_previous_line_body=body

def body(ref,language):
    if ref!='16.14':return _previous_line_body(ref,language)
    if language=='python':return '''from math import gcd
if not points:
    return []
best = [1, 0, -points[0][0]]
best_count = 0
for anchor in range(len(points)):
    groups = {}
    duplicates = 0
    x, y = points[anchor]
    for other in range(anchor + 1, len(points)):
        dx, dy = points[other][0] - x, points[other][1] - y
        if dx == 0 and dy == 0:
            duplicates += 1
            continue
        divisor = gcd(abs(dx), abs(dy))
        dx //= divisor
        dy //= divisor
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        groups[(dy, dx)] = groups.get((dy, dx), 0) + 1
    for (dy, dx), count in groups.items():
        if count + duplicates + 1 > best_count:
            best_count = count + duplicates + 1
            a, b = dy, -dx
            c = -a * x - b * y
            if a < 0 or (a == 0 and b < 0):
                a, b, c = -a, -b, -c
            best = [a, b, c]
return best'''
    if language=='javascript':return 'if(points.length===0)return [];function gcd(a,b){while(b!==0){const next=a%b;a=b;b=next;}return a;}let best=[1,0,-points[0][0]],bestCount=0;for(let anchor=0;anchor<points.length;++anchor){const groups=new Map(),[x,y]=points[anchor];let duplicates=0;for(let other=anchor+1;other<points.length;++other){let dx=points[other][0]-x,dy=points[other][1]-y;if(dx===0&&dy===0){++duplicates;continue;}const divisor=gcd(Math.abs(dx),Math.abs(dy));dx/=divisor;dy/=divisor;if(dx<0||(dx===0&&dy<0)){dx=-dx;dy=-dy;}const key=dy+","+dx;groups.set(key,(groups.get(key)||0)+1);}for(const [key,count] of groups)if(count+duplicates+1>bestCount){bestCount=count+duplicates+1;const [dy,dx]=key.split(",").map(Number);let a=dy,b=-dx,c=-a*x-b*y;if(a<0||(a===0&&b<0)){a=-a;b=-b;c=-c;}best=[a,b,c];}}return best;'
    if language=='csharp':return 'if(points.Length==0)return [];int Gcd(int a,int b){while(b!=0){int next=a%b;a=b;b=next;}return a;}int[] best=[1,0,-points[0][0]];int bestCount=0;for(int anchor=0;anchor<points.Length;++anchor){var groups=new Dictionary<(int Dy,int Dx),int>();int duplicates=0,x=points[anchor][0],y=points[anchor][1];for(int other=anchor+1;other<points.Length;++other){int dx=points[other][0]-x,dy=points[other][1]-y;if(dx==0&&dy==0){++duplicates;continue;}int divisor=Gcd(Math.Abs(dx),Math.Abs(dy));dx/=divisor;dy/=divisor;if(dx<0||(dx==0&&dy<0)){dx=-dx;dy=-dy;}groups.TryGetValue((dy,dx),out int count);groups[(dy,dx)]=count+1;}foreach(var entry in groups)if(entry.Value+duplicates+1>bestCount){bestCount=entry.Value+duplicates+1;int a=entry.Key.Dy,b=-entry.Key.Dx,c=-a*x-b*y;if(a<0||(a==0&&b<0)){a=-a;b=-b;c=-c;}best=[a,b,c];}}return best;'
    if language=='java':return 'if(points.length==0)return new int[0];class MathHelper {int gcd(int a,int b){while(b!=0){int next=a%b;a=b;b=next;}return a;}}var math=new MathHelper();int[] best={1,0,-points[0][0]};int bestCount=0;for(int anchor=0;anchor<points.length;++anchor){Map<Integer,Integer> groups=new HashMap<>();int duplicates=0,x=points[anchor][0],y=points[anchor][1];for(int other=anchor+1;other<points.length;++other){int dx=points[other][0]-x,dy=points[other][1]-y;if(dx==0&&dy==0){++duplicates;continue;}int divisor=math.gcd(Math.abs(dx),Math.abs(dy));dx/=divisor;dy/=divisor;if(dx<0||(dx==0&&dy<0)){dx=-dx;dy=-dy;}int key=(dy+2000)*4001+dx;groups.put(key,groups.getOrDefault(key,0)+1);}for(var entry:groups.entrySet())if(entry.getValue()+duplicates+1>bestCount){bestCount=entry.getValue()+duplicates+1;int a=entry.getKey()/4001-2000,b=-(entry.getKey()%4001),c=-a*x-b*y;if(a<0||(a==0&&b<0)){a=-a;b=-b;c=-c;}best=new int[]{a,b,c};}}return best;'
    return 'if(points.empty())return {};auto gcd=[](int a,int b){while(b!=0){int next=a%b;a=b;b=next;}return a;};std::vector<int> best{1,0,-points[0][0]};int bestCount=0;for(size_t anchor=0;anchor<points.size();++anchor){std::unordered_map<int,int> groups;int duplicates=0,x=points[anchor][0],y=points[anchor][1];for(size_t other=anchor+1;other<points.size();++other){int dx=points[other][0]-x,dy=points[other][1]-y;if(dx==0&&dy==0){++duplicates;continue;}int divisor=gcd(dx<0?-dx:dx,dy<0?-dy:dy);dx/=divisor;dy/=divisor;if(dx<0||(dx==0&&dy<0)){dx=-dx;dy=-dy;}++groups[(dy+2000)*4001+dx];}for(const auto& entry:groups)if(entry.second+duplicates+1>bestCount){bestCount=entry.second+duplicates+1;int a=entry.first/4001-2000,b=-(entry.first%4001),c=-a*x-b*y;if(a<0||(a==0&&b<0)){a=-a;b=-b;c=-c;}best={a,b,c};}}return best;'

_previous_numeric_body=body

def body(ref,language):
    if ref!='16.26':return _previous_numeric_body(ref,language)
    if language=='python':return '''total = 0.0
term = 0.0
operator = '+'
index = 0
while index < len(expression):
    number = 0
    while index < len(expression) and '0' <= expression[index] <= '9':
        number = number * 10 + ord(expression[index]) - ord('0')
        index += 1
    if operator == '+':
        total += term
        term = float(number)
    elif operator == '-':
        total += term
        term = -float(number)
    elif operator == '*':
        term *= number
    else:
        term /= number
    if index < len(expression):
        operator = expression[index]
        index += 1
return total + term'''
    if language=='javascript':return "let total=0,term=0,operator='+',index=0;while(index<expression.length){let number=0;while(index<expression.length&&expression[index]>='0'&&expression[index]<='9'){number=number*10+expression.charCodeAt(index)-48;++index;}if(operator==='+'){total+=term;term=number;}else if(operator==='-'){total+=term;term=-number;}else if(operator==='*')term*=number;else term/=number;if(index<expression.length)operator=expression[index++];}return total+term;"
    if language=='csharp':return "double total=0,term=0;char op='+';int index=0;while(index<expression.Length){int number=0;while(index<expression.Length&&expression[index]>='0'&&expression[index]<='9'){number=number*10+expression[index]-'0';index++;}if(op=='+'){total+=term;term=number;}else if(op=='-'){total+=term;term=-number;}else if(op=='*')term*=number;else term/=number;if(index<expression.Length)op=expression[index++];}return total+term;"
    if language=='java':return "double total=0,term=0;char op='+';int index=0;while(index<expression.length()){int number=0;while(index<expression.length()&&expression.charAt(index)>='0'&&expression.charAt(index)<='9'){number=number*10+expression.charAt(index)-'0';index++;}if(op=='+'){total+=term;term=number;}else if(op=='-'){total+=term;term=-number;}else if(op=='*')term*=number;else term/=number;if(index<expression.length())op=expression.charAt(index++);}return total+term;"
    return "double total=0,term=0;char op='+';size_t index=0;while(index<expression.size()){int number=0;while(index<expression.size()&&expression[index]>='0'&&expression[index]<='9'){number=number*10+expression[index]-'0';++index;}if(op=='+'){total+=term;term=number;}else if(op=='-'){total+=term;term=-number;}else if(op=='*')term*=number;else term/=number;if(index<expression.size())op=expression[index++];}return total+term;"

_previous_geometry_body=body

def body(ref,language):
    if ref not in ('16.3','16.13'):return _previous_geometry_body(ref,language)
    if ref=='16.3':
        if language=='python':return '''a, b, c, d = endpoints
rx, ry = b[0]-a[0], b[1]-a[1]
sx, sy = d[0]-c[0], d[1]-c[1]
qx, qy = c[0]-a[0], c[1]-a[1]
denominator = rx*sy-ry*sx
if denominator != 0:
    first = qx*sy-qy*sx
    second = qx*ry-qy*rx
    if denominator < 0:
        denominator, first, second = -denominator, -first, -second
    if 0 <= first <= denominator and 0 <= second <= denominator:
        t = first/denominator
        return [a[0]+t*rx, a[1]+t*ry]
    return []
def contains(start, end, point):
    return ((end[0]-start[0])*(point[1]-start[1]) == (end[1]-start[1])*(point[0]-start[0])
            and min(start[0],end[0]) <= point[0] <= max(start[0],end[0])
            and min(start[1],end[1]) <= point[1] <= max(start[1],end[1]))
for point in endpoints:
    if contains(a,b,point) and contains(c,d,point):
        return [float(point[0]),float(point[1])]
return []'''
        if language=='javascript':return 'const [a,b,c,d]=endpoints,rx=b[0]-a[0],ry=b[1]-a[1],sx=d[0]-c[0],sy=d[1]-c[1],qx=c[0]-a[0],qy=c[1]-a[1];let denominator=rx*sy-ry*sx;if(denominator!==0){let first=qx*sy-qy*sx,second=qx*ry-qy*rx;if(denominator<0){denominator=-denominator;first=-first;second=-second;}if(first>=0&&first<=denominator&&second>=0&&second<=denominator){const t=first/denominator;return [a[0]+t*rx,a[1]+t*ry];}return [];}function contains(start,end,point){return (end[0]-start[0])*(point[1]-start[1])===(end[1]-start[1])*(point[0]-start[0])&&point[0]>=Math.min(start[0],end[0])&&point[0]<=Math.max(start[0],end[0])&&point[1]>=Math.min(start[1],end[1])&&point[1]<=Math.max(start[1],end[1]);}for(const point of endpoints)if(contains(a,b,point)&&contains(c,d,point))return [point[0],point[1]];return [];'
        empty='return new double[0];' if language=='java' else 'return [];' if language=='csharp' else 'return {};'
        ret=lambda v:'return new double[]{'+v+'};' if language=='java' else 'return ['+v+'];' if language=='csharp' else 'return {'+v+'};'
        setup='int[] a=endpoints[0],b=endpoints[1],c=endpoints[2],d=endpoints[3];' if language in ('java','csharp') else 'const auto& a=endpoints[0];const auto& b=endpoints[1];const auto& c=endpoints[2];const auto& d=endpoints[3];'
        minimum='Math.min' if language=='java' else 'Math.Min' if language=='csharp' else 'std::min';maximum='Math.max' if language=='java' else 'Math.Max' if language=='csharp' else 'std::max'
        check=f'return (end[0]-start[0])*(point[1]-start[1])==(end[1]-start[1])*(point[0]-start[0])&&point[0]>={minimum}(start[0],end[0])&&point[0]<={maximum}(start[0],end[0])&&point[1]>={minimum}(start[1],end[1])&&point[1]<={maximum}(start[1],end[1]);'
        if language=='java':helper='class Geometry {boolean contains(int[] start,int[] end,int[] point){'+check+'}}var geometry=new Geometry();';call='geometry.contains';loop='for(int[] point:endpoints)'
        elif language=='csharp':helper='bool Contains(int[] start,int[] end,int[] point){'+check+'}';call='Contains';loop='foreach(var point in endpoints)'
        else:helper='auto contains=[](const std::vector<int>& start,const std::vector<int>& end,const std::vector<int>& point){'+check+'};';call='contains';loop='for(const auto& point:endpoints)'
        return setup+'int rx=b[0]-a[0],ry=b[1]-a[1],sx=d[0]-c[0],sy=d[1]-c[1],qx=c[0]-a[0],qy=c[1]-a[1],denominator=rx*sy-ry*sx;if(denominator!=0){int first=qx*sy-qy*sx,second=qx*ry-qy*rx;if(denominator<0){denominator=-denominator;first=-first;second=-second;}if(first>=0&&first<=denominator&&second>=0&&second<=denominator){double t=(double)first/denominator;'+ret('a[0]+t*rx,a[1]+t*ry')+'}'+empty+'}'+helper+loop+'if('+call+'(a,b,point)&&'+call+'(c,d,point))'+ret('(double)point[0],(double)point[1]')+empty
    if language=='python':return '''x = squares[0][0]+squares[0][2]/2.0
y = squares[0][1]+squares[0][2]/2.0
dx = squares[1][0]+squares[1][2]/2.0-x
dy = squares[1][1]+squares[1][2]/2.0-y
if dx == 0 and dy == 0:
    dy = 1.0
    other = 0.0
else:
    other = 1.0
scale = max(abs(dx),abs(dy))
first_radius = squares[0][2]/(2.0*scale)
second_radius = squares[1][2]/(2.0*scale)
start = min(-first_radius,other-second_radius)
end = max(first_radius,other+second_radius)
return [x+start*dx,y+start*dy,x+end*dx,y+end*dy]'''
    if language=='javascript':return 'const x=squares[0][0]+squares[0][2]/2,y=squares[0][1]+squares[0][2]/2;let dx=squares[1][0]+squares[1][2]/2-x,dy=squares[1][1]+squares[1][2]/2-y,other=1;if(dx===0&&dy===0){dy=1;other=0;}const scale=Math.max(Math.abs(dx),Math.abs(dy)),first=squares[0][2]/(2*scale),second=squares[1][2]/(2*scale),start=Math.min(-first,other-second),end=Math.max(first,other+second);return [x+start*dx,y+start*dy,x+end*dx,y+end*dy];'
    minimum='Math.min' if language=='java' else 'Math.Min' if language=='csharp' else 'std::min';maximum='Math.max' if language=='java' else 'Math.Max' if language=='csharp' else 'std::max';absolute='Math.abs' if language=='java' else 'Math.Abs' if language=='csharp' else 'std::abs'
    result='x+start*dx,y+start*dy,x+end*dx,y+end*dy'
    ret='return new double[]{'+result+'};' if language=='java' else 'return ['+result+'];' if language=='csharp' else 'return {'+result+'};'
    return f'double x=squares[0][0]+squares[0][2]/2.0,y=squares[0][1]+squares[0][2]/2.0,dx=squares[1][0]+squares[1][2]/2.0-x,dy=squares[1][1]+squares[1][2]/2.0-y,other=1;if(dx==0&&dy==0){{dy=1;other=0;}}double scale={maximum}({absolute}(dx),{absolute}(dy)),first=squares[0][2]/(2.0*scale),second=squares[1][2]/(2.0*scale),start={minimum}(-first,other-second),end={maximum}(first,other+second);'+ret

_previous_xml_body=body

def body(ref,language):
    if ref!='16.12':return _previous_xml_body(ref,language)
    if language=='python':return '''if not elementNames:
    return []
lookup = {name: str(code) for name,code in zip(codeNames,codes)}
attributes = [[] for _ in elementNames]
for index,owner in enumerate(attributeOwners):
    attributes[owner].append(index)
result = []
events = [(0,False)]
while events:
    node, exiting = events.pop()
    if exiting:
        result.append('0')
        continue
    result.append(lookup[elementNames[node]])
    for attribute in attributes[node]:
        result.extend([lookup[attributeNames[attribute]],attributeValues[attribute]])
    result.append('0')
    events.append((node,True))
    if elementTexts[node]:
        result.append(elementTexts[node])
    else:
        for child in reversed(children[node]):
            events.append((child,False))
return result'''
    if language=='javascript':return 'if(elementNames.length===0)return [];const lookup=new Map(codeNames.map((name,i)=>[name,String(codes[i])])),attributes=Array.from({length:elementNames.length},()=>[]),result=[],events=[[0,false]];for(let i=0;i<attributeOwners.length;++i)attributes[attributeOwners[i]].push(i);while(events.length){const [node,exiting]=events.pop();if(exiting){result.push("0");continue;}result.push(lookup.get(elementNames[node]));for(const attribute of attributes[node])result.push(lookup.get(attributeNames[attribute]),attributeValues[attribute]);result.push("0");events.push([node,true]);if(elementTexts[node].length)result.push(elementTexts[node]);else for(let i=children[node].length-1;i>=0;--i)events.push([children[node][i],false]);}return result;'
    if language=='csharp':return 'var result=new List<string>();if(elementNames.Length==0)return result;var lookup=new Dictionary<string,string>(StringComparer.Ordinal);for(int i=0;i<codeNames.Length;++i)lookup[codeNames[i]]=codes[i].ToString(System.Globalization.CultureInfo.InvariantCulture);var attributes=new List<int>[elementNames.Length];for(int i=0;i<attributes.Length;++i)attributes[i]=new List<int>();for(int i=0;i<attributeOwners.Length;++i)attributes[attributeOwners[i]].Add(i);var events=new Stack<(int Node,bool Exit)>();events.Push((0,false));while(events.Count>0){var frame=events.Pop();int node=frame.Node;if(frame.Exit){result.Add("0");continue;}result.Add(lookup[elementNames[node]]);foreach(int attribute in attributes[node]){result.Add(lookup[attributeNames[attribute]]);result.Add(attributeValues[attribute]);}result.Add("0");events.Push((node,true));if(elementTexts[node].Length>0)result.Add(elementTexts[node]);else for(int i=children[node].Length-1;i>=0;--i)events.Push((children[node][i],false));}return result;'
    if language=='java':return 'var result=new ArrayList<String>();if(elementNames.length==0)return result;var lookup=new HashMap<String,String>();for(int i=0;i<codeNames.length;++i)lookup.put(codeNames[i],Integer.toString(codes[i]));var attributes=new ArrayList<ArrayList<Integer>>();for(int i=0;i<elementNames.length;++i)attributes.add(new ArrayList<>());for(int i=0;i<attributeOwners.length;++i)attributes.get(attributeOwners[i]).add(i);var events=new ArrayDeque<int[]>();events.push(new int[]{0,0});while(!events.isEmpty()){int[] frame=events.pop();int node=frame[0];if(frame[1]!=0){result.add("0");continue;}result.add(lookup.get(elementNames[node]));for(int attribute:attributes.get(node)){result.add(lookup.get(attributeNames[attribute]));result.add(attributeValues[attribute]);}result.add("0");events.push(new int[]{node,1});if(!elementTexts[node].isEmpty())result.add(elementTexts[node]);else for(int i=children[node].length-1;i>=0;--i)events.push(new int[]{children[node][i],0});}return result;'
    return 'std::vector<std::string> result;if(elementNames.empty())return result;std::unordered_map<std::string,std::string> lookup;for(size_t i=0;i<codeNames.size();++i)lookup[codeNames[i]]=std::to_string(codes[i]);std::vector<std::vector<size_t>> attributes(elementNames.size());for(size_t i=0;i<attributeOwners.size();++i)attributes[attributeOwners[i]].push_back(i);std::vector<std::pair<int,bool>> events{{0,false}};while(!events.empty()){auto frame=events.back();events.pop_back();int node=frame.first;if(frame.second){result.push_back("0");continue;}result.push_back(lookup.at(elementNames[node]));for(size_t attribute:attributes[node]){result.push_back(lookup.at(attributeNames[attribute]));result.push_back(attributeValues[attribute]);}result.push_back("0");events.emplace_back(node,true);if(!elementTexts[node].empty())result.push_back(elementTexts[node]);else for(auto it=children[node].rbegin();it!=children[node].rend();++it)events.emplace_back(*it,false);}return result;'
