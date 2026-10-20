"""Original example reasoning, separate from executable language fixture sources."""
import json
from collections import Counter
from itertools import combinations
from math import prod
from oracle import tree,inorder

def show(v):return json.dumps(v,ensure_ascii=True)
def explain(s,c):
    a,e=c['arguments'],c['expected'];x=a[0];m=s['method'];mode=s['mode']
    if m=='TwoSum':i,j=e;return f'Positions {i} and {j} are different, and {x[i]} + {x[j]} = {a[1]}.'
    if m=='ContainsDuplicate':
        repeated=[v for v,n in Counter(x).items() if n>1]
        return f'{repeated[0]} occurs more than once.' if repeated else 'Every value occurs at most once, including when the array is empty.'
    if m=='TopKFrequent':return 'Selected frequencies: '+', '.join(f'{v} occurs {x.count(v)} time(s)' for v in e)+'. The selected set is unique; its order may vary.'
    if m=='ProductExceptSelf':return 'For positions in order, multiply the other entries: '+ '; '.join(f'{show(x[:i]+x[i+1:])} → {v}' for i,v in enumerate(e))+'.'
    if m=='LongestConsecutive':
        values=set(x)
        start=next((v for v in sorted(values) if all(v+i in values for i in range(e))),None)
        return f'A longest run is {show(list(range(start,start+e)))}; repeated entries do not extend it.' if e else 'There are no values, so the longest run has length zero.'
    if m=='ThreeSum':return '; '.join(' + '.join(map(str,row))+' = 0' for row in e)+'. Each triple is returned once despite repeated input values.' if e else 'No selection of three different positions has sum zero.'
    if m=='MaxArea':
        i,j=max(combinations(range(len(x)),2),key=lambda p:(min(x[p[0]],x[p[1]])*(p[1]-p[0]),p[1]-p[0]))
        return f'Use positions {i} and {j}: width {j-i} × shorter height {min(x[i],x[j])} = {e}. No pair gives a larger area.'
    if m=='MaxProfit':
        if not e:return 'No strictly later sale is more expensive than an earlier purchase, so making no transaction gives zero.'
        i,j=next((i,j) for i,j in combinations(range(len(x)),2) if x[j]-x[i]==e)
        return f'Buy on day {i} for {x[i]} and sell on day {j} for {x[j]}; the profit is {e}.'
    if m=='CombinationSum':return '; '.join(' + '.join(map(str,row))+f' = {a[1]}' for row in e)+'. Reordering a combination does not add another answer.' if e else 'No multiset of the candidate values reaches the target.'
    if m in ('Insert','Merge'):return f'The sorted closed union is {show(e)}. Any shared endpoint joins the intervals into the same merged component.'
    if m=='EraseOverlapIntervals':return f'Removing {e} interval(s) is sufficient and fewer cannot work. Touching endpoints are compatible under this contract.'
    if m=='CanAttendMeetings':return 'No pair has an overlap of positive length; a shared end/start time is allowed.' if e else 'At least two meetings occupy the same time, so one person cannot attend them all.'
    if m=='MinMeetingRooms':
        if not x:return 'With no meetings, no room is needed.'
        t=next(t for t in sorted({r[0] for r in x}) if sum(start<=t<end for start,end in x)==e)
        return f'At time {t}, exactly {e} meetings are in progress. Reusing a room at an end time achieves this peak room count.'
    if m=='MissingNumber':return f'The range is 0 through {len(x)} inclusive; {e} is its only absent value.'
    if m=='IsAnagram':return 'The two letter-frequency maps are identical.' if e else 'At least one letter has a different frequency in the two strings.'
    if m=='GroupAnagrams':return 'Every input occurrence appears once. Groups have sorted-letter keys '+show([''.join(sorted(row[0])) for row in e])+', and singleton groups are retained.'
    if mode=='strings_codec':return f'Decoding the encoding on a fresh instance must restore all {len(e)} entries exactly, including their separators, empty strings, and control characters. No particular encoded text is required.'
    if m=='IsPalindrome':
        normalized=''.join(ch.lower() for ch in x if ch.isascii() and ch.isalnum())
        return f'After filtering and lowercasing, the sequence is {show(normalized)}. It '+('equals' if e else 'differs from')+' its reversal.'
    if m=='LengthOfLongestSubstring':
        word=next((x[i:i+e] for i in range(len(x)-e+1) if len(set(x[i:i+e]))==e),'')
        return f'{show(word)} has {e} distinct characters and is contiguous. No longer substring has all characters distinct.'
    if m=='CharacterReplacement':
        word=next((x[i:i+e] for i in range(len(x)-e+1) if e==0 or e-max(Counter(x[i:i+e]).values())<=a[1]),'')
        replacements=e-max(Counter(word).values(),default=0)
        return f'The window {show(word)} needs {replacements} replacement(s), within the budget {a[1]}. No longer window fits the budget.'
    if m=='MinWindow':return f'{show(e)} contains all characters of {show(a[1])}, including repetitions, and is the leftmost shortest valid window.' if e else f'No window supplies all required occurrences in {show(a[1])}.'
    if m=='LongestPalindrome':return f'{show(e)} is a palindrome of length {len(e)}. No longer substring is palindromic; ties use the leftmost starting position.'
    if m=='CountSubstrings':
        ranges=[[i,j-1] for i in range(len(x)) for j in range(i+1,len(x)+1) if x[i:j]==x[i:j][::-1]]
        return f'The inclusive position ranges are {show(ranges)}, giving {e} palindromic occurrences.'
    if m=='IsValid':return 'The stack of unmatched openings is empty after all brackets close with matching types.' if e else 'A closing bracket mismatches the latest opening, or an opening remains unmatched at the end.'
    if m=='Rotate':return 'The new entry at [row,column] is the original entry at [n−1−column,row]. The displayed matrix results from changing values in the existing rows.'
    if m=='SpiralOrder':return f'Follow the outside boundary clockwise, then repeat on the remaining interior. This visits the {len(e)} entries once in the displayed order.'
    if m=='SetZeroes':
        zeros=[[r,cc] for r,row in enumerate(x) for cc,v in enumerate(row) if v==0]
        return f'Original zeros occur at {show(zeros)}. Clear their rows and columns together; newly written zeros cause no additional clearing.'
    if m=='FindMin':return f'{e} is the least value, even though the rotation can put it away from the first position.'
    if m=='Search':return f'nums[{e}] equals target {a[1]}.' if e>=0 else f'Target {a[1]} does not appear, so return −1.'
    if m=='ReverseList':return 'The original node positions are visited in order '+show(list(range(len(x)-1,-1,-1)))+'. Values stay attached to their nodes.'
    if m in ('MergeTwoLists','MergeKLists'):return f'All {len(e)} input nodes are relinked into nondecreasing value order. Equal-valued nodes are distinct and must all survive.'
    if mode=='list_cycle':return f'The tail points to original position {a[1]}, so following next eventually revisits that node.' if e else 'The last next link is null, so the traversal ends. Repeated values alone do not form a cycle.'
    if m=='ReorderList':return 'Take the first node, last node, next first node, next last node, and continue until every original node appears once.'
    if m=='RemoveNthFromEnd':return f'Remove original zero-based position {len(x)-a[1]}, which is {a[1]} node(s) from the end. The remaining original nodes keep their order.'
    if m=='InvertTree':return 'At every original node, exchange its left and right child references. The breadth-first result omits trailing null children.'
    if m=='MaxDepth':
        def longest(n):
            if not n:return []
            left,right=longest(n.left),longest(n.right)
            return [n.val]+(left if len(left)>=len(right) else right)
        path=longest(tree(x));return f'A deepest root-to-leaf path has values {show(path)} and contains {e} nodes.'
    if m=='IsSameTree':return 'Corresponding child positions and values all agree.' if e else 'The two trees differ in a child position or corresponding value; matching traversal values alone are insufficient.'
    if m=='IsSubtree':return 'The second tree occurs with its full shape and all descendants, or is empty.' if e else 'No node roots a subtree with exactly the second tree’s full shape and values.'
    if m=='LevelOrder':return 'Read each depth left to right: '+show(e)+'. Null children do not appear as values in the depth arrays.'
    if m=='BuildTree':return 'The reconstructed tree has preorder '+show(a[0])+' and inorder '+show(a[1])+'. Distinct values make that tree unique.'
    if m=='MaxPathSum':return f'The best nonempty path has sum {e}; a single node is allowed, so negative ancestors need not be included.'
    if mode=='tree_codec':return f'A fresh decoder must reconstruct breadth-first tree {show(e)} using newly allocated nodes. Preserve the original tree and encode missing children as needed in your chosen format.'
    if mode=='tree_node':return f'The node with value {e} is the lowest node containing both {a[1]} and {a[2]} among its descendants, counting itself. Return that original node.'
    if m=='IsValidBST':return 'All ancestor lower and upper bounds are strict and satisfied.' if e else 'A value violates an ancestor bound or repeats an ancestor value. Checking only immediate parent-child comparisons is insufficient.'
    if m=='KthSmallest':return f'Inorder values are {show(inorder(tree(x)))}. Entry {a[1]} when counting from 1 is {e}.'
    if mode in ('trie','dictionary'):
        results=iter(e);trace=[]
        for op,word in zip(*a):
            if op not in ('insert','addWord'):trace.append(f'{op}({show(word)}) → {str(next(results)).lower()}')
        return '; '.join(trace)+'. Insertions affect later queries on the same instance.'
    if m=='FindWords':return f'The found distinct words are {show(e)}. Each has a horizontal/vertical path using no cell twice; duplicate dictionary entries add no duplicate result.'
    if mode=='median':
        values=[];i=0;trace=[]
        for op,v in zip(*a):
            if op=='addNum':values.append(v);values.sort()
            else:trace.append(f'{show(values)} has median {e[i]}');i+=1
        return '; '.join(trace)+'. Compute even-size means without overflowing a 32-bit addition.'
    if m=='Exist':return f'A horizontal/vertical path spells {show(a[1])} without reusing a cell.' if e else f'No allowed path spells {show(a[1])}; neither diagonal moves nor cell reuse are allowed.'
    if m=='NumIslands':return f'There are {e} components of 1 cells under horizontal/vertical adjacency. Diagonal contact does not join components.'
    if mode=='graph_clone':return f'The copy has adjacency {show(e)} with labels preserved. Its node objects and neighbor references must all belong to the new graph.'
    if m=='PacificAtlantic':return f'The cells {show(e)} each have a non-increasing route to a top/left border and a bottom/right border. Border contact itself counts as reaching that ocean.'
    if m=='CanFinish':return 'A topological ordering exists, so every prerequisite can be satisfied before its dependent course.' if e else 'A directed prerequisite cycle prevents completing every course, even if some other courses are independent.'
    if m=='CountComponents':return f'The undirected graph has {e} maximal connected groups, including every isolated vertex as its own group.'
    if m=='ValidTree':return 'The graph is nonempty, connected, and has exactly n−1 edges, hence no cycle.' if e else 'The graph is empty, disconnected, or cyclic; repeated edges and self-loops also prevent tree status.'
    if m=='AlienOrder':return f'{show(e)} contains each appearing letter once and makes every adjacent word pair sorted. Other valid alphabet orders are accepted.' if e else 'Either no letters appear, or no alphabet order works. A reversed prefix relation or a directed character-order cycle makes a nonempty alphabet impossible.'
    if m=='ClimbStairs':return f'Sum C({x}−t,t) over t = 0 through {x//2}, where t is the number of two-step moves; the total is {e}.'
    if m=='Rob':
        circle=s['title']=='House Robber II'
        selected=next(([i for i in range(len(x)) if mask>>i&1] for mask in range(1<<len(x)) if sum(x[i] for i in range(len(x)) if mask>>i&1)==e and not(mask&(mask<<1)) and not(circle and len(x)>1 and mask&1 and mask>>(len(x)-1)&1)),[])
        return f'Choose positions {show(selected)} for total {e}, respecting '+('the circular first/last adjacency.' if circle else 'the straight-street adjacency rule.')
    if m=='NumDecodings':return f'There are {e} complete splits into codes from 1 through 26. Leading-zero codes and standalone zero codes are invalid.'
    if m=='CoinChange':return f'The fewest coins needed is {e}; every denomination is reusable.' if e>=0 else 'No nonnegative counts of the available denominations have the requested sum.'
    if m=='MaxProduct':
        i,j=next((i,j) for i in range(len(x)) for j in range(i+1,len(x)+1) if prod(x[i:j])==e)
        return f'The contiguous subarray {show(x[i:j])}, at inclusive positions [{i},{j-1}], has product {e}; no nonempty subarray has a larger product.'
    if m=='WordBreak':return 'Dictionary words can cover the entire string in order, with no gap; the empty string uses zero words.' if e else 'No concatenation of dictionary words covers the entire string.'
    if m=='LengthOfLIS':
        subsequence=next((list(v) for v in combinations(x,e) if all(v[i-1]<v[i] for i in range(1,e))),[])
        return f'{show(subsequence)} is a strictly increasing subsequence of length {e}. No longer such subsequence exists.'
    if m=='UniquePaths':return f'Every path has {a[0]-1} down moves and {a[1]-1} right moves. Choose their order in C({sum(a)-2},{a[0]-1}) = {e} ways.'
    if m=='CanJump':return 'There is a sequence of permitted forward jumps to the final position; a one-element array is already there.' if e else 'Every reachable position stops before a gap that cannot be crossed to the final position.'
    if m=='CombinationSum4':return f'There are {e} ordered sequences. Different value orders count separately; for target zero the empty sequence contributes one.'
    if m=='MaxSubArray':
        i,j=next((i,j) for i in range(len(x)) for j in range(i+1,len(x)+1) if sum(x[i:j])==e)
        return f'The nonempty contiguous subarray {show(x[i:j])}, at inclusive positions [{i},{j-1}], sums to {e}.'
    if m=='HammingWeight':return f'The 32-bit representation {x:032b} contains {e} one bit(s).'
    if m=='CountBits':return f'Include every integer from 0 through {x}, giving {x+1} counts; the count for i equals that for i>>1 plus its low bit.'
    if m=='ReverseBits':return f'Reverse all 32 positions: {x:032b} becomes {e:032b}, whose unsigned value is {e}.'
    if m=='GetSum':return f'The mathematical sum of {a[0]} and {a[1]} is {e}. The implementation must obtain it through bitwise carry propagation.'
    raise AssertionError('Missing original explanation: '+s['id'])
