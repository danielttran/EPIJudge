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

_previous_body=body

def body(ref,language):
    if ref not in ('10.4','10.8','10.10'):
        return _previous_body(ref,language)
    if ref=='10.4':
        if language=='python':return '''if target <= 0:
    return -1
bound = 1
while True:
    value = values.ElementAt(bound)
    if value == -1 or value >= target:
        break
    bound *= 2
low, high = bound // 2, bound
while low <= high:
    middle = low + (high - low) // 2
    value = values.ElementAt(middle)
    if value == -1 or value > target:
        high = middle - 1
    elif value < target:
        low = middle + 1
    else:
        return middle
return -1'''
        if language=='javascript':return 'if(target<=0)return -1;let bound=1;while(true){const value=values.ElementAt(bound);if(value===-1||value>=target)break;bound*=2;}let low=Math.floor(bound/2),high=bound;while(low<=high){const middle=low+Math.floor((high-low)/2),value=values.ElementAt(middle);if(value===-1||value>target)high=middle-1;else if(value<target)low=middle+1;else return middle;}return -1;'
        return 'if(target<=0)return -1;int bound=1;while(true){int value=values.ElementAt(bound);if(value==-1||value>=target)break;bound*=2;}int low=bound/2,high=bound;while(low<=high){int middle=low+(high-low)/2,value=values.ElementAt(middle);if(value==-1||value>target)high=middle-1;else if(value<target)low=middle+1;else return middle;}return -1;'
    if ref=='10.8':
        if language=='python':return '''bits = bytearray(4000)
count = 0
for value in values:
    slot, shift = (value - 1) >> 3, (value - 1) & 7
    mask = 1 << shift
    if bits[slot] & mask:
        count += 1
    else:
        bits[slot] |= mask
result = [0] * count
for index in range(4000):
    bits[index] = 0
write = 0
for value in values:
    slot, shift = (value - 1) >> 3, (value - 1) & 7
    mask = 1 << shift
    if bits[slot] & mask:
        result[write] = value
        write += 1
    else:
        bits[slot] |= mask
return result'''
        if language=='javascript':return 'const bits=new Uint8Array(4000);let count=0;for(const value of values){const slot=(value-1)>>3,mask=1<<((value-1)&7);if(bits[slot]&mask)++count;else bits[slot]|=mask;}const result=new Array(count);bits.fill(0);let write=0;for(const value of values){const slot=(value-1)>>3,mask=1<<((value-1)&7);if(bits[slot]&mask)result[write++]=value;else bits[slot]|=mask;}return result;'
        setup='byte[] bits=new byte[4000];' if language!='cpp' else 'std::array<unsigned char,4000> bits{};'
        loop='foreach(int value in values)' if language=='csharp' else 'for(int value:values)'
        mark='bits[slot]=(byte)(bits[slot]|mask);' if language in ('csharp','java') else 'bits[slot]=static_cast<unsigned char>(bits[slot]|mask);'
        clear='Array.Clear(bits);' if language=='csharp' else 'Arrays.fill(bits,(byte)0);' if language=='java' else 'bits.fill(0);'
        result='int[] result=new int[count];' if language!='cpp' else 'std::vector<int> result(count);'
        return f'{setup}int count=0;{loop}{{int slot=(value-1)>>3,mask=1<<((value-1)&7);if((bits[slot]&mask)!=0)++count;else {mark}}}{result}{clear}int write=0;{loop}{{int slot=(value-1)>>3,mask=1<<((value-1)&7);if((bits[slot]&mask)!=0)result[write++]=value;else {mark}}}return result;'
    if language=='python':return '''class RankTracker:
    class _Node:
        def __init__(self, value):
            self.value = value
            self.left_count = 0
            self.left = self.right = None

    def __init__(self):
        self._root = None

    def Track(self, value: int) -> None:
        if self._root is None:
            self._root = self._Node(value)
            return
        node = self._root
        while True:
            if value <= node.value:
                node.left_count += 1
                if node.left is None:
                    node.left = self._Node(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = self._Node(value)
                    return
                node = node.right

    def GetRank(self, value: int) -> int:
        node = self._root
        skipped = 0
        while node is not None:
            if value == node.value:
                return skipped + node.left_count
            if value < node.value:
                node = node.left
            else:
                skipped += node.left_count + 1
                node = node.right
        return -1
'''
    if language=='javascript':return 'class RankTracker {constructor(){this.root=null;}Track(value){if(this.root===null){this.root={value,leftCount:0,left:null,right:null};return;}let node=this.root;while(true){if(value<=node.value){++node.leftCount;if(node.left===null){node.left={value,leftCount:0,left:null,right:null};return;}node=node.left;}else{if(node.right===null){node.right={value,leftCount:0,left:null,right:null};return;}node=node.right;}}}GetRank(value){let node=this.root,skipped=0;while(node!==null){if(value===node.value)return skipped+node.leftCount;if(value<node.value)node=node.left;else{skipped+=node.leftCount+1;node=node.right;}}return -1;}}'
    if language=='csharp':return 'public class RankTracker {private sealed class Node {public int Value,LeftCount;public Node? Left,Right;public Node(int value){Value=value;}}private Node? root;public RankTracker(){}public void Track(int value){if(root==null){root=new Node(value);return;}Node node=root;while(true){if(value<=node.Value){++node.LeftCount;if(node.Left==null){node.Left=new Node(value);return;}node=node.Left;}else{if(node.Right==null){node.Right=new Node(value);return;}node=node.Right;}}}public int GetRank(int value){Node? node=root;int skipped=0;while(node!=null){if(value==node.Value)return skipped+node.LeftCount;if(value<node.Value)node=node.Left;else{skipped+=node.LeftCount+1;node=node.Right;}}return -1;}}'
    if language=='java':return 'class RankTracker {private static class Node {int value,leftCount;Node left,right;Node(int value){this.value=value;}}private Node root;public RankTracker(){}public void Track(int value){if(root==null){root=new Node(value);return;}Node node=root;while(true){if(value<=node.value){++node.leftCount;if(node.left==null){node.left=new Node(value);return;}node=node.left;}else{if(node.right==null){node.right=new Node(value);return;}node=node.right;}}}public int GetRank(int value){Node node=root;int skipped=0;while(node!=null){if(value==node.value)return skipped+node.leftCount;if(value<node.value)node=node.left;else{skipped+=node.leftCount+1;node=node.right;}}return -1;}}'
    return '#include <memory>\nclass RankTracker {struct Node {int value,leftCount=0;std::unique_ptr<Node> left,right;explicit Node(int value):value(value){}};std::unique_ptr<Node> root;public:RankTracker()=default;void Track(int value){if(!root){root=std::make_unique<Node>(value);return;}Node* node=root.get();while(true){if(value<=node->value){++node->leftCount;if(!node->left){node->left=std::make_unique<Node>(value);return;}node=node->left.get();}else{if(!node->right){node->right=std::make_unique<Node>(value);return;}node=node->right.get();}}}int GetRank(int value){Node* node=root.get();int skipped=0;while(node){if(value==node->value)return skipped+node->leftCount;if(value<node->value)node=node->left.get();else{skipped+=node->leftCount+1;node=node->right.get();}}return -1;}};'

_previous_file_body=body

def body(ref,language):
    if ref!='10.7':return _previous_file_body(ref,language)
    if language=='python':return '''block = 0
if smallMemory:
    counts = [0]*2048
    while True:
        value = file.ReadNext()
        if value == -1:
            break
        counts[value >> 20] += 1
    while counts[block] == 1 << 20:
        block += 1
    file.Reset()
bitmap = bytearray((1 << 17) if smallMemory else (1 << 28))
while True:
    value = file.ReadNext()
    if value == -1:
        break
    if not smallMemory or value >> 20 == block:
        offset = value & ((1 << 20)-1) if smallMemory else value
        bitmap[offset >> 3] |= 1 << (offset & 7)
for index, byte in enumerate(bitmap):
    if byte != 255:
        for bit in range(8):
            if byte & (1 << bit) == 0:
                return (block << 20) + (index << 3) + bit
return -1'''
    if language=='javascript':return 'let block=0;if(smallMemory){const counts=new Uint32Array(2048);for(let value;(value=file.ReadNext())!==-1;)++counts[value>>>20];while(counts[block]===(1<<20))++block;file.Reset();}const bitmap=new Uint8Array(smallMemory?1<<17:1<<28);for(let value;(value=file.ReadNext())!==-1;)if(!smallMemory||(value>>>20)===block){const offset=smallMemory?value&((1<<20)-1):value;bitmap[offset>>>3]|=1<<(offset&7);}for(let index=0;index<bitmap.length;++index)if(bitmap[index]!==255)for(let bit=0;bit<8;++bit)if((bitmap[index]&(1<<bit))===0)return block*1048576+index*8+bit;return -1;'
    if language=='csharp':return 'int block=0;if(smallMemory){var counts=new int[2048];int value;while((value=file.ReadNext())!=-1)counts[value>>20]++;while(counts[block]==(1<<20))block++;file.Reset();}var bitmap=new byte[smallMemory?1<<17:1<<28];int item;while((item=file.ReadNext())!=-1)if(!smallMemory||(item>>20)==block){int offset=smallMemory?item&((1<<20)-1):item;bitmap[offset>>3]|=(byte)(1<<(offset&7));}for(int index=0;index<bitmap.Length;++index)if(bitmap[index]!=255)for(int bit=0;bit<8;++bit)if((bitmap[index]&(1<<bit))==0)return (block<<20)+(index<<3)+bit;return -1;'
    if language=='java':return 'int block=0;if(smallMemory){int[] counts=new int[2048];int value;while((value=file.ReadNext())!=-1)counts[value>>>20]++;while(counts[block]==(1<<20))block++;file.Reset();}byte[] bitmap=new byte[smallMemory?1<<17:1<<28];int item;while((item=file.ReadNext())!=-1)if(!smallMemory||(item>>>20)==block){int offset=smallMemory?item&((1<<20)-1):item;bitmap[offset>>>3]|=(byte)(1<<(offset&7));}for(int index=0;index<bitmap.length;++index)if(bitmap[index]!=(byte)255)for(int bit=0;bit<8;++bit)if((bitmap[index]&(1<<bit))==0)return (block<<20)+(index<<3)+bit;return -1;'
    return 'int block=0;if(smallMemory){std::vector<int> counts(2048);int value;while((value=file.ReadNext())!=-1)++counts[value>>20];while(counts[block]==(1<<20))++block;file.Reset();}std::vector<unsigned char> bitmap(smallMemory?1u<<17:1u<<28);int item;while((item=file.ReadNext())!=-1)if(!smallMemory||(item>>20)==block){int offset=smallMemory?item&((1<<20)-1):item;bitmap[offset>>3]|=static_cast<unsigned char>(1<<(offset&7));}for(size_t index=0;index<bitmap.size();++index)if(bitmap[index]!=255)for(int bit=0;bit<8;++bit)if((bitmap[index]&(1<<bit))==0)return (block<<20)+static_cast<int>(index*8)+bit;return -1;'
