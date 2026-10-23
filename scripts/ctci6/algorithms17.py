"""Independent six-exercise implementations, matching each runtime's widths."""

def body(ref,language):
    if ref=='17.1':
        if language=='python':return '''mask = 0xffffffff
first &= mask
second &= mask
while second:
    carry = ((first & second) << 1) & mask
    first ^= second
    second = carry
return first if first < 0x80000000 else ~(first ^ mask)'''
        if language=='javascript':return 'while(second!==0){const carry=(first&second)<<1;first^=second;second=carry;}return first;'
        if language=='java':return 'while(second!=0){int carry=(first&second)<<1;first^=second;second=carry;}return first;'
        if language=='csharp':return 'uint a=unchecked((uint)first),b=unchecked((uint)second);while(b!=0){uint carry=(a&b)<<1;a^=b;b=carry;}return unchecked((int)a);'
        return 'auto a=static_cast<std::uint32_t>(first),b=static_cast<std::uint32_t>(second);while(b!=0){std::uint32_t carry=(a&b)<<1;a^=b;b=carry;}std::int32_t result;std::memcpy(&result,&a,sizeof(result));return result;'
    if ref=='17.6':
        if language=='python':return '''total = 0
place = 1
while place <= n:
    high = n // (place * 10)
    digit = (n // place) % 10
    low = n % place
    total += high * place
    if digit == 2:
        total += low + 1
    elif digit > 2:
        total += place
    place *= 10
return total'''
        if language=='javascript':return 'let total=0;for(let place=1;place<=n;place*=10){const high=Math.floor(n/(place*10)),digit=Math.floor(n/place)%10,low=n%place;total+=high*place;if(digit===2)total+=low+1;else if(digit>2)total+=place;}return total;'
        wide='long' if language in ('csharp','java') else 'std::int64_t'
        cast='(int)total' if language in ('csharp','java') else 'static_cast<int>(total)'
        return f'{wide} total=0;for({wide} place=1;place<=n;place*=10){{{wide} high=n/(place*10),digit=(n/place)%10,low=n%place;total+=high*place;if(digit==2)total+=low+1;else if(digit>2)total+=place;}}return {cast};'
    if ref=='17.9':
        if language=='python':return '''values = [1]
third = fifth = seventh = 0
for _ in range(k):
    next_three = values[third] * 3
    next_five = values[fifth] * 5
    next_seven = values[seventh] * 7
    value = min(next_three, next_five, next_seven)
    values.append(value)
    if value == next_three:
        third += 1
    if value == next_five:
        fifth += 1
    if value == next_seven:
        seventh += 1
return values[k]'''
        if language=='javascript':return 'const values=[1];let third=0,fifth=0,seventh=0;for(let i=0;i<k;++i){const a=values[third]*3,b=values[fifth]*5,c=values[seventh]*7,value=Math.min(a,b,c);values.push(value);if(value===a)++third;if(value===b)++fifth;if(value===c)++seventh;}return values[k];'
        allocate='int[] values=new int[k+1];values[0]=1;' if language!='cpp' else 'std::vector<int> values(k+1);values[0]=1;'
        minimum='Math.Min' if language=='csharp' else 'Math.min' if language=='java' else 'std::min'
        return allocate+f'int third=0,fifth=0,seventh=0;for(int i=1;i<=k;++i){{int a=values[third]*3,b=values[fifth]*5,c=values[seventh]*7,value={minimum}(a,{minimum}(b,c));values[i]=value;if(value==a)++third;if(value==b)++fifth;if(value==c)++seventh;}}return values[k];'
    if ref=='17.10':
        if language=='python':return '''candidate = 0
balance = 0
for value in values:
    if balance == 0:
        candidate = value
    balance += 1 if value == candidate else -1
count = sum(value == candidate for value in values)
return [candidate] if count > len(values) // 2 else []'''
        if language=='javascript':return 'let candidate=0,balance=0;for(const value of values){if(balance===0)candidate=value;balance+=value===candidate?1:-1;}let count=0;for(const value of values)if(value===candidate)++count;return count>Math.floor(values.length/2)?[candidate]:[];'
        loop='foreach(int value in values)' if language=='csharp' else 'for(int value:values)'
        size='values.Length' if language=='csharp' else 'values.length' if language=='java' else 'static_cast<int>(values.size())'
        answer='[candidate]' if language=='csharp' else 'new int[]{candidate}' if language=='java' else '{candidate}'
        empty='[]' if language=='csharp' else 'new int[0]' if language=='java' else '{}'
        return f'int candidate=0,balance=0;{loop}{{if(balance==0)candidate=value;balance+=value==candidate?1:-1;}}int count=0;{loop}{{if(value==candidate)++count;}}if(count>{size}/2)return {answer};return {empty};'
    if ref=='17.16':
        if language=='python':return 'one_back = two_back = 0\nfor duration in appointments:\n    current = max(one_back, duration + two_back)\n    two_back = one_back\n    one_back = current\nreturn one_back'
        if language=='javascript':return 'let oneBack=0,twoBack=0;for(const duration of appointments){const current=Math.max(oneBack,duration+twoBack);twoBack=oneBack;oneBack=current;}return oneBack;'
        loop='foreach(int duration in appointments)' if language=='csharp' else 'for(int duration:appointments)'
        maximum='Math.Max' if language=='csharp' else 'Math.max' if language=='java' else 'std::max'
        return f'int oneBack=0,twoBack=0;{loop}{{int current={maximum}(oneBack,duration+twoBack);twoBack=oneBack;oneBack=current;}}return oneBack;'
    if ref=='17.21':
        if language=='python':return '''left, right = 0, len(heights) - 1
left_max = right_max = volume = 0
while left <= right:
    if left_max <= right_max:
        left_max = max(left_max, heights[left])
        volume += left_max - heights[left]
        left += 1
    else:
        right_max = max(right_max, heights[right])
        volume += right_max - heights[right]
        right -= 1
return volume'''
        if language=='javascript':return 'let left=0,right=heights.length-1,leftMax=0,rightMax=0,volume=0;while(left<=right){if(leftMax<=rightMax){leftMax=Math.max(leftMax,heights[left]);volume+=leftMax-heights[left];++left;}else{rightMax=Math.max(rightMax,heights[right]);volume+=rightMax-heights[right];--right;}}return volume;'
        size='heights.Length' if language=='csharp' else 'heights.length' if language=='java' else 'static_cast<int>(heights.size())'
        maximum='Math.Max' if language=='csharp' else 'Math.max' if language=='java' else 'std::max'
        return f'int left=0,right={size}-1,leftMax=0,rightMax=0,volume=0;while(left<=right){{if(leftMax<=rightMax){{leftMax={maximum}(leftMax,heights[left]);volume+=leftMax-heights[left];++left;}}else{{rightMax={maximum}(rightMax,heights[right]);volume+=rightMax-heights[right];--right;}}}}return volume;'
    raise ValueError(ref)

_previous_body=body

def body(ref,language):
    if ref not in ('17.5','17.14','17.18','17.19','17.23','17.24'):
        return _previous_body(ref,language)
    if ref=='17.5':
        if language=='python':return '''n = len(text)
first = [-2] * (2 * n + 1)
first[n] = -1
balance = best = 0
start = end = -1
for index, char in enumerate(text):
    balance += -1 if '0' <= char <= '9' else 1
    slot = balance + n
    if first[slot] == -2:
        first[slot] = index
    elif index - first[slot] > best:
        best = index - first[slot]
        start, end = first[slot] + 1, index
return [start, end]'''
        if language=='javascript':return 'const n=text.length,first=Array(2*n+1).fill(-2);first[n]=-1;let balance=0,best=0,start=-1,end=-1;for(let i=0;i<n;++i){balance+=text[i]>="0"&&text[i]<="9"?-1:1;const slot=balance+n;if(first[slot]===-2)first[slot]=i;else if(i-first[slot]>best){best=i-first[slot];start=first[slot]+1;end=i;}}return [start,end];'
        size='text.Length' if language=='csharp' else 'text.length()' if language=='java' else 'static_cast<int>(text.size())'
        setup='int[] first=new int[2*n+1];Array.Fill(first,-2);' if language=='csharp' else 'int[] first=new int[2*n+1];Arrays.fill(first,-2);' if language=='java' else 'std::vector<int> first(2*n+1,-2);'
        char='text.charAt(i)' if language=='java' else 'text[i]'
        result='[start,end]' if language=='csharp' else 'new int[]{start,end}' if language=='java' else '{start,end}'
        return f'int n={size};{setup}first[n]=-1;int balance=0,best=0,start=-1,end=-1;for(int i=0;i<n;++i){{balance+=({char}>=\'0\'&&{char}<=\'9\')?-1:1;int slot=balance+n;if(first[slot]==-2)first[slot]=i;else if(i-first[slot]>best){{best=i-first[slot];start=first[slot]+1;end=i;}}}}return {result};'
    if ref=='17.14':
        if language=='python':return '''if k == 0:
    return []
import heapq
heap = [-values[i] for i in range(k)]
heapq.heapify(heap)
for index in range(k, len(values)):
    value = values[index]
    if value < -heap[0]:
        heapq.heapreplace(heap, -value)
return sorted(-value for value in heap)'''
        if language=='javascript':return '''if(k===0)return [];const heap=values.slice(0,k);function down(index){while(true){let child=2*index+1;if(child>=heap.length)return;if(child+1<heap.length&&heap[child+1]>heap[child])++child;if(heap[index]>=heap[child])return;[heap[index],heap[child]]=[heap[child],heap[index]];index=child;}}for(let i=Math.floor(k/2)-1;i>=0;--i)down(i);for(let i=k;i<values.length;++i){if(values[i]<heap[0]){heap[0]=values[i];down(0);}}heap.sort((a,b)=>a-b);return heap;'''
        if language=='cpp':return 'if(k==0)return {};std::vector<int> heap(values.begin(),values.begin()+k);std::make_heap(heap.begin(),heap.end());for(int i=k;i<static_cast<int>(values.size());++i){if(values[i]<heap.front()){std::pop_heap(heap.begin(),heap.end());heap.back()=values[i];std::push_heap(heap.begin(),heap.end());}}std::sort_heap(heap.begin(),heap.end());return heap;'
        if language=='csharp':return 'if(k==0)return [];var heap=new PriorityQueue<int,int>(Comparer<int>.Create((a,b)=>b.CompareTo(a)));for(int i=0;i<k;++i)heap.Enqueue(values[i],values[i]);for(int i=k;i<values.Length;++i){if(values[i]<heap.Peek()){heap.Dequeue();heap.Enqueue(values[i],values[i]);}}int[] result=new int[k];for(int i=k-1;i>=0;--i)result[i]=heap.Dequeue();return result;'
        return 'if(k==0)return new int[0];var heap=new PriorityQueue<Integer>(Comparator.reverseOrder());for(int i=0;i<k;++i)heap.add(values[i]);for(int i=k;i<values.length;++i){if(values[i]<heap.peek()){heap.remove();heap.add(values[i]);}}int[] result=new int[k];for(int i=k-1;i>=0;--i)result[i]=heap.remove();return result;'
    if ref=='17.18':
        if language=='python':return '''if not small:
    return [-1, -1]
counts = {value: 0 for value in small}
missing = len(small)
left = 0
best_start = best_end = -1
for right, value in enumerate(big):
    if value in counts:
        if counts[value] == 0:
            missing -= 1
        counts[value] += 1
    while missing == 0:
        if best_start == -1 or right - left < best_end - best_start:
            best_start, best_end = left, right
        removed = big[left]
        if removed in counts:
            counts[removed] -= 1
            if counts[removed] == 0:
                missing += 1
        left += 1
return [best_start, best_end]'''
        if language=='javascript':return 'if(small.length===0)return [-1,-1];const counts=new Map(small.map(v=>[v,0]));let missing=small.length,left=0,start=-1,end=-1;for(let right=0;right<big.length;++right){const value=big[right];if(counts.has(value)){if(counts.get(value)===0)--missing;counts.set(value,counts.get(value)+1);}while(missing===0){if(start===-1||right-left<end-start){start=left;end=right;}const removed=big[left];if(counts.has(removed)){counts.set(removed,counts.get(removed)-1);if(counts.get(removed)===0)++missing;}++left;}}return [start,end];'
        smallsize='small.Length' if language=='csharp' else 'small.length' if language=='java' else 'static_cast<int>(small.size())'
        bigsize='big.Length' if language=='csharp' else 'big.length' if language=='java' else 'static_cast<int>(big.size())'
        make=lambda a,b:'['+a+','+b+']' if language=='csharp' else 'new int[]{'+a+','+b+'}' if language=='java' else '{'+a+','+b+'}'
        setup='var counts=new Dictionary<int,int>();foreach(int value in small)counts[value]=0;' if language=='csharp' else 'Map<Integer,Integer> counts=new HashMap<>();for(int value:small)counts.put(value,0);' if language=='java' else 'std::unordered_map<int,int> counts;for(int value:small)counts[value]=0;'
        has=lambda value:'counts.ContainsKey('+value+')' if language=='csharp' else 'counts.containsKey('+value+')' if language=='java' else 'counts.find('+value+')!=counts.end()'
        get=lambda value:'counts.get('+value+')' if language=='java' else 'counts['+value+']'
        add='counts.put(value,counts.get(value)+1);' if language=='java' else '++counts[value];'
        remove='counts.put(removed,counts.get(removed)-1);' if language=='java' else '--counts[removed];'
        return f'if({smallsize}==0)return {make("-1","-1")};{setup}int missing={smallsize},left=0,start=-1,end=-1;for(int right=0;right<{bigsize};++right){{int value=big[right];if({has("value")}){{if({get("value")}==0)--missing;{add}}}while(missing==0){{if(start==-1||right-left<end-start){{start=left;end=right;}}int removed=big[left];if({has("removed")}){{{remove}if({get("removed")}==0)++missing;}}++left;}}}}return {make("start","end")};'
    if ref=='17.19':
        if language=='python':return '''n = len(values) + 2
combined = 0
for value in range(1, n + 1):
    combined ^= value
for value in values:
    combined ^= value
bit = combined & -combined
first = second = 0
for value in range(1, n + 1):
    if value & bit:
        first ^= value
    else:
        second ^= value
for value in values:
    if value & bit:
        first ^= value
    else:
        second ^= value
return [min(first, second), max(first, second)]'''
        if language=='javascript':return 'const n=values.length+2;let combined=0;for(let value=1;value<=n;++value)combined^=value;for(const value of values)combined^=value;const bit=combined&-combined;let first=0,second=0;for(let value=1;value<=n;++value){if(value&bit)first^=value;else second^=value;}for(const value of values){if(value&bit)first^=value;else second^=value;}return [Math.min(first,second),Math.max(first,second)];'
        size='values.Length' if language=='csharp' else 'values.length' if language=='java' else 'static_cast<int>(values.size())'
        loop='foreach(int value in values)' if language=='csharp' else 'for(int value:values)'
        minimum='Math.Min' if language=='csharp' else 'Math.min' if language=='java' else 'std::min'
        maximum='Math.Max' if language=='csharp' else 'Math.max' if language=='java' else 'std::max'
        result=f'[{minimum}(first,second),{maximum}(first,second)]' if language=='csharp' else f'new int[]{{{minimum}(first,second),{maximum}(first,second)}}' if language=='java' else f'{{{minimum}(first,second),{maximum}(first,second)}}'
        return f'int n={size}+2,combined=0;for(int value=1;value<=n;++value)combined^=value;{loop}combined^=value;int bit=combined&-combined,first=0,second=0;for(int value=1;value<=n;++value){{if((value&bit)!=0)first^=value;else second^=value;}}{loop}{{if((value&bit)!=0)first^=value;else second^=value;}}return {result};'
    if ref=='17.23':
        if language=='python':return '''n = len(matrix)
right = [[0] * n for _ in range(n)]
down = [[0] * n for _ in range(n)]
for row in range(n - 1, -1, -1):
    for column in range(n - 1, -1, -1):
        if matrix[row][column] == 0:
            right[row][column] = 1 + (right[row][column + 1] if column + 1 < n else 0)
            down[row][column] = 1 + (down[row + 1][column] if row + 1 < n else 0)
for size in range(n, 0, -1):
    for row in range(n - size + 1):
        for column in range(n - size + 1):
            if right[row][column] >= size and down[row][column] >= size and right[row + size - 1][column] >= size and down[row][column + size - 1] >= size:
                return [row, column, size]
return []'''
        if language=='javascript':return 'const n=matrix.length,right=Array.from({length:n},()=>Array(n).fill(0)),down=Array.from({length:n},()=>Array(n).fill(0));for(let r=n-1;r>=0;--r){for(let c=n-1;c>=0;--c){if(matrix[r][c]===0){right[r][c]=1+(c+1<n?right[r][c+1]:0);down[r][c]=1+(r+1<n?down[r+1][c]:0);}}}for(let size=n;size>=1;--size){for(let r=0;r+size<=n;++r){for(let c=0;c+size<=n;++c){if(right[r][c]>=size&&down[r][c]>=size&&right[r+size-1][c]>=size&&down[r][c+size-1]>=size)return [r,c,size];}}}return [];'
        size='matrix.Length' if language=='csharp' else 'matrix.length' if language=='java' else 'static_cast<int>(matrix.size())'
        allocate='int[,] right=new int[n,n],down=new int[n,n];' if language=='csharp' else 'int[][] right=new int[n][n],down=new int[n][n];' if language=='java' else 'std::vector<std::vector<int>> right(n,std::vector<int>(n)),down(n,std::vector<int>(n));'
        at=lambda name,r,c:f'{name}[{r},{c}]' if language=='csharp' else f'{name}[{r}][{c}]'
        result='[r,c,size]' if language=='csharp' else 'new int[]{r,c,size}' if language=='java' else '{r,c,size}'
        empty='[]' if language=='csharp' else 'new int[0]' if language=='java' else '{}'
        return f'int n={size};{allocate}for(int r=n-1;r>=0;--r){{for(int c=n-1;c>=0;--c){{if(matrix[r][c]==0){{{at("right","r","c")}=1+(c+1<n?{at("right","r","c+1")}:0);{at("down","r","c")}=1+(r+1<n?{at("down","r+1","c")}:0);}}}}}}for(int size=n;size>=1;--size){{for(int r=0;r+size<=n;++r){{for(int c=0;c+size<=n;++c){{if({at("right","r","c")}>=size&&{at("down","r","c")}>=size&&{at("right","r+size-1","c")}>=size&&{at("down","r","c+size-1")}>=size)return {result};}}}}}}return {empty};'
    if language=='python':return '''rows = len(matrix)
columns = len(matrix[0]) if rows else 0
if not rows or not columns:
    return []
best = -2147483648
answer = []
for top in range(rows):
    totals = [0] * columns
    for bottom in range(top, rows):
        running = start = 0
        for column in range(columns):
            totals[column] += matrix[bottom][column]
            if running < 0:
                running = totals[column]
                start = column
            else:
                running += totals[column]
            if running > best:
                best = running
                answer = [best, top, start, bottom, column]
return answer'''
    if language=='javascript':return 'const rows=matrix.length,columns=rows?matrix[0].length:0;if(!rows||!columns)return [];let best=-2147483648,answer=[];for(let top=0;top<rows;++top){const totals=Array(columns).fill(0);for(let bottom=top;bottom<rows;++bottom){let running=0,start=0;for(let c=0;c<columns;++c){totals[c]+=matrix[bottom][c];if(running<0){running=totals[c];start=c;}else running+=totals[c];if(running>best){best=running;answer=[best,top,start,bottom,c];}}}}return answer;'
    rows='matrix.Length' if language=='csharp' else 'matrix.length' if language=='java' else 'static_cast<int>(matrix.size())'
    cols='matrix[0].Length' if language=='csharp' else 'matrix[0].length' if language=='java' else 'static_cast<int>(matrix[0].size())'
    empty='[]' if language=='csharp' else 'new int[0]' if language=='java' else '{}'
    allocate='int[] answer=new int[5];' if language!='cpp' else 'std::vector<int> answer(5);'
    totals='int[] totals=new int[columns];' if language!='cpp' else 'std::vector<int> totals(columns);'
    result='[best,top,start,bottom,c]' if language=='csharp' else 'new int[]{best,top,start,bottom,c}' if language=='java' else '{best,top,start,bottom,c}'
    return f'int rows={rows},columns=rows==0?0:{cols};if(rows==0||columns==0)return {empty};int best=-2147483648;{allocate}for(int top=0;top<rows;++top){{{totals}for(int bottom=top;bottom<rows;++bottom){{int running=0,start=0;for(int c=0;c<columns;++c){{totals[c]+=matrix[bottom][c];if(running<0){{running=totals[c];start=c;}}else running+=totals[c];if(running>best){{best=running;answer={result};}}}}}}}}return answer;'

_previous_text_body=body

def body(ref,language):
    if ref=='17.11':
        if language=='python':return '''last_first = last_second = -1
best = len(words) + 1
for index, word in enumerate(words):
    if word == first:
        last_first = index
        if last_second >= 0:
            best = min(best, index - last_second)
    elif word == second:
        last_second = index
        if last_first >= 0:
            best = min(best, index - last_first)
return -1 if best == len(words) + 1 else best'''
        if language=='javascript':return 'let lastFirst=-1,lastSecond=-1,best=words.length+1;for(let i=0;i<words.length;++i){if(words[i]===first){lastFirst=i;if(lastSecond>=0)best=Math.min(best,i-lastSecond);}else if(words[i]===second){lastSecond=i;if(lastFirst>=0)best=Math.min(best,i-lastFirst);}}return best===words.length+1?-1:best;'
        size='words.Length' if language=='csharp' else 'words.length' if language=='java' else 'static_cast<int>(words.size())';match=lambda q:'words[i].equals('+q+')' if language=='java' else 'words[i]=='+q;minimum='Math.Min' if language=='csharp' else 'Math.min' if language=='java' else 'std::min'
        return f'int lastFirst=-1,lastSecond=-1,best={size}+1;for(int i=0;i<{size};++i){{if({match("first")}){{lastFirst=i;if(lastSecond>=0)best={minimum}(best,i-lastSecond);}}else if({match("second")}){{lastSecond=i;if(lastFirst>=0)best={minimum}(best,i-lastFirst);}}}}return best=={size}+1?-1:best;'
    if ref=='17.15':
        if language=='python':return '''dictionary = set(words)
best = ""
for word in words:
    dp = [-1] * (len(word) + 1)
    dp[0] = 0
    for end in range(1, len(word) + 1):
        for start in range(end):
            if dp[start] >= 0 and word[start:end] in dictionary:
                dp[end] = max(dp[end], dp[start] + 1)
    if dp[-1] >= 2 and (len(word) > len(best) or (len(word) == len(best) and word < best)):
        best = word
return best'''
        if language=='javascript':return 'const dictionary=new Set(words);let best="";for(const word of words){const dp=new Array(word.length+1).fill(-1);dp[0]=0;for(let end=1;end<=word.length;++end)for(let start=0;start<end;++start)if(dp[start]>=0&&dictionary.has(word.slice(start,end)))dp[end]=Math.max(dp[end],dp[start]+1);if(dp[word.length]>=2&&(word.length>best.length||(word.length===best.length&&word<best)))best=word;}return best;'
        if language=='cpp':return 'std::unordered_set<std::string> dictionary(words.begin(),words.end());std::string best;for(const auto& word:words){int n=static_cast<int>(word.size());std::vector<int> dp(n+1,-1);dp[0]=0;for(int end=1;end<=n;++end)for(int start=0;start<end;++start)if(dp[start]>=0&&dictionary.count(word.substr(start,end-start)))dp[end]=std::max(dp[end],dp[start]+1);if(dp[n]>=2&&(word.size()>best.size()||(word.size()==best.size()&&word<best)))best=word;}return best;'
        if language=='csharp':return 'var dictionary=new HashSet<string>(words,StringComparer.Ordinal);string best="";foreach(string word in words){int[] dp=new int[word.Length+1];Array.Fill(dp,-1);dp[0]=0;for(int end=1;end<=word.Length;++end)for(int start=0;start<end;++start)if(dp[start]>=0&&dictionary.Contains(word.Substring(start,end-start)))dp[end]=Math.Max(dp[end],dp[start]+1);if(dp[word.Length]>=2&&(word.Length>best.Length||(word.Length==best.Length&&StringComparer.Ordinal.Compare(word,best)<0)))best=word;}return best;'
        return 'Set<String> dictionary=new HashSet<>(Arrays.asList(words));String best="";for(String word:words){int[] dp=new int[word.length()+1];Arrays.fill(dp,-1);dp[0]=0;for(int end=1;end<=word.length();++end)for(int start=0;start<end;++start)if(dp[start]>=0&&dictionary.contains(word.substring(start,end)))dp[end]=Math.max(dp[end],dp[start]+1);if(dp[word.length()]>=2&&(word.length()>best.length()||(word.length()==best.length()&&word.compareTo(best)<0)))best=word;}return best;'
    if ref=='17.17':
        if language=='python':return '''result = []
for pattern in patterns:
    positions = []
    for start in range(len(text) - len(pattern) + 1):
        if text.startswith(pattern, start):
            positions.append(start)
    result.append(positions)
return result'''
        if language=='javascript':return 'const result=[];for(const pattern of patterns){const positions=[];for(let start=0;start+pattern.length<=text.length;++start)if(text.startsWith(pattern,start))positions.push(start);result.push(positions);}return result;'
        if language=='cpp':return 'std::vector<std::vector<int>> result;for(const auto& pattern:patterns){std::vector<int> positions;int limit=static_cast<int>(text.size())-static_cast<int>(pattern.size());for(int start=0;start<=limit;++start)if(text.compare(start,pattern.size(),pattern)==0)positions.push_back(start);result.push_back(std::move(positions));}return result;'
        if language=='csharp':return 'var result=new List<int[]>();foreach(string pattern in patterns){var positions=new List<int>();for(int start=0;start+pattern.Length<=text.Length;++start)if(string.CompareOrdinal(text,start,pattern,0,pattern.Length)==0)positions.Add(start);result.Add(positions.ToArray());}return result.ToArray();'
        return 'List<int[]> result=new ArrayList<>();for(String pattern:patterns){List<Integer> positions=new ArrayList<>();for(int start=0;start+pattern.length()<=text.length();++start)if(text.startsWith(pattern,start))positions.add(start);int[] row=new int[positions.size()];for(int i=0;i<row.length;++i)row[i]=positions.get(i);result.add(row);}return result.toArray(new int[0][]);'
    return _previous_text_body(ref,language)
