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

_previous_structured_body=body

def body(ref,language):
    if ref=='17.8':
        if language=='python':return '''if not people:
    return []
order = sorted(range(len(people)), key=lambda i: (people[i][0], people[i][1], i))
length = [1] * len(order)
previous = [-1] * len(order)
best = 0
for i in range(len(order)):
    for j in range(i):
        a, b = people[order[j]], people[order[i]]
        if a[0] < b[0] and a[1] < b[1] and length[j] + 1 > length[i]:
            length[i] = length[j] + 1
            previous[i] = j
    if length[i] > length[best]:
        best = i
result = []
while best != -1:
    result.append(order[best])
    best = previous[best]
result.reverse()
return result'''
        if language=='javascript':return 'if(people.length===0)return [];const order=Array.from({length:people.length},(_,i)=>i).sort((a,b)=>people[a][0]-people[b][0]||people[a][1]-people[b][1]||a-b),length=new Array(order.length).fill(1),previous=new Array(order.length).fill(-1);let best=0;for(let i=0;i<order.length;++i){for(let j=0;j<i;++j){const a=people[order[j]],b=people[order[i]];if(a[0]<b[0]&&a[1]<b[1]&&length[j]+1>length[i]){length[i]=length[j]+1;previous[i]=j;}}if(length[i]>length[best])best=i;}const result=[];while(best!==-1){result.push(order[best]);best=previous[best];}return result.reverse();'
        if language=='cpp':return 'int n=static_cast<int>(people.size());if(n==0)return {};std::vector<int> order(n),length(n,1),previous(n,-1);for(int i=0;i<n;++i)order[i]=i;std::sort(order.begin(),order.end(),[&](int a,int b){if(people[a][0]!=people[b][0])return people[a][0]<people[b][0];if(people[a][1]!=people[b][1])return people[a][1]<people[b][1];return a<b;});int best=0;for(int i=0;i<n;++i){for(int j=0;j<i;++j)if(people[order[j]][0]<people[order[i]][0]&&people[order[j]][1]<people[order[i]][1]&&length[j]+1>length[i]){length[i]=length[j]+1;previous[i]=j;}if(length[i]>length[best])best=i;}std::vector<int> result;for(int at=best;at!=-1;at=previous[at])result.push_back(order[at]);std::reverse(result.begin(),result.end());return result;'
        if language=='csharp':return 'int n=people.Length;if(n==0)return [];int[] order=new int[n],length=new int[n],previous=new int[n];for(int i=0;i<n;++i)order[i]=i;Array.Sort(order,(a,b)=>{int height=people[a][0].CompareTo(people[b][0]);if(height!=0)return height;int weight=people[a][1].CompareTo(people[b][1]);return weight!=0?weight:a.CompareTo(b);});Array.Fill(length,1);Array.Fill(previous,-1);int best=0;for(int i=0;i<n;++i){for(int j=0;j<i;++j)if(people[order[j]][0]<people[order[i]][0]&&people[order[j]][1]<people[order[i]][1]&&length[j]+1>length[i]){length[i]=length[j]+1;previous[i]=j;}if(length[i]>length[best])best=i;}var result=new List<int>();for(int at=best;at!=-1;at=previous[at])result.Add(order[at]);result.Reverse();return result.ToArray();'
        return 'int n=people.length;if(n==0)return new int[0];Integer[] order=new Integer[n];int[] length=new int[n],previous=new int[n];for(int i=0;i<n;++i)order[i]=i;Arrays.sort(order,(a,b)->{int height=Integer.compare(people[a][0],people[b][0]);if(height!=0)return height;int weight=Integer.compare(people[a][1],people[b][1]);return weight!=0?weight:Integer.compare(a,b);});Arrays.fill(length,1);Arrays.fill(previous,-1);int best=0;for(int i=0;i<n;++i){for(int j=0;j<i;++j)if(people[order[j]][0]<people[order[i]][0]&&people[order[j]][1]<people[order[i]][1]&&length[j]+1>length[i]){length[i]=length[j]+1;previous[i]=j;}if(length[i]>length[best])best=i;}int[] result=new int[length[best]];for(int at=result.length-1;at>=0;--at){result[at]=order[best];best=previous[best];}return result;'
    if ref=='17.13':
        if language=='python':return '''words = set(dictionary)
maximum = max(map(len, words), default=0)
cost = [0] * (len(text) + 1)
previous = [0] * (len(text) + 1)
for end in range(1, len(text) + 1):
    cost[end] = cost[end - 1] + 1
    previous[end] = end - 1
    for length in range(1, min(maximum, end) + 1):
        start = end - length
        if text[start:end] in words and cost[start] < cost[end]:
            cost[end] = cost[start]
            previous[end] = start
result = []
end = len(text)
while end:
    result.append(text[previous[end]:end])
    end = previous[end]
result.reverse()
return result'''
        if language=='javascript':return 'const words=new Set(dictionary);let maximum=0;for(const word of words)maximum=Math.max(maximum,word.length);const cost=new Array(text.length+1).fill(0),previous=new Array(text.length+1).fill(0);for(let end=1;end<=text.length;++end){cost[end]=cost[end-1]+1;previous[end]=end-1;for(let length=1;length<=maximum&&length<=end;++length){const start=end-length;if(words.has(text.slice(start,end))&&cost[start]<cost[end]){cost[end]=cost[start];previous[end]=start;}}}const result=[];for(let end=text.length;end>0;end=previous[end])result.push(text.slice(previous[end],end));return result.reverse();'
        if language=='cpp':return 'std::unordered_set<std::string> words(dictionary.begin(),dictionary.end());int maximum=0;for(const auto& word:words)maximum=std::max(maximum,static_cast<int>(word.size()));int n=static_cast<int>(text.size());std::vector<int> cost(n+1,0),previous(n+1,0);for(int end=1;end<=n;++end){cost[end]=cost[end-1]+1;previous[end]=end-1;for(int length=1;length<=maximum&&length<=end;++length){int start=end-length;if(words.count(text.substr(start,length))&&cost[start]<cost[end]){cost[end]=cost[start];previous[end]=start;}}}std::vector<std::string> result;for(int end=n;end>0;end=previous[end])result.push_back(text.substr(previous[end],end-previous[end]));std::reverse(result.begin(),result.end());return result;'
        if language=='csharp':return 'var words=new HashSet<string>(dictionary,StringComparer.Ordinal);int maximum=0;foreach(string word in words)maximum=Math.Max(maximum,word.Length);int[] cost=new int[text.Length+1],previous=new int[text.Length+1];for(int end=1;end<=text.Length;++end){cost[end]=cost[end-1]+1;previous[end]=end-1;for(int length=1;length<=maximum&&length<=end;++length){int start=end-length;if(words.Contains(text.Substring(start,length))&&cost[start]<cost[end]){cost[end]=cost[start];previous[end]=start;}}}var result=new List<string>();for(int end=text.Length;end>0;end=previous[end])result.Add(text.Substring(previous[end],end-previous[end]));result.Reverse();return result;'
        return 'Set<String> words=new HashSet<>(Arrays.asList(dictionary));int maximum=0;for(String word:words)maximum=Math.max(maximum,word.length());int[] cost=new int[text.length()+1],previous=new int[text.length()+1];for(int end=1;end<=text.length();++end){cost[end]=cost[end-1]+1;previous[end]=end-1;for(int length=1;length<=maximum&&length<=end;++length){int start=end-length;if(words.contains(text.substring(start,end))&&cost[start]<cost[end]){cost[end]=cost[start];previous[end]=start;}}}List<String> result=new ArrayList<>();for(int end=text.length();end>0;end=previous[end])result.add(text.substring(previous[end],end));Collections.reverse(result);return result;'
    if ref=='17.22':
        if language=='python':return '''words = set(dictionary)
previous = {start: None}
queue = [start]
head = 0
while head < len(queue):
    word = queue[head]
    head += 1
    if word == stop:
        path = []
        current = stop
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path
    for position in range(len(word)):
        for letter in "abcdefghijklmnopqrstuvwxyz":
            if letter == word[position]:
                continue
            candidate = word[:position] + letter + word[position + 1:]
            if candidate in words and candidate not in previous:
                previous[candidate] = word
                queue.append(candidate)
return []'''
        if language=='javascript':return 'const words=new Set(dictionary),previous=new Map([[start,null]]),queue=[start];for(let head=0;head<queue.length;++head){const word=queue[head];if(word===stop){const path=[];for(let current=stop;current!==null;current=previous.get(current))path.push(current);return path.reverse();}for(let position=0;position<word.length;++position)for(let code=97;code<=122;++code){const letter=String.fromCharCode(code);if(letter===word[position])continue;const candidate=word.slice(0,position)+letter+word.slice(position+1);if(words.has(candidate)&&!previous.has(candidate)){previous.set(candidate,word);queue.push(candidate);}}}return [];'
        if language=='cpp':return 'std::unordered_set<std::string> words(dictionary.begin(),dictionary.end());std::unordered_map<std::string,std::string> previous{{start,""}};std::vector<std::string> queue{start};for(size_t head=0;head<queue.size();++head){std::string word=queue[head];if(word==stop){std::vector<std::string> path;for(std::string current=stop;!current.empty();current=previous.at(current))path.push_back(current);std::reverse(path.begin(),path.end());return path;}for(size_t position=0;position<word.size();++position){std::string candidate=word;for(char letter=\'a\';letter<=\'z\';++letter){if(letter==word[position])continue;candidate[position]=letter;if(words.count(candidate)&&!previous.count(candidate)){previous[candidate]=word;queue.push_back(candidate);}}}}return {};'
        if language=='csharp':return 'var words=new HashSet<string>(dictionary,StringComparer.Ordinal);var previous=new Dictionary<string,string?>(StringComparer.Ordinal){{start,null}};var queue=new List<string>{start};for(int head=0;head<queue.Count;++head){string word=queue[head];if(word==stop){var path=new List<string>();for(string? current=stop;current!=null;current=previous[current])path.Add(current);path.Reverse();return path;}char[] letters=word.ToCharArray();for(int position=0;position<letters.Length;++position){char original=letters[position];for(char letter=\'a\';letter<=\'z\';++letter){if(letter==original)continue;letters[position]=letter;string candidate=new string(letters);if(words.Contains(candidate)&&!previous.ContainsKey(candidate)){previous[candidate]=word;queue.Add(candidate);}}letters[position]=original;}}return [];'
        return 'Set<String> words=new HashSet<>(Arrays.asList(dictionary));Map<String,String> previous=new HashMap<>();previous.put(start,null);List<String> queue=new ArrayList<>();queue.add(start);for(int head=0;head<queue.size();++head){String word=queue.get(head);if(word.equals(stop)){List<String> path=new ArrayList<>();for(String current=stop;current!=null;current=previous.get(current))path.add(current);Collections.reverse(path);return path;}char[] letters=word.toCharArray();for(int position=0;position<letters.length;++position){char original=letters[position];for(char letter=\'a\';letter<=\'z\';++letter){if(letter==original)continue;letters[position]=letter;String candidate=new String(letters);if(words.contains(candidate)&&!previous.containsKey(candidate)){previous.put(candidate,word);queue.add(candidate);}}letters[position]=original;}}return new ArrayList<>();'
    if ref=='17.26':
        if language=='python':return '''n = len(documentIds)
postings = {}
for index, document in enumerate(documents):
    for word in document:
        postings.setdefault(word, []).append(index)
intersections = {}
for posting in postings.values():
    for left in range(len(posting)):
        for right in range(left + 1, len(posting)):
            key = posting[left] * n + posting[right]
            intersections[key] = intersections.get(key, 0) + 1
result = []
for key, count in intersections.items():
    left, right = divmod(key, n)
    a, b = sorted((documentIds[left], documentIds[right]))
    result.append([a, b, count, len(documents[left]) + len(documents[right]) - count])
result.sort()
return result'''
        if language=='javascript':return 'const n=documentIds.length,postings=new Map(),intersections=new Map();for(let i=0;i<n;++i)for(const word of documents[i]){if(!postings.has(word))postings.set(word,[]);postings.get(word).push(i);}for(const posting of postings.values())for(let left=0;left<posting.length;++left)for(let right=left+1;right<posting.length;++right){const key=posting[left]*n+posting[right];intersections.set(key,(intersections.get(key)||0)+1);}const result=[];for(const [key,count] of intersections){const left=Math.floor(key/n),right=key%n,a=documentIds[left],b=documentIds[right];result.push([Math.min(a,b),Math.max(a,b),count,documents[left].length+documents[right].length-count]);}result.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);return result;'
        if language=='cpp':return 'int n=static_cast<int>(documentIds.size());std::unordered_map<int,std::vector<int>> postings;for(int i=0;i<n;++i)for(int word:documents[i])postings[word].push_back(i);std::unordered_map<int,int> intersections;for(const auto& entry:postings){const auto& posting=entry.second;for(size_t a=0;a<posting.size();++a)for(size_t b=a+1;b<posting.size();++b)++intersections[posting[a]*n+posting[b]];}std::vector<std::vector<int>> result;for(const auto& entry:intersections){int left=entry.first/n,right=entry.first%n,count=entry.second,a=documentIds[left],b=documentIds[right];result.push_back({std::min(a,b),std::max(a,b),count,static_cast<int>(documents[left].size()+documents[right].size())-count});}std::sort(result.begin(),result.end());return result;'
        if language=='csharp':return 'int n=documentIds.Length;var postings=new Dictionary<int,List<int>>();for(int i=0;i<n;++i)foreach(int word in documents[i]){if(!postings.TryGetValue(word,out var posting)){posting=new List<int>();postings[word]=posting;}posting.Add(i);}var intersections=new Dictionary<int,int>();foreach(var posting in postings.Values)for(int a=0;a<posting.Count;++a)for(int b=a+1;b<posting.Count;++b){int key=posting[a]*n+posting[b];intersections.TryGetValue(key,out int count);intersections[key]=count+1;}var result=new List<int[]>();foreach(var entry in intersections){int left=entry.Key/n,right=entry.Key%n,count=entry.Value,a=documentIds[left],b=documentIds[right];result.Add([Math.Min(a,b),Math.Max(a,b),count,documents[left].Length+documents[right].Length-count]);}result.Sort((a,b)=>{int first=a[0].CompareTo(b[0]);return first!=0?first:a[1].CompareTo(b[1]);});return result.ToArray();'
        return 'int n=documentIds.length;Map<Integer,List<Integer>> postings=new HashMap<>();for(int i=0;i<n;++i)for(int word:documents[i])postings.computeIfAbsent(word,k->new ArrayList<>()).add(i);Map<Integer,Integer> intersections=new HashMap<>();for(List<Integer> posting:postings.values())for(int a=0;a<posting.size();++a)for(int b=a+1;b<posting.size();++b){int key=posting.get(a)*n+posting.get(b);intersections.put(key,intersections.getOrDefault(key,0)+1);}List<int[]> result=new ArrayList<>();for(var entry:intersections.entrySet()){int left=entry.getKey()/n,right=entry.getKey()%n,count=entry.getValue(),a=documentIds[left],b=documentIds[right];result.add(new int[]{Math.min(a,b),Math.max(a,b),count,documents[left].length+documents[right].length-count});}result.sort((a,b)->{int first=Integer.compare(a[0],b[0]);return first!=0?first:Integer.compare(a[1],b[1]);});return result.toArray(new int[0][]);'
    if ref!='17.25':return _previous_structured_body(ref,language)
    if language=='python':return '''groups = {}
seen = set()
maximum = 0
for word in words:
    if word not in seen:
        seen.add(word)
        groups.setdefault(len(word), []).append(word)
        maximum = max(maximum, len(word))
for area in range(maximum * maximum, 0, -1):
    for height in range(1, maximum + 1):
        if area % height:
            continue
        width = area // height
        if width not in groups or height not in groups:
            continue
        prefixes = {word[:length] for word in groups[height] for length in range(1, height + 1)}
        rows = []
        def search():
            if len(rows) == height:
                return True
            for word in groups[width]:
                rows.append(word)
                if all("".join(row[column] for row in rows) in prefixes for column in range(width)) and search():
                    return True
                rows.pop()
            return False
        if search():
            return rows
return []'''
    if language=='javascript':return 'const groups=new Map(),seen=new Set();let maximum=0;for(const word of words)if(!seen.has(word)){seen.add(word);if(!groups.has(word.length))groups.set(word.length,[]);groups.get(word.length).push(word);maximum=Math.max(maximum,word.length);}for(let area=maximum*maximum;area>0;--area)for(let height=1;height<=maximum;++height){if(area%height!==0)continue;const width=area/height;if(!groups.has(width)||!groups.has(height))continue;const prefixes=new Set();for(const word of groups.get(height))for(let length=1;length<=height;++length)prefixes.add(word.slice(0,length));const rows=[];function search(){if(rows.length===height)return true;for(const word of groups.get(width)){rows.push(word);let valid=true;for(let column=0;column<width;++column){let prefix="";for(const row of rows)prefix+=row[column];if(!prefixes.has(prefix)){valid=false;break;}}if(valid&&search())return true;rows.pop();}return false;}if(search())return rows;}return [];'
    if language=='cpp':return 'std::unordered_set<std::string> seen;std::vector<std::vector<std::string>> groups(6);int maximum=0;for(const auto& word:words)if(seen.insert(word).second){groups[word.size()].push_back(word);maximum=std::max(maximum,static_cast<int>(word.size()));}for(int area=maximum*maximum;area>0;--area)for(int height=1;height<=maximum;++height){if(area%height!=0)continue;int width=area/height;if(width>maximum||groups[width].empty()||groups[height].empty())continue;std::unordered_set<std::string> prefixes;for(const auto& word:groups[height])for(int length=1;length<=height;++length)prefixes.insert(word.substr(0,length));std::vector<std::string> rows;std::function<bool()> search=[&](){if(static_cast<int>(rows.size())==height)return true;for(const auto& word:groups[width]){rows.push_back(word);bool valid=true;for(int column=0;column<width;++column){std::string prefix;for(const auto& row:rows)prefix+=row[column];if(!prefixes.count(prefix)){valid=false;break;}}if(valid&&search())return true;rows.pop_back();}return false;};if(search())return rows;}return {};'
    if language=='csharp':return 'var seen=new HashSet<string>(StringComparer.Ordinal);var groups=new List<string>[6];for(int i=0;i<groups.Length;++i)groups[i]=new List<string>();int maximum=0;foreach(string word in words)if(seen.Add(word)){groups[word.Length].Add(word);maximum=Math.Max(maximum,word.Length);}for(int area=maximum*maximum;area>0;--area)for(int height=1;height<=maximum;++height){if(area%height!=0)continue;int width=area/height;if(width>maximum||groups[width].Count==0||groups[height].Count==0)continue;var prefixes=new HashSet<string>(StringComparer.Ordinal);foreach(string word in groups[height])for(int length=1;length<=height;++length)prefixes.Add(word.Substring(0,length));var rows=new List<string>();bool Search(){if(rows.Count==height)return true;foreach(string word in groups[width]){rows.Add(word);bool valid=true;for(int column=0;column<width;++column){var prefix=new StringBuilder();foreach(string row in rows)prefix.Append(row[column]);if(!prefixes.Contains(prefix.ToString())){valid=false;break;}}if(valid&&Search())return true;rows.RemoveAt(rows.Count-1);}return false;}if(Search())return rows;}return [];'
    return 'Set<String> seen=new HashSet<>();List<List<String>> groups=new ArrayList<>();for(int i=0;i<=5;++i)groups.add(new ArrayList<>());int maximum=0;for(String word:words)if(seen.add(word)){groups.get(word.length()).add(word);maximum=Math.max(maximum,word.length());}for(int area=maximum*maximum;area>0;--area)for(int height=1;height<=maximum;++height){if(area%height!=0)continue;int width=area/height;if(width>maximum||groups.get(width).isEmpty()||groups.get(height).isEmpty())continue;Set<String> prefixes=new HashSet<>();for(String word:groups.get(height))for(int length=1;length<=height;++length)prefixes.add(word.substring(0,length));List<String> rows=new ArrayList<>();int targetHeight=height,targetWidth=width;class Search {boolean run(){if(rows.size()==targetHeight)return true;for(String word:groups.get(targetWidth)){rows.add(word);boolean valid=true;for(int column=0;column<targetWidth;++column){StringBuilder prefix=new StringBuilder();for(String row:rows)prefix.append(row.charAt(column));if(!prefixes.contains(prefix.toString())){valid=false;break;}}if(valid&&run())return true;rows.remove(rows.size()-1);}return false;}}if(new Search().run())return rows;}return new ArrayList<>();'

_previous_names_body=body

def body(ref,language):
    if ref!='17.7':return _previous_names_body(ref,language)
    if language=='python':return '''adjacent = [[] for _ in names]
for first, second in synonyms:
    adjacent[first].append(second)
    adjacent[second].append(first)
visited = [False] * len(names)
result = []
for start in range(len(names)):
    if visited[start]:
        continue
    visited[start] = True
    queue = [start]
    total = 0
    for name in queue:
        total += frequencies[name]
        for other in adjacent[name]:
            if not visited[other]:
                visited[other] = True
                queue.append(other)
    result.append([start, total])
return result'''
    if language=='javascript':return 'const adjacent=Array.from({length:names.length},()=>[]),visited=new Array(names.length).fill(false),result=[];for(const [first,second] of synonyms){adjacent[first].push(second);adjacent[second].push(first);}for(let start=0;start<names.length;++start){if(visited[start])continue;visited[start]=true;const queue=[start];let total=0;for(let head=0;head<queue.length;++head){const name=queue[head];total+=frequencies[name];for(const other of adjacent[name])if(!visited[other]){visited[other]=true;queue.push(other);}}result.push([start,total]);}return result;'
    if language=='cpp':return 'int n=static_cast<int>(names.size());std::vector<std::vector<int>> adjacent(n),result;for(const auto& edge:synonyms){adjacent[edge[0]].push_back(edge[1]);adjacent[edge[1]].push_back(edge[0]);}std::vector<bool> visited(n,false);for(int start=0;start<n;++start){if(visited[start])continue;visited[start]=true;std::vector<int> queue{start};int total=0;for(size_t head=0;head<queue.size();++head){int name=queue[head];total+=frequencies[name];for(int other:adjacent[name])if(!visited[other]){visited[other]=true;queue.push_back(other);}}result.push_back({start,total});}return result;'
    if language=='csharp':return 'int n=names.Length;var adjacent=new List<int>[n];for(int i=0;i<n;++i)adjacent[i]=new List<int>();foreach(var edge in synonyms){adjacent[edge[0]].Add(edge[1]);adjacent[edge[1]].Add(edge[0]);}bool[] visited=new bool[n];var result=new List<int[]>();for(int start=0;start<n;++start){if(visited[start])continue;visited[start]=true;var queue=new List<int>{start};int total=0;for(int head=0;head<queue.Count;++head){int name=queue[head];total+=frequencies[name];foreach(int other in adjacent[name])if(!visited[other]){visited[other]=true;queue.Add(other);}}result.Add([start,total]);}return result.ToArray();'
    return 'int n=names.length;List<List<Integer>> adjacent=new ArrayList<>();for(int i=0;i<n;++i)adjacent.add(new ArrayList<>());for(int[] edge:synonyms){adjacent.get(edge[0]).add(edge[1]);adjacent.get(edge[1]).add(edge[0]);}boolean[] visited=new boolean[n];List<int[]> result=new ArrayList<>();for(int start=0;start<n;++start){if(visited[start])continue;visited[start]=true;List<Integer> queue=new ArrayList<>();queue.add(start);int total=0;for(int head=0;head<queue.size();++head){int name=queue.get(head);total+=frequencies[name];for(int other:adjacent.get(name))if(!visited[other]){visited[other]=true;queue.add(other);}}result.add(new int[]{start,total});}return result.toArray(new int[0][]);'

_previous_median_body=body

def body(ref,language):
    if ref!='17.20':return _previous_median_body(ref,language)
    if language=='python':return '''from heapq import heappush, heappop
lower = []
upper = []
medians = []
for value in values:
    if not lower or value <= -lower[0]:
        heappush(lower, -value)
    else:
        heappush(upper, value)
    if len(lower) > len(upper) + 1:
        heappush(upper, -heappop(lower))
    elif len(upper) > len(lower):
        heappush(lower, -heappop(upper))
    medians.append(float(-lower[0]) if len(lower) > len(upper) else (-lower[0] + upper[0]) / 2.0)
return medians'''
    if language=='csharp':return 'var lower=new PriorityQueue<int,long>();var upper=new PriorityQueue<int,long>();var medians=new double[values.Length];for(int i=0;i<values.Length;++i){int value=values[i];if(lower.Count==0||value<=lower.Peek())lower.Enqueue(value,-(long)value);else upper.Enqueue(value,value);if(lower.Count>upper.Count+1){int moved=lower.Dequeue();upper.Enqueue(moved,moved);}else if(upper.Count>lower.Count){int moved=upper.Dequeue();lower.Enqueue(moved,-(long)moved);}medians[i]=lower.Count>upper.Count?lower.Peek():((double)lower.Peek()+upper.Peek())/2.0;}return medians;'
    if language=='java':return 'var lower=new PriorityQueue<Integer>(Comparator.reverseOrder());var upper=new PriorityQueue<Integer>();double[] medians=new double[values.length];for(int i=0;i<values.length;++i){int value=values[i];if(lower.isEmpty()||value<=lower.peek())lower.add(value);else upper.add(value);if(lower.size()>upper.size()+1)upper.add(lower.remove());else if(upper.size()>lower.size())lower.add(upper.remove());medians[i]=lower.size()>upper.size()?lower.peek():((double)lower.peek()+upper.peek())/2.0;}return medians;'
    if language=='cpp':return 'std::priority_queue<int> lower;std::priority_queue<int,std::vector<int>,std::greater<int>> upper;std::vector<double> medians;medians.reserve(values.size());for(int value:values){if(lower.empty()||value<=lower.top())lower.push(value);else upper.push(value);if(lower.size()>upper.size()+1){upper.push(lower.top());lower.pop();}else if(upper.size()>lower.size()){lower.push(upper.top());upper.pop();}medians.push_back(lower.size()>upper.size()?lower.top():(static_cast<double>(lower.top())+upper.top())/2.0);}return medians;'
    return '''class Heap {
  constructor(before) { this.data = []; this.before = before; }
  push(value) {
    const data = this.data;
    data.push(value);
    let index = data.length - 1;
    while (index > 0) {
      const parent = Math.floor((index - 1) / 2);
      if (!this.before(data[index], data[parent])) break;
      [data[index], data[parent]] = [data[parent], data[index]];
      index = parent;
    }
  }
  pop() {
    const data = this.data, result = data[0], last = data.pop();
    if (data.length !== 0) {
      data[0] = last;
      let index = 0;
      while (2 * index + 1 < data.length) {
        let child = 2 * index + 1;
        if (child + 1 < data.length && this.before(data[child + 1], data[child])) ++child;
        if (!this.before(data[child], data[index])) break;
        [data[index], data[child]] = [data[child], data[index]];
        index = child;
      }
    }
    return result;
  }
}
const lower = new Heap((a,b) => a > b), upper = new Heap((a,b) => a < b), medians = [];
for (const value of values) {
  if (lower.data.length === 0 || value <= lower.data[0]) lower.push(value);
  else upper.push(value);
  if (lower.data.length > upper.data.length + 1) upper.push(lower.pop());
  else if (upper.data.length > lower.data.length) lower.push(upper.pop());
  medians.push(lower.data.length > upper.data.length ? lower.data[0] : (lower.data[0] + upper.data[0]) / 2);
}
return medians;'''

_previous_bits_body=body

def body(ref,language):
    if ref!='17.4':return _previous_bits_body(ref,language)
    if language=='python':return '''current = list(range(numbers.Size()))
answer = 0
column = 0
while current and column < 32:
    zeros = []
    ones = []
    for index in current:
        (zeros if numbers.FetchBit(index,column) == 0 else ones).append(index)
    if len(zeros) <= len(ones):
        current = zeros
    else:
        answer |= 1 << column
        current = ones
    column += 1
return answer'''
    if language=='javascript':return 'let current=Array.from({length:numbers.Size()},(_,i)=>i),answer=0,column=0;while(current.length&&column<32){const zeros=[],ones=[];for(const index of current)(numbers.FetchBit(index,column)===0?zeros:ones).push(index);if(zeros.length<=ones.length)current=zeros;else{answer|=1<<column;current=ones;}++column;}return answer;'
    if language=='csharp':return 'var current=new List<int>();for(int i=0;i<numbers.Size();++i)current.Add(i);int answer=0,column=0;while(current.Count>0&&column<32){var zeros=new List<int>();var ones=new List<int>();foreach(int index in current)(numbers.FetchBit(index,column)==0?zeros:ones).Add(index);if(zeros.Count<=ones.Count)current=zeros;else{answer|=1<<column;current=ones;}column++;}return answer;'
    if language=='java':return 'var current=new ArrayList<Integer>();for(int i=0;i<numbers.Size();++i)current.add(i);int answer=0,column=0;while(!current.isEmpty()&&column<32){var zeros=new ArrayList<Integer>();var ones=new ArrayList<Integer>();for(int index:current)(numbers.FetchBit(index,column)==0?zeros:ones).add(index);if(zeros.size()<=ones.size())current=zeros;else{answer|=1<<column;current=ones;}column++;}return answer;'
    return 'std::vector<int> current;for(int i=0;i<numbers.Size();++i)current.push_back(i);int answer=0,column=0;while(!current.empty()&&column<32){std::vector<int> zeros,ones;for(int index:current)(numbers.FetchBit(index,column)==0?zeros:ones).push_back(index);if(zeros.size()<=ones.size())current=std::move(zeros);else{answer|=1<<column;current=std::move(ones);}++column;}return answer;'

_previous_binode_body=body

def body(ref,language):
    if ref!='17.12':return _previous_binode_body(ref,language)
    if language=='python':return '''stack = []
current = root
previous = None
head = None
while current is not None or stack:
    while current is not None:
        stack.append(current)
        current = current.Node1
    node = stack.pop()
    right = node.Node2
    node.Node1 = previous
    if previous is None:
        head = node
    else:
        previous.Node2 = node
    previous = node
    current = right
if previous is not None:
    previous.Node2 = None
return head'''
    if language=='javascript':return 'const stack=[];let current=root,previous=null,head=null;while(current!==null||stack.length){while(current!==null){stack.push(current);current=current.Node1;}const node=stack.pop(),right=node.Node2;node.Node1=previous;if(previous===null)head=node;else previous.Node2=node;previous=node;current=right;}if(previous!==null)previous.Node2=null;return head;'
    if language=='csharp':return 'var stack=new Stack<BiNode>();BiNode? current=root,previous=null,head=null;while(current is not null||stack.Count>0){while(current is not null){stack.Push(current);current=current.Node1;}var node=stack.Pop();var right=node.Node2;node.Node1=previous;if(previous is null)head=node;else previous.Node2=node;previous=node;current=right;}if(previous is not null)previous.Node2=null;return head;'
    if language=='java':return 'var stack=new ArrayDeque<BiNode>();BiNode current=root,previous=null,head=null;while(current!=null||!stack.isEmpty()){while(current!=null){stack.push(current);current=current.Node1;}BiNode node=stack.pop(),right=node.Node2;node.Node1=previous;if(previous==null)head=node;else previous.Node2=node;previous=node;current=right;}if(previous!=null)previous.Node2=null;return head;'
    return 'std::vector<BiNode*> stack;BiNode* current=root;BiNode* previous=nullptr;BiNode* head=nullptr;while(current!=nullptr||!stack.empty()){while(current!=nullptr){stack.push_back(current);current=current->Node1;}BiNode* node=stack.back();stack.pop_back();BiNode* right=node->Node2;node->Node1=previous;if(previous==nullptr)head=node;else previous->Node2=node;previous=node;current=right;}if(previous!=nullptr)previous->Node2=nullptr;return head;'

_previous_random_body=body

def body(ref,language):
    if ref not in ('17.2','17.3'):return _previous_random_body(ref,language)
    if ref=='17.2':
        if language=='python':return 'for index in range(len(values)-1,0,-1):\n    other = RandomSource.GetRandom(0,index)\n    values[index], values[other] = values[other], values[index]'
        if language=='javascript':return 'for(let index=values.length-1;index>0;--index){const other=RandomSource.GetRandom(0,index);[values[index],values[other]]=[values[other],values[index]];}'
        if language=='csharp':return 'for(int index=values.Length-1;index>0;--index){int other=RandomSource.GetRandom(0,index);(values[index],values[other])=(values[other],values[index]);}'
        if language=='java':return 'for(int index=values.length-1;index>0;--index){int other=RandomSource.GetRandom(0,index),saved=values[index];values[index]=values[other];values[other]=saved;}'
        return 'for(int index=static_cast<int>(values.size())-1;index>0;--index){int other=RandomSource::GetRandom(0,index);std::swap(values[index],values[other]);}'
    if language=='python':return 'reservoir = values[:count]\nif count == 0:\n    return reservoir\nfor index in range(count,len(values)):\n    slot = RandomSource.GetRandom(0,index)\n    if slot < count:\n        reservoir[slot] = values[index]\nreturn reservoir'
    if language=='javascript':return 'const reservoir=values.slice(0,count);if(count===0)return reservoir;for(let index=count;index<values.length;++index){const slot=RandomSource.GetRandom(0,index);if(slot<count)reservoir[slot]=values[index];}return reservoir;'
    if language=='csharp':return 'var reservoir=values.Take(count).ToArray();if(count==0)return reservoir;for(int index=count;index<values.Length;++index){int slot=RandomSource.GetRandom(0,index);if(slot<count)reservoir[slot]=values[index];}return reservoir;'
    if language=='java':return 'int[] reservoir=Arrays.copyOf(values,count);if(count==0)return reservoir;for(int index=count;index<values.length;++index){int slot=RandomSource.GetRandom(0,index);if(slot<count)reservoir[slot]=values[index];}return reservoir;'
    return 'std::vector<int> reservoir(values.begin(),values.begin()+count);if(count==0)return reservoir;for(int index=count;index<static_cast<int>(values.size());++index){int slot=RandomSource::GetRandom(0,index);if(slot<count)reservoir[slot]=values[index];}return reservoir;'
