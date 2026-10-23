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
