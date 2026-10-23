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
