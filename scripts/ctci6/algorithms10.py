"""Independent sorting/searching algorithms with explicit mutation targets."""

def body(ref,language):
    if ref=='10.1':
        if language=='python':return '''a, b, write = realCount - 1, len(second) - 1, len(first) - 1
while b >= 0:
    if a >= 0 and first[a] > second[b]:
        first[write] = first[a]
        a -= 1
    else:
        first[write] = second[b]
        b -= 1
    write -= 1
return first'''
        if language=='javascript':return 'let a=realCount-1,b=second.length-1,write=first.length-1;while(b>=0){if(a>=0&&first[a]>second[b])first[write--]=first[a--];else first[write--]=second[b--];}return first;'
        length=lambda name:name+'.Length' if language=='csharp' else name+'.length' if language=='java' else 'static_cast<int>('+name+'.size())'
        return f'int a=realCount-1,b={length("second")}-1,write={length("first")}-1;while(b>=0){{if(a>=0&&first[a]>second[b])first[write--]=first[a--];else first[write--]=second[b--];}}return first;'
    if ref=='10.2':
        if language=='python':return "words.sort(key=lambda word: ''.join(sorted(word)))\nreturn words.copy()"
        if language=='javascript':return 'const decorated=words.map(word=>({key:[...word].sort().join(""),word}));decorated.sort((a,b)=>a.key<b.key?-1:a.key>b.key?1:0);for(let i=0;i<words.length;++i)words[i]=decorated[i].word;return words.slice();'
        if language=='cpp':return 'std::vector<std::pair<std::string,std::string>> decorated;decorated.reserve(words.size());for(const auto& word:words){auto key=word;std::sort(key.begin(),key.end());decorated.emplace_back(key,word);}std::sort(decorated.begin(),decorated.end());for(size_t i=0;i<words.size();++i)words[i]=decorated[i].second;return words;'
        if language=='csharp':return 'var decorated=new (string Key,string Word)[words.Length];for(int i=0;i<words.Length;++i){var letters=words[i].ToCharArray();Array.Sort(letters);decorated[i]=(new string(letters),words[i]);}Array.Sort(decorated,(a,b)=>StringComparer.Ordinal.Compare(a.Key,b.Key));for(int i=0;i<words.Length;++i)words[i]=decorated[i].Word;return new List<string>(words);'
        return 'int n=words.length;String[] original=words.clone(),keys=new String[n];Integer[] order=new Integer[n];for(int i=0;i<n;++i){char[] letters=words[i].toCharArray();Arrays.sort(letters);keys[i]=new String(letters);order[i]=i;}Arrays.sort(order,(a,b)->keys[a].compareTo(keys[b]));for(int i=0;i<n;++i)words[i]=original[order[i]];return new ArrayList<>(Arrays.asList(words));'
    if ref=='10.3':
        if language=='python':return '''left, right = 0, len(values) - 1
while left <= right:
    middle = left + (right - left) // 2
    if values[middle] == target:
        return middle
    if values[left] == values[middle] == values[right]:
        left += 1
        right -= 1
    elif values[left] <= values[middle]:
        if values[left] <= target < values[middle]:
            right = middle - 1
        else:
            left = middle + 1
    else:
        if values[middle] < target <= values[right]:
            left = middle + 1
        else:
            right = middle - 1
return -1'''
        if language=='javascript':return 'let left=0,right=values.length-1;while(left<=right){const middle=left+Math.floor((right-left)/2);if(values[middle]===target)return middle;if(values[left]===values[middle]&&values[middle]===values[right]){++left;--right;}else if(values[left]<=values[middle]){if(values[left]<=target&&target<values[middle])right=middle-1;else left=middle+1;}else{if(values[middle]<target&&target<=values[right])left=middle+1;else right=middle-1;}}return -1;'
        size='values.Length' if language=='csharp' else 'values.length' if language=='java' else 'static_cast<int>(values.size())'
        return f'int left=0,right={size}-1;while(left<=right){{int middle=left+(right-left)/2;if(values[middle]==target)return middle;if(values[left]==values[middle]&&values[middle]==values[right]){{++left;--right;}}else if(values[left]<=values[middle]){{if(values[left]<=target&&target<values[middle])right=middle-1;else left=middle+1;}}else{{if(values[middle]<target&&target<=values[right])left=middle+1;else right=middle-1;}}}}return -1;'
    if ref=='10.5':
        if language=='python':return '''if not target:
    return -1
low, high = 0, len(words) - 1
while low <= high:
    middle = low + (high - low) // 2
    if not words[middle]:
        left, right = middle - 1, middle + 1
        while True:
            if left < low and right > high:
                return -1
            if right <= high and words[right]:
                middle = right
                break
            if left >= low and words[left]:
                middle = left
                break
            left -= 1
            right += 1
    if words[middle] == target:
        return middle
    if words[middle] < target:
        low = middle + 1
    else:
        high = middle - 1
return -1'''
        if language=='javascript':return 'if(target.length===0)return -1;let low=0,high=words.length-1;while(low<=high){let middle=low+Math.floor((high-low)/2);if(words[middle].length===0){let left=middle-1,right=middle+1;while(true){if(left<low&&right>high)return -1;if(right<=high&&words[right].length!==0){middle=right;break;}if(left>=low&&words[left].length!==0){middle=left;break;}--left;++right;}}if(words[middle]===target)return middle;if(words[middle]<target)low=middle+1;else high=middle-1;}return -1;'
        size='words.Length' if language=='csharp' else 'words.length' if language=='java' else 'static_cast<int>(words.size())'
        empty=lambda word:word+'.Length==0' if language=='csharp' else word+'.isEmpty()' if language=='java' else word+'.empty()'
        compare='StringComparer.Ordinal.Compare(words[middle],target)' if language=='csharp' else 'words[middle].compareTo(target)' if language=='java' else 'words[middle].compare(target)'
        return f'if({empty("target")})return -1;int low=0,high={size}-1;while(low<=high){{int middle=low+(high-low)/2;if({empty("words[middle]")}){{int left=middle-1,right=middle+1;while(true){{if(left<low&&right>high)return -1;if(right<=high&&!({empty("words[right]")})){{middle=right;break;}}if(left>=low&&!({empty("words[left]")})){{middle=left;break;}}--left;++right;}}}}int comparison={compare};if(comparison==0)return middle;if(comparison<0)low=middle+1;else high=middle-1;}}return -1;'
    if ref=='10.9':
        if language=='python':return '''rows = len(matrix)
columns = len(matrix[0]) if rows else 0
row, column = 0, columns - 1
while row < rows and column >= 0:
    value = matrix[row][column]
    if value == target:
        return [row, column]
    if value > target:
        column -= 1
    else:
        row += 1
return [-1, -1]'''
        if language=='javascript':return 'const rows=matrix.length,columns=rows?matrix[0].length:0;let row=0,column=columns-1;while(row<rows&&column>=0){const value=matrix[row][column];if(value===target)return [row,column];if(value>target)--column;else ++row;}return [-1,-1];'
        rows='matrix.Length' if language=='csharp' else 'matrix.length' if language=='java' else 'static_cast<int>(matrix.size())'
        cols='matrix[0].Length' if language=='csharp' else 'matrix[0].length' if language=='java' else 'static_cast<int>(matrix[0].size())'
        make=lambda a,b:'['+a+','+b+']' if language=='csharp' else 'new int[]{'+a+','+b+'}' if language=='java' else '{'+a+','+b+'}'
        return f'int rows={rows},columns=rows==0?0:{cols},row=0,column=columns-1;while(row<rows&&column>=0){{int value=matrix[row][column];if(value==target)return {make("row","column")};if(value>target)--column;else ++row;}}return {make("-1","-1")};'
    if ref=='10.11':
        if language=='python':return '''for index in range(1, len(values), 2):
    best = index
    if values[index - 1] > values[best]:
        best = index - 1
    if index + 1 < len(values) and values[index + 1] > values[best]:
        best = index + 1
    values[index], values[best] = values[best], values[index]
return values'''
        if language=='javascript':return 'for(let i=1;i<values.length;i+=2){let best=i;if(values[i-1]>values[best])best=i-1;if(i+1<values.length&&values[i+1]>values[best])best=i+1;[values[i],values[best]]=[values[best],values[i]];}return values;'
        size='values.Length' if language=='csharp' else 'values.length' if language=='java' else 'static_cast<int>(values.size())'
        swap='int temporary=values[i];values[i]=values[best];values[best]=temporary;' if language!='cpp' else 'std::swap(values[i],values[best]);'
        return f'for(int i=1;i<{size};i+=2){{int best=i;if(values[i-1]>values[best])best=i-1;if(i+1<{size}&&values[i+1]>values[best])best=i+1;{swap}}}return values;'
    raise ValueError(ref)
