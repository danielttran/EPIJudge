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


def previous(ref, language):
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


def body(ref, language):
    if ref not in ("8.3", "8.12", "8.13", "8.14"):
        return previous(ref, language)
    if ref == "8.3":
        if language == "python":
            return """if distinctValues:
    low, high = 0, len(values) - 1
    while low <= high:
        middle = low + (high - low) // 2
        if values[middle] == middle:
            return middle
        if values[middle] > middle:
            high = middle - 1
        else:
            low = middle + 1
    return -1
def search(low, high):
    if low > high:
        return -1
    middle = low + (high - low) // 2
    value = values[middle]
    if value == middle:
        return middle
    left = search(low, min(middle - 1, value))
    return left if left != -1 else search(max(middle + 1, value), high)
return search(0, len(values) - 1)"""
        if language == "javascript":
            return "if(distinctValues){let low=0,high=values.length-1;while(low<=high){const middle=low+Math.floor((high-low)/2);if(values[middle]===middle)return middle;if(values[middle]>middle)high=middle-1;else low=middle+1;}return -1;}function search(low,high){if(low>high)return -1;const middle=low+Math.floor((high-low)/2),value=values[middle];if(value===middle)return middle;const left=search(low,Math.min(middle-1,value));return left!==-1?left:search(Math.max(middle+1,value),high);}return search(0,values.length-1);"
        size = (
            "values.Length"
            if language == "csharp"
            else "values.length"
            if language == "java"
            else "static_cast<int>(values.size())"
        )
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
        binary = f"if(distinctValues){{int low=0,high={size}-1;while(low<=high){{int middle=low+(high-low)/2;if(values[middle]==middle)return middle;if(values[middle]>middle)high=middle-1;else low=middle+1;}}return -1;}}"
        name = "search" if language == "cpp" else "Search"
        logic = f"if(low>high)return -1;int middle=low+(high-low)/2,value=values[middle];if(value==middle)return middle;int left={name}(low,{minimum}(middle-1,value));return left!=-1?left:{name}({maximum}(middle+1,value),high);"
        helper = (
            f"int Search(int low,int high){{{logic}}}return Search(0,{size}-1);"
            if language == "csharp"
            else f"class Finder {{int Search(int low,int high){{{logic}}}}}return new Finder().Search(0,{size}-1);"
            if language == "java"
            else f"std::function<int(int,int)> search=[&](int low,int high){{{logic}}};return search(0,{size}-1);"
        )
        return binary + helper
    if ref == "8.12":
        if language == "python":
            return """board = [0] * 8
result = []
def visit(row, used_columns, used_down, used_up):
    if row == 8:
        result.append(board.copy())
        return
    for column in range(8):
        col_bit = 1 << column
        down_bit = 1 << (row - column + 7)
        up_bit = 1 << (row + column)
        if used_columns & col_bit or used_down & down_bit or used_up & up_bit:
            continue
        board[row] = column
        visit(row + 1, used_columns | col_bit, used_down | down_bit, used_up | up_bit)
visit(0, 0, 0, 0)
return result"""
        if language == "javascript":
            return "const board=Array(8).fill(0),result=[];function visit(row,usedColumns,usedDown,usedUp){if(row===8){result.push(board.slice());return;}for(let column=0;column<8;++column){const colBit=1<<column,downBit=1<<(row-column+7),upBit=1<<(row+column);if((usedColumns&colBit)||(usedDown&downBit)||(usedUp&upBit))continue;board[row]=column;visit(row+1,usedColumns|colBit,usedDown|downBit,usedUp|upBit);}}visit(0,0,0,0);return result;"
        setup = (
            "int[] board=new int[8];var result=new List<List<int>>();"
            if language == "csharp"
            else "int[] board=new int[8];List<List<Integer>> result=new ArrayList<>();"
            if language == "java"
            else "std::vector<int> board(8);std::vector<std::vector<int>> result;"
        )
        emit = (
            "result.Add(new List<int>(board));"
            if language == "csharp"
            else "var copy=new ArrayList<Integer>();for(int column:board)copy.add(column);result.add(copy);"
            if language == "java"
            else "result.push_back(board);"
        )
        name = "visit" if language == "cpp" else "Visit"
        logic = f"if(row==8){{{emit}return;}}for(int column=0;column<8;++column){{int colBit=1<<column,downBit=1<<(row-column+7),upBit=1<<(row+column);if((usedColumns&colBit)!=0 || (usedDown&downBit)!=0 || (usedUp&upBit)!=0)continue;board[row]=column;{name}(row+1,usedColumns|colBit,usedDown|downBit,usedUp|upBit);}}"
        signature = "int row,int usedColumns,int usedDown,int usedUp"
        helper = (
            f"void Visit({signature}){{{logic}}}Visit(0,0,0,0);"
            if language == "csharp"
            else f"class Search {{void Visit({signature}){{{logic}}}}}new Search().Visit(0,0,0,0);"
            if language == "java"
            else f"std::function<void(int,int,int,int)> visit=[&]({signature}){{{logic}}};visit(0,0,0,0);"
        )
        return setup + helper + "return result;"
    if ref == "8.13":
        if language == "python":
            return """order = sorted(range(len(boxes)), key=lambda index: boxes[index][0])
heights = [0] * len(order)
best = 0
for position, current in enumerate(order):
    heights[position] = boxes[current][1]
    for earlier in range(position):
        top = order[earlier]
        if all(boxes[top][dimension] < boxes[current][dimension] for dimension in range(3)):
            heights[position] = max(heights[position], boxes[current][1] + heights[earlier])
    best = max(best, heights[position])
return best"""
        if language == "javascript":
            return "const order=Array.from({length:boxes.length},(_,i)=>i).sort((a,b)=>boxes[a][0]-boxes[b][0]),heights=Array(boxes.length).fill(0);let best=0;for(let i=0;i<order.length;++i){const current=order[i];heights[i]=boxes[current][1];for(let j=0;j<i;++j){const top=order[j];if(boxes[top][0]<boxes[current][0]&&boxes[top][1]<boxes[current][1]&&boxes[top][2]<boxes[current][2])heights[i]=Math.max(heights[i],boxes[current][1]+heights[j]);}best=Math.max(best,heights[i]);}return best;"
        size = (
            "boxes.Length"
            if language == "csharp"
            else "boxes.length"
            if language == "java"
            else "static_cast<int>(boxes.size())"
        )
        setup = (
            "int[] order=new int[n],heights=new int[n];for(int i=0;i<n;++i)order[i]=i;Array.Sort(order,(a,b)=>boxes[a][0].CompareTo(boxes[b][0]));"
            if language == "csharp"
            else "Integer[] order=new Integer[n];int[] heights=new int[n];for(int i=0;i<n;++i)order[i]=i;Arrays.sort(order,(a,b)->Integer.compare(boxes[a][0],boxes[b][0]));"
            if language == "java"
            else "std::vector<int> order(n),heights(n);for(int i=0;i<n;++i)order[i]=i;std::sort(order.begin(),order.end(),[&](int a,int b){return boxes[a][0]<boxes[b][0];});"
        )
        maximum = (
            "Math.Max"
            if language == "csharp"
            else "Math.max"
            if language == "java"
            else "std::max"
        )
        return f"int n={size};{setup}int best=0;for(int i=0;i<n;++i){{int current=order[i];heights[i]=boxes[current][1];for(int j=0;j<i;++j){{int top=order[j];if(boxes[top][0]<boxes[current][0] && boxes[top][1]<boxes[current][1] && boxes[top][2]<boxes[current][2])heights[i]={maximum}(heights[i],boxes[current][1]+heights[j]);}}best={maximum}(best,heights[i]);}}return best;"
    if ref == "8.14":
        if language == "python":
            return """if not expression:
    return 0
count = (len(expression) + 1) // 2
truth = [[0] * count for _ in range(count)]
falsity = [[0] * count for _ in range(count)]
for index in range(count):
    truth[index][index] = 1 if expression[2 * index] == '1' else 0
    falsity[index][index] = 1 - truth[index][index]
for length in range(2, count + 1):
    for low in range(count - length + 1):
        high = low + length - 1
        for split in range(low, high):
            lt, lf = truth[low][split], falsity[low][split]
            rt, rf = truth[split + 1][high], falsity[split + 1][high]
            total = (lt + lf) * (rt + rf)
            operation = expression[2 * split + 1]
            true_count = lt * rt if operation == '&' else total - lf * rf if operation == '|' else lt * rf + lf * rt
            truth[low][high] += true_count
            falsity[low][high] += total - true_count
return truth[0][count - 1] if desired else falsity[0][count - 1]"""
        if language == "javascript":
            return 'if(expression.length===0)return 0;const count=(expression.length+1)/2,truth=Array.from({length:count},()=>Array(count).fill(0)),falsity=Array.from({length:count},()=>Array(count).fill(0));for(let i=0;i<count;++i){truth[i][i]=expression[2*i]==="1"?1:0;falsity[i][i]=1-truth[i][i];}for(let length=2;length<=count;++length){for(let low=0;low+length<=count;++low){const high=low+length-1;for(let split=low;split<high;++split){const lt=truth[low][split],lf=falsity[low][split],rt=truth[split+1][high],rf=falsity[split+1][high],total=(lt+lf)*(rt+rf),operation=expression[2*split+1],trueCount=operation==="&"?lt*rt:operation==="|"?total-lf*rf:lt*rf+lf*rt;truth[low][high]+=trueCount;falsity[low][high]+=total-trueCount;}}}return desired?truth[0][count-1]:falsity[0][count-1];'
        size = (
            "expression.Length"
            if language == "csharp"
            else "expression.length()"
            if language == "java"
            else "static_cast<int>(expression.size())"
        )
        tables = (
            "int[,] truth=new int[count,count],falsity=new int[count,count];"
            if language == "csharp"
            else "int[][] truth=new int[count][count],falsity=new int[count][count];"
            if language == "java"
            else "std::vector<std::vector<int>> truth(count,std::vector<int>(count)),falsity(count,std::vector<int>(count));"
        )
        at = lambda table, i, j: (
            table + "[" + i + "," + j + "]"
            if language == "csharp"
            else table + "[" + i + "][" + j + "]"
        )
        char = lambda index: (
            "expression.charAt(" + index + ")"
            if language == "java"
            else "expression[" + index + "]"
        )
        return f"""if({size}==0)return 0;int count=({size}+1)/2;{tables}
for(int i=0;i<count;++i){{{at("truth", "i", "i")}={char("2*i")}=='1'?1:0;{at("falsity", "i", "i")}=1-{at("truth", "i", "i")};}}
for(int length=2;length<=count;++length){{for(int low=0;low+length<=count;++low){{int high=low+length-1;for(int split=low;split<high;++split){{int lt={at("truth", "low", "split")},lf={at("falsity", "low", "split")},rt={at("truth", "split+1", "high")},rf={at("falsity", "split+1", "high")},total=(lt+lf)*(rt+rf);char operation={char("2*split+1")};int trueCount=operation=='&'?lt*rt:operation=='|'?total-lf*rf:lt*rf+lf*rt;{at("truth", "low", "high")}+=trueCount;{at("falsity", "low", "high")}+=total-trueCount;}}}}}}
return desired?{at("truth", "0", "count-1")}:{at("falsity", "0", "count-1")};"""
    raise ValueError(ref)

_prior_body = body

def body(ref, language):
    if ref not in ('8.2','8.6','8.10'):
        return _prior_body(ref, language)
    if ref == '8.2':
        if language == 'python':
            return '''rows = len(grid)
columns = len(grid[0]) if rows else 0
if not rows or not columns:
    return []
parent = [[0] * columns for _ in range(rows)]
for r in range(rows):
    for c in range(columns):
        if grid[r][c] == 0:
            continue
        if r == 0 and c == 0:
            parent[r][c] = 3
        elif r > 0 and parent[r - 1][c]:
            parent[r][c] = 1
        elif c > 0 and parent[r][c - 1]:
            parent[r][c] = 2
if not parent[-1][-1]:
    return []
path = []
r, c = rows - 1, columns - 1
while True:
    path.append([r, c])
    if r == 0 and c == 0:
        break
    if parent[r][c] == 1:
        r -= 1
    else:
        c -= 1
path.reverse()
return path'''
        if language == 'javascript':
            return 'const rows=grid.length,columns=rows?grid[0].length:0;if(!rows||!columns)return [];const parent=Array.from({length:rows},()=>Array(columns).fill(0));for(let r=0;r<rows;++r){for(let c=0;c<columns;++c){if(grid[r][c]===0)continue;if(r===0&&c===0)parent[r][c]=3;else if(r>0&&parent[r-1][c])parent[r][c]=1;else if(c>0&&parent[r][c-1])parent[r][c]=2;}}if(!parent[rows-1][columns-1])return [];const path=[];let r=rows-1,c=columns-1;while(true){path.push([r,c]);if(r===0&&c===0)break;if(parent[r][c]===1)--r;else --c;}path.reverse();return path;'
        rows = 'grid.Length' if language=='csharp' else 'grid.length' if language=='java' else 'static_cast<int>(grid.size())'
        cols = 'grid[0].Length' if language=='csharp' else 'grid[0].length' if language=='java' else 'static_cast<int>(grid[0].size())'
        setup = 'int[,] parent=new int[rows,columns];var path=new List<List<int>>();' if language=='csharp' else 'int[][] parent=new int[rows][columns];List<List<Integer>> path=new ArrayList<>();' if language=='java' else 'std::vector<std::vector<int>> parent(rows,std::vector<int>(columns)),path;'
        at = lambda r,c: f'parent[{r},{c}]' if language=='csharp' else f'parent[{r}][{c}]'
        empty = 'return [];' if language=='csharp' else 'return new ArrayList<>();' if language=='java' else 'return {};'
        add = 'path.Add([row,col]);' if language=='csharp' else 'path.add(new ArrayList<>(List.of(row,col)));' if language=='java' else 'path.push_back({row,col});'
        reverse = 'path.Reverse();' if language=='csharp' else 'Collections.reverse(path);' if language=='java' else 'std::reverse(path.begin(),path.end());'
        return f'''int rows={rows},columns=rows==0?0:{cols};if(rows==0||columns==0){{{empty}}}{setup}
for(int r=0;r<rows;++r){{for(int c=0;c<columns;++c){{if(grid[r][c]==0)continue;if(r==0&&c==0){at('r','c')}=3;else if(r>0&&{at('r-1','c')}!=0){at('r','c')}=1;else if(c>0&&{at('r','c-1')}!=0){at('r','c')}=2;}}}}
if({at('rows-1','columns-1')}==0){{{empty}}}int row=rows-1,col=columns-1;while(true){{{add}if(row==0&&col==0)break;if({at('row','col')}==1)--row;else --col;}}{reverse}return path;'''
    if ref == '8.6':
        if language == 'python':
            return '''towers = [list(range(disks, 0, -1)), [], []]
moves = []
def transfer(count, source, buffer, destination):
    if count == 0:
        return
    transfer(count - 1, source, destination, buffer)
    disk = towers[source].pop()
    towers[destination].append(disk)
    moves.append([disk, source, destination])
    transfer(count - 1, buffer, source, destination)
transfer(disks, 0, 1, 2)
return moves'''
        if language == 'javascript':
            return 'const towers=[Array.from({length:disks},(_,i)=>disks-i),[],[]],moves=[];function transfer(count,source,buffer,destination){if(count===0)return;transfer(count-1,source,destination,buffer);const disk=towers[source].pop();towers[destination].push(disk);moves.push([disk,source,destination]);transfer(count-1,buffer,source,destination);}transfer(disks,0,1,2);return moves;'
        setup = 'var towers=new Stack<int>[] {new(),new(),new()};for(int disk=disks;disk>=1;--disk)towers[0].Push(disk);var moves=new List<List<int>>();' if language=='csharp' else 'List<Deque<Integer>> towers=List.of(new ArrayDeque<>(),new ArrayDeque<>(),new ArrayDeque<>());for(int disk=disks;disk>=1;--disk)towers.get(0).push(disk);List<List<Integer>> moves=new ArrayList<>();' if language=='java' else 'std::array<std::vector<int>,3> towers;for(int disk=disks;disk>=1;--disk)towers[0].push_back(disk);std::vector<std::vector<int>> moves;'
        operation = 'int disk=towers[source].Pop();towers[destination].Push(disk);moves.Add([disk,source,destination]);' if language=='csharp' else 'int disk=towers.get(source).pop();towers.get(destination).push(disk);moves.add(new ArrayList<>(List.of(disk,source,destination)));' if language=='java' else 'int disk=towers[source].back();towers[source].pop_back();towers[destination].push_back(disk);moves.push_back({disk,source,destination});'
        name = 'transfer' if language=='cpp' else 'Transfer'
        signature = 'int count,int source,int buffer,int destination'
        logic = f'if(count==0)return;{name}(count-1,source,destination,buffer);{operation}{name}(count-1,buffer,source,destination);'
        helper = f'void Transfer({signature}){{{logic}}}Transfer(disks,0,1,2);' if language=='csharp' else f'class Solver {{void Transfer({signature}){{{logic}}}}}new Solver().Transfer(disks,0,1,2);' if language=='java' else f'std::function<void(int,int,int,int)> transfer=[&]({signature}){{{logic}}};transfer(disks,0,1,2);'
        return setup+helper+'return moves;'
    if language == 'python':
        return '''rows = len(screen)
columns = len(screen[0]) if rows else 0
if row < 0 or row >= rows or column < 0 or column >= columns:
    return screen
old_color = screen[row][column]
if old_color == newColor:
    return screen
work = [(row, column)]
screen[row][column] = newColor
while work:
    r, c = work.pop()
    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
        if 0 <= nr < rows and 0 <= nc < columns and screen[nr][nc] == old_color:
            screen[nr][nc] = newColor
            work.append((nr, nc))
return screen'''
    if language == 'javascript':
        return 'const rows=screen.length,columns=rows?screen[0].length:0;if(row<0||row>=rows||column<0||column>=columns)return screen;const oldColor=screen[row][column];if(oldColor===newColor)return screen;const work=[[row,column]];screen[row][column]=newColor;while(work.length){const [r,c]=work.pop();for(const [nr,nc] of [[r-1,c],[r+1,c],[r,c-1],[r,c+1]]){if(nr>=0&&nr<rows&&nc>=0&&nc<columns&&screen[nr][nc]===oldColor){screen[nr][nc]=newColor;work.push([nr,nc]);}}}return screen;'
    rows = 'screen.Length' if language=='csharp' else 'screen.length' if language=='java' else 'static_cast<int>(screen.size())'
    cols = 'screen[0].Length' if language=='csharp' else 'screen[0].length' if language=='java' else 'static_cast<int>(screen[0].size())'
    setup = 'var work=new Stack<(int,int)>();work.Push((row,column));' if language=='csharp' else 'Deque<int[]> work=new ArrayDeque<>();work.push(new int[]{row,column});' if language=='java' else 'std::vector<std::pair<int,int>> work{{row,column}};'
    pop = 'var (r,c)=work.Pop();' if language=='csharp' else 'var cell=work.pop();int r=cell[0],c=cell[1];' if language=='java' else 'auto [r,c]=work.back();work.pop_back();'
    neighbors = 'int dr[]={-1,1,0,0},dc[]={0,0,-1,1};' if language=='cpp' else 'int[] dr={-1,1,0,0},dc={0,0,-1,1};'
    push = 'work.Push((nr,nc));' if language=='csharp' else 'work.push(new int[]{nr,nc});' if language=='java' else 'work.push_back({nr,nc});'
    count = 'work.Count>0' if language=='csharp' else '!work.isEmpty()' if language=='java' else '!work.empty()'
    return f'int rows={rows},columns=rows==0?0:{cols};if(row<0||row>=rows||column<0||column>=columns)return screen;int oldColor=screen[row][column];if(oldColor==newColor)return screen;{setup}screen[row][column]=newColor;{neighbors}while({count}){{{pop}for(int i=0;i<4;++i){{int nr=r+dr[i],nc=c+dc[i];if(nr>=0&&nr<rows&&nc>=0&&nc<columns&&screen[nr][nc]==oldColor){{screen[nr][nc]=newColor;{push}}}}}}}return screen;'
