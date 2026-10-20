"""Original Blind 75 contracts. Order is the Crackr page order, verified 2026-10-20.

Examples are authored here, rather than copied from another judge. The first
cases in each corpus are the public examples. No network is used by generation.
"""

SPECS = []
def add(title, topic, difficulty, method, params, result, description, constraints, cases, mode='function', comparison='ordered'):
    slug = ''.join(c.lower() if c.isalnum() else '_' for c in title).strip('_')
    while '__' in slug: slug = slug.replace('__', '_')
    SPECS.append(dict(id='blind75_' + slug, title=title, topic=topic, difficulty=difficulty,
        method=method, params=[dict(name=n, type=t) for n,t in params], result=result,
        description=description, constraints=constraints, cases=[dict(arguments=a, expected=e) for a,e in cases],
        mode=mode, comparison=comparison, position=len(SPECS)+1))

add('Two Sum','Arrays','Easy','TwoSum',[('nums','ai'),('target','i')],'ai',
    'Find two different positions in nums whose values add to target. Return their zero-based indices in either order. Exactly one pair of positions works; using one position twice is forbidden.',
    ['2 ≤ nums.length ≤ 3000; values and target are integers between -1000000 and 1000000.','The array is not necessarily sorted.'],
    [([[4,1,8,6],10],[0,3]), ([[5,5],10],[0,1]), ([[0,-3,8],5],[1,2])],comparison='unordered')
add('Contains Duplicate','Arrays','Easy','ContainsDuplicate',[('nums','ai')],'b',
    'Return whether at least one integer occurs at two different positions in nums.', ['0 ≤ nums.length ≤ 3000; values are signed 32-bit integers.'],
    [([[2,7,2]],True), ([[2,7,4]],False), ([[]],False)])
add('Top K Frequent Elements','Arrays','Medium','TopKFrequent',[('nums','ai'),('k','i')],'ai',
    'Return the k distinct values that occur most often in nums, in any order. Frequencies at the selection boundary are different, so the selected set is unique.',
    ['1 ≤ nums.length ≤ 3000.','1 ≤ k ≤ the number of distinct values.'],
    [([[8,8,8,3,3,4],2],[8,3]), ([[-2,-2,5],1],[-2]), ([[4,9],2],[4,9])],comparison='unordered')
add('Product of Array Except Self','Arrays','Medium','ProductExceptSelf',[('nums','ai')],'ai',
    'For every position i, return the product of all nums entries except nums[i]. Use no division and aim for linear time. A zero is a normal factor.',
    ['2 ≤ nums.length ≤ 3000.','Every prefix, suffix, and requested product fits a signed 32-bit integer.'],
    [([[2,3,4]],[12,8,6]), ([[0,5,0]],[0,0,0]), ([[-1,2,0]],[0,0,-2])])
add('Longest Consecutive Sequence','Arrays','Medium','LongestConsecutive',[('nums','ai')],'i',
    'Return the largest number of distinct consecutive integer values present in nums. Their positions need not be consecutive; duplicates add no length. Return zero for an empty array.',
    ['0 ≤ nums.length ≤ 3000; -1000000 ≤ nums[i] ≤ 1000000.','Aim for expected linear time.'],
    [([[11,4,6,5,5,20]],3), ([[]],0), ([[-2,-1,0,2]],3)])
add('3Sum','Arrays','Medium','ThreeSum',[('nums','ai')],'aai',
    'Return all distinct triples of values whose sum is zero and which can be chosen from three different positions in nums. Order within a triple and order among triples do not matter. Do not repeat a value triple.',
    ['0 ≤ nums.length ≤ 200; -100000 ≤ nums[i] ≤ 100000.'],
    [([[-2,0,2,2,-2]],[[-2,0,2]]), ([[0,0,0,0]],[[0,0,0]]), ([[1,2]],[])],comparison='nested')
add('Container With Most Water','Arrays','Medium','MaxArea',[('height','ai')],'i',
    'At index i stands a vertical segment from (i,0) to (i,height[i]). Choose two segments to form an upright container. Return the greatest area: their horizontal distance times the shorter height.',
    ['2 ≤ height.length ≤ 3000; 0 ≤ height[i] ≤ 100000.'],
    [([[3,1,4,2]],6), ([[0,0]],0), ([[5,5]],5)])
add('Best Time to Buy and Sell Stock','Arrays','Easy','MaxProfit',[('prices','ai')],'i',
    'Choose at most one day to buy and a strictly later day to sell one share. Return the largest possible sale price minus purchase price, or zero when no profitable transaction exists.',
    ['1 ≤ prices.length ≤ 3000; 0 ≤ prices[i] ≤ 100000.'],
    [([[9,3,8,2,6]],5), ([[8,5,1]],0), ([[5]],0)])
add('Combination Sum','Arrays','Medium','CombinationSum',[('candidates','ai'),('target','i')],'aai',
    'Return all distinct multisets of candidates whose sum is target. Each candidate is positive and may be used any number of times. Changing selection order does not make a new combination. Return each combination once, in any order.',
    ['1 ≤ candidates.length ≤ 12; candidates are distinct integers from 1 to 40.','1 ≤ target ≤ 40.'],
    [([[2,5,7],9],[[2,2,5],[2,7]]), ([[4,6],5],[]), ([[3],6],[[3,3]])],comparison='nested')
add('Insert Interval','Arrays','Medium','Insert',[('intervals','aai'),('newInterval','ai')],'aai',
    'Insert newInterval into the sorted disjoint closed intervals and return the sorted union. Closed intervals sharing an endpoint overlap and must be merged.',
    ['0 ≤ intervals.length ≤ 3000.','Each interval is [start,end] with -1000000 ≤ start ≤ end ≤ 1000000; input intervals are sorted and do not overlap.'],
    [([[[1,3],[7,9]],[3,8]],[[1,9]]), ([[],[2,4]],[[2,4]]), ([[[1,2]],[5,6]],[[1,2],[5,6]])])
add('Merge Intervals','Arrays','Medium','Merge',[('intervals','aai')],'aai',
    'Return the union of the closed input intervals, sorted by start. Merge every overlap, including shared endpoints. Input order is arbitrary.',
    ['0 ≤ intervals.length ≤ 3000; every interval [start,end] satisfies -1000000 ≤ start ≤ end ≤ 1000000.'],
    [([[[5,8],[1,4],[4,6]]],[[1,8]]), ([[]],[]), ([[[2,2],[3,3]]],[[2,2],[3,3]])])
add('Non-overlapping Intervals','Arrays','Medium','EraseOverlapIntervals',[('intervals','aai')],'i',
    'Remove as few intervals as possible so the remaining intervals have no overlap of positive length. Return the removal count. Here a meeting ending at t is compatible with one starting at t.',
    ['0 ≤ intervals.length ≤ 3000; -1000000 ≤ start < end ≤ 1000000.'],
    [([[[1,4],[2,3],[3,5]]],1), ([[]],0), ([[[1,2],[2,3]]],0)])
add('Meeting Rooms','Arrays','Easy','CanAttendMeetings',[('intervals','aai')],'b',
    'Can one person attend every meeting? A meeting occupies [start,end); another may start exactly when it ends. Return false if any two meetings overlap.',
    ['0 ≤ intervals.length ≤ 3000; 0 ≤ start < end ≤ 1000000.'],
    [([[[1,3],[3,6]]],True), ([[[1,5],[2,4]]],False), ([[]],True)])
add('Meeting Rooms II','Arrays','Medium','MinMeetingRooms',[('intervals','aai')],'i',
    'Return the fewest rooms needed to host all meetings. A room is free at a meeting\'s end time; intervals occupy [start,end).',
    ['0 ≤ intervals.length ≤ 3000; 0 ≤ start < end ≤ 1000000.'],
    [([[[1,5],[2,3],[3,6]]],2), ([[[1,2],[2,3]]],1), ([[]],0)])
add('Missing Number','Arrays','Easy','MissingNumber',[('nums','ai')],'i',
    'nums contains n different integers chosen from 0 through n inclusive. Return the one value in that range that is absent.',
    ['0 ≤ n = nums.length ≤ 3000; all entries are distinct and lie in [0,n].'],
    [([[3,0,1]],2), ([[]],0), ([[0,1]],2)])
add('Valid Anagram','Strings','Easy','IsAnagram',[('s','s'),('t','s')],'b',
    'Return whether s and t contain exactly the same letters with the same multiplicities. Character order is irrelevant.',
    ['s and t contain only lowercase English letters; each length is at most 3000.'],
    [(['abbc','bcab'],True), (['aab','abb'],False), (['',''],True)])
add('Group Anagrams','Strings','Medium','GroupAnagrams',[('strs','as')],'aas',
    'Partition all input strings into groups with identical letter counts. Include singleton groups and preserve duplicate entries. Group order and order inside groups do not matter.',
    ['0 ≤ strs.length ≤ 3000; each string has at most 100 lowercase English letters.'],
    [([['ab','c','ba','ab']],[['ab','ba','ab'],['c']]), ([['','']],[['','']]), ([[]],[])],comparison='nested')
add('Encode and Decode Strings','Strings','Medium','Codec',[('strings','as')],'as',
    'Implement Encode(strings) returning a single string and Decode(encoded) restoring the original list exactly. The harness calls Decode on a fresh Codec instance, so the encoding must carry all information. No required wire format is imposed.',
    ['0 ≤ strings.length ≤ 200; each string has at most 200 ASCII characters, including digits, separators, newlines, and NUL.','Decode receives a string produced by Encode. An empty list differs from a list containing an empty string.'],
    [([['a:3','', 'b\nc']],['a:3','','b\nc']), ([[]],[]), ([['']],['']), ([['\u0000#','12']],['\u0000#','12'])],mode='strings_codec')
add('Valid Palindrome','Strings','Easy','IsPalindrome',[('s','s')],'b',
    'Discard every character other than ASCII letters and digits, and ignore letter case. Return whether the remaining sequence reads the same in both directions. The empty sequence is a palindrome.',
    ['s contains at most 3000 ASCII characters.'],
    [(['A man, a plan, a canal: Panama!'],True), (['0P'],False), (['...'],True)])
add('Longest Substring Without Repeating Characters','Strings','Medium','LengthOfLongestSubstring',[('s','s')],'i',
    'Return the greatest length of a contiguous substring of s whose characters are all distinct. Spaces and punctuation are characters too.',
    ['0 ≤ s.length ≤ 3000; s contains ASCII characters.'],
    [(['abba'],2), (['a b!a'],4), ([''],0)])
add('Longest Repeating Character Replacement','Strings','Medium','CharacterReplacement',[('s','s'),('k','i')],'i',
    'You may replace at most k characters of s by any uppercase English letters. Return the longest contiguous substring that can then consist of just one repeated letter.',
    ['s contains at most 3000 uppercase English letters; 0 ≤ k ≤ s.length.'],
    [(['ABABA',1],3), (['ABCD',2],3), (['',0],0)])
add('Minimum Window Substring','Strings','Hard','MinWindow',[('s','s'),('t','s')],'s',
    'Return the shortest contiguous substring of s containing every character of t with at least its multiplicity. Return the empty string if no such window exists. If several shortest windows exist, return the leftmost one.',
    ['s and t contain ASCII letters; 0 ≤ s.length ≤ 3000; 1 ≤ t.length ≤ 3000.','Character case is significant.'],
    [(['cabefab','ab'],'ab'), (['aaab','aab'],'aab'), (['a','aa'],'')])
add('Longest Palindromic Substring','Strings','Medium','LongestPalindrome',[('s','s')],'s',
    'Return a longest contiguous substring of s that reads identically forwards and backwards. If several have the greatest length, return the leftmost one. Return an empty string for empty input.',
    ['0 ≤ s.length ≤ 1000; s consists of ASCII letters and digits; case is significant.'],
    [(['babad'],'bab'), (['cabbad'],'abba'), ([''],'')])
add('Palindromic Substrings','Strings','Medium','CountSubstrings',[('s','s')],'i',
    'Count the nonempty contiguous substrings that are palindromes. Two equal strings occurring at different position ranges count separately.',
    ['0 ≤ s.length ≤ 1000; s consists of lowercase English letters.'],
    [(['aaa'],6), (['aba'],4), ([''],0)])
add('Valid Parentheses','Stack','Easy','IsValid',[('s','s')],'b',
    'Return whether every opening bracket is closed by the same bracket type in proper nesting order. The three pairs are (), [], and {}. The empty string is valid.',
    ['0 ≤ s.length ≤ 3000; every character is one of ()[]{}.'],
    [(['{[()]}'],True), (['([)]'],False), ([''],True), (['('],False)])
add('Rotate Image','Matrix','Medium','Rotate',[('matrix','aai')],'void',
    'Rotate the square matrix 90 degrees clockwise by mutating the supplied matrix itself. Return no value. Preserve its outer array and each row object; replacing the parameter by a new matrix does not count. The displayed result is the matrix after the call.',
    ['1 ≤ matrix.length ≤ 100; every row has exactly matrix.length entries; values are signed 32-bit integers.'],
    [([[[1,2],[3,4]]],[[3,1],[4,2]]), ([[[7]]],[[7]]), ([[[1,2,3],[4,5,6],[7,8,9]]],[[7,4,1],[8,5,2],[9,6,3]])],mode='matrix_inplace')
add('Spiral Matrix','Matrix','Medium','SpiralOrder',[('matrix','aai')],'ai',
    'Return every matrix entry once in clockwise spiral order, starting at the top-left and moving right. The matrix can be rectangular.',
    ['1 ≤ rows, columns ≤ 100; all rows have the same length; values are signed 32-bit integers.'],
    [([[[1,2,3],[4,5,6]]],[1,2,3,6,5,4]), ([[[1],[2],[3]]],[1,2,3])])
add('Set Matrix Zeroes','Matrix','Medium','SetZeroes',[('matrix','aai')],'void',
    'For each zero in the original matrix, set its entire row and column to zero. Mutate the supplied matrix, preserving the outer array and row objects, and return no value. Newly created zeros must not trigger further clearing. The displayed result is the final matrix.',
    ['1 ≤ rows, columns ≤ 100; all rows have the same length; values are signed 32-bit integers.','Aim for constant auxiliary space.'],
    [([[[1,0,3],[4,5,6]]],[[0,0,0],[4,0,6]]), ([[[0]]],[[0]]), ([[[1,2]]],[[1,2]])],mode='matrix_inplace')
add('Find Minimum in Rotated Sorted Array','Binary Search','Medium','FindMin',[('nums','ai')],'i',
    'nums was a strictly increasing array and was rotated at an arbitrary pivot, possibly not at all. Return its smallest value in logarithmic time.',
    ['1 ≤ nums.length ≤ 3000; all values are distinct signed 32-bit integers.'],
    [([[6,9,1,3]],1), ([[2]],2), ([[1,2,3]],1)])
add('Search in Rotated Sorted Array','Binary Search','Medium','Search',[('nums','ai'),('target','i')],'i',
    'nums is a rotation of a strictly increasing array. Return the zero-based position of target, or -1 when absent. Aim for logarithmic time.',
    ['0 ≤ nums.length ≤ 3000; all values are distinct signed 32-bit integers; target is a signed 32-bit integer.'],
    [([[6,9,1,3],1],2), ([[6,9,1,3],8],-1), ([[],1],-1)])
add('Reverse Linked List','Linked List','Easy','ReverseList',[('head','list')],'list',
    'Reverse an acyclic singly linked list by changing next links, and return its new head. Reuse exactly the original nodes and preserve each node\'s value. Lists in examples are shown as arrays of node values.',
    ['0 ≤ number of nodes ≤ 3000; values are signed 32-bit integers.'],
    [([[2,4,4]],[4,4,2]), ([[]],[]), ([[9]],[9])],mode='list_reuse')
add('Merge Two Sorted Lists','Linked List','Easy','MergeTwoLists',[('list1','list'),('list2','list')],'list',
    'Merge two disjoint acyclic lists sorted in nondecreasing order. Relink their existing nodes into one sorted list and return its head. Preserve every node and its value; allocate no replacement output nodes.',
    ['The lists have at most 3000 nodes in total; node values are signed 32-bit integers.'],
    [([[1,4],[1,3]],[1,1,3,4]), ([[],[]],[]), ([[],[2]],[2])],mode='list_reuse')
add('Linked List Cycle','Linked List','Easy','HasCycle',[('head','list')],'b',
    'Return whether repeatedly following next from head eventually revisits a node. The harness creates the list from values and connects its last node to the zero-based pos node when pos ≥ 0; pos = -1 means no cycle. pos is test setup, not a method argument. Do not change any node.',
    ['0 ≤ number of nodes ≤ 3000; -1 ≤ pos < number of nodes; an empty list has pos = -1.'],
    [([[4,7,4],1],True), ([[4,4],-1],False), ([[], -1],False), ([[2],0],True)],mode='list_cycle')
add('Reorder List','Linked List','Medium','ReorderList',[('head','list')],'void',
    'For nodes L0,L1,…,Ln, relink the list as L0,Ln,L1,L(n-1),… . Mutate links without changing node values or allocating replacement nodes. Return no value. The displayed output follows next from the original head.',
    ['0 ≤ number of nodes ≤ 3000; input is acyclic.'],
    [([[1,2,3,4,5]],[1,5,2,4,3]), ([[1,2,3,4]],[1,4,2,3]), ([[]],[])],mode='list_reorder')
add('Remove Nth Node From End of List','Linked List','Medium','RemoveNthFromEnd',[('head','list'),('n','i')],'list',
    'Remove the nth node counted backwards from the tail (n = 1 removes the tail). Return the head of the remaining list. Relink original nodes and preserve their values; no replacement nodes are allowed.',
    ['1 ≤ number of nodes ≤ 3000; 1 ≤ n ≤ number of nodes; input is acyclic.'],
    [([[5,6,7],2],[5,7]), ([[5],1],[]), ([[5,6],2],[6])],mode='list_remove')
add('Merge k Sorted Lists','Linked List','Hard','MergeKLists',[('lists','lists')],'list',
    'Merge all the disjoint, acyclic lists into one nondecreasing list by relinking original nodes. Return its head. Preserve every node and its value, and allocate no replacement output nodes.',
    ['0 ≤ lists.length ≤ 100; at most 3000 nodes in total; each input list is sorted.'],
    [([[[1,5],[],[2,2,7]]],[1,2,2,5,7]), ([[]],[]), ([[[],[]]],[])],mode='list_reuse')
add('Invert Binary Tree','Binary Tree','Easy','InvertTree',[('root','tree')],'tree',
    'Swap the left and right children at every node and return the original root. Mutate the original nodes without changing values or replacing nodes. Trees are displayed in breadth-first order with null for a missing child, omitting trailing nulls.',
    ['0 ≤ number of nodes ≤ 1000; node values are signed 32-bit integers; input is a proper tree.'],
    [([[4,2,7,1,None,6,9]],[4,7,2,9,6,None,1]), ([[]],[]), ([[3]],[3])],mode='tree_inplace')
add('Maximum Depth of Binary Tree','Binary Tree','Easy','MaxDepth',[('root','tree')],'i',
    'Return the greatest number of nodes on a root-to-leaf path. An empty tree has depth zero. Trees use breadth-first values with null missing children and omitted trailing nulls.',
    ['0 ≤ number of nodes ≤ 1000; node values are signed 32-bit integers.'],
    [([[1,None,2,3]],3), ([[]],0), ([[8]],1)])
add('Same Tree','Binary Tree','Easy','IsSameTree',[('p','tree'),('q','tree')],'b',
    'Return whether p and q have the same shape and equal values at every corresponding node. Two empty trees are equal. Trees use breadth-first values with null missing children.',
    ['Each tree has at most 1000 nodes with signed 32-bit values.'],
    [([[1,2],[1,None,2]],False), ([[],[]],True), ([[1,2,3],[1,2,3]],True)])
add('Subtree of Another Tree','Binary Tree','Easy','IsSubtree',[('root','tree'),('subRoot','tree')],'b',
    'Return whether some node of root is the root of a subtree identical in shape and values to subRoot. A subtree includes that node and every descendant. An empty subRoot is a subtree of every tree, including an empty tree.',
    ['Each tree has at most 1000 nodes with signed 32-bit values; breadth-first arrays use null for missing children.'],
    [([[3,4,5,1,2],[4,1,2]],True), ([[3,4,5,1,2],[4,1]],False), ([[],[]],True)])
add('Binary Tree Level Order Traversal','Binary Tree','Medium','LevelOrder',[('root','tree')],'aai',
    'Return one array for each depth, listing node values from left to right. Return an empty array for an empty tree. Input uses breadth-first values and null missing children.',
    ['0 ≤ number of nodes ≤ 1000; node values are signed 32-bit integers.'],
    [([[4,2,7,None,3]],[[4],[2,7],[3]]), ([[]],[])])
add('Construct Binary Tree from Preorder and Inorder Traversal','Binary Tree','Medium','BuildTree',[('preorder','ai'),('inorder','ai')],'tree',
    'Reconstruct the unique binary tree with the supplied preorder (root, left, right) and inorder (left, root, right) traversals. Return its root. Output uses breadth-first values and null for missing children.',
    ['The arrays contain the same distinct signed 32-bit values and describe a valid tree.','0 ≤ preorder.length = inorder.length ≤ 1000.'],
    [([[4,2,3,7],[2,3,4,7]],[4,2,7,None,3]), ([[],[]],[]), ([[1],[1]],[1])])
add('Binary Tree Maximum Path Sum','Binary Tree','Hard','MaxPathSum',[('root','tree')],'i',
    'A path follows parent-child edges and visits each of its nodes once. It may start and end anywhere and must contain at least one node. Return the greatest sum of values along a path; it need not pass through the root.',
    ['1 ≤ number of nodes ≤ 1000; -1000 ≤ node.val ≤ 1000; input uses breadth-first values and null missing children.'],
    [([[-5,2,4]],4), ([[1,2,3]],6), ([[-3]],-3)])
add('Serialize and Deserialize Binary Tree','Binary Tree','Hard','Codec',[('root','tree')],'tree',
    'Implement Serialize(root) returning a string and Deserialize(encoded) restoring a proper binary tree with the same shape and values. Deserialize runs on a fresh Codec instance; do not rely on saved object state. The restored nodes must be separate from the input nodes. Preserve the input tree. Any self-contained string format is allowed.',
    ['0 ≤ number of nodes ≤ 1000; values are signed 32-bit integers.','Input/output trees use breadth-first values and null missing children; Deserialize receives Serialize output.'],
    [([[2,None,5,4]],[2,None,5,4]), ([[]],[]), ([[0,-1,0]],[0,-1,0])],mode='tree_codec')
add('Lowest Common Ancestor of a Binary Search Tree','Binary Search Tree','Easy','LowestCommonAncestor',[('root','tree'),('p','i'),('q','i')],'tree_node',
    'Return the original node that is the lowest common ancestor of the nodes with values p and q in a strict binary search tree. A node counts as its own descendant. p and q are supplied as values, are distinct, and both occur. The displayed result is the returned node\'s value.',
    ['2 ≤ number of nodes ≤ 1000; all values are distinct signed 32-bit integers; no parent pointers are supplied.'],
    [([[6,2,8,0,4,7,9,None,None,3,5],2,4],2), ([[2,1,3],1,3],2)],mode='tree_node')
add('Validate Binary Search Tree','Binary Search Tree','Medium','IsValidBST',[('root','tree')],'b',
    'Return whether every node\'s entire left subtree has smaller values and its entire right subtree has larger values. Equal values are forbidden anywhere along an ancestor constraint. An empty tree is valid.',
    ['0 ≤ number of nodes ≤ 1000; values are signed 32-bit integers; breadth-first arrays use null for missing children.'],
    [([[5,1,7,None,None,4,8]],False), ([[2,1,3]],True), ([[2,2]],False), ([[]],True)])
add('Kth Smallest Element in a BST','Binary Search Tree','Medium','KthSmallest',[('root','tree'),('k','i')],'i',
    'Return the kth smallest node value in a strict binary search tree, counting from 1.',
    ['1 ≤ k ≤ number of nodes ≤ 1000; values are distinct signed 32-bit integers; input uses breadth-first arrays with null missing children.'],
    [([[4,2,6,1,3],3],3), ([[9],1],9)])
add('Implement Trie (Prefix Tree)','Tries','Medium','Trie',[('operations','as'),('arguments','as')],'ab',
    'Implement a Trie with Insert(word), Search(word), and StartsWith(prefix). The empty trie contains no words. Search checks complete previously inserted words; StartsWith checks whether any inserted word begins with prefix. Operations run on one instance in order. The displayed result includes only boolean query results.',
    ['The equally sized operations and arguments arrays have at most 3000 entries.','Operations are insert, search, or startsWith; arguments contain lowercase English letters, including the empty string; inserts may repeat.'],
    [([['search','insert','search','search','startsWith','insert','search'],['','cat','cat','ca','ca','ca','ca']],[False,True,False,True,True]), ([['startsWith','insert','search','startsWith'],['','','','']],[False,True,True])],mode='trie')
add('Design Add and Search Words Data Structure','Tries','Medium','WordDictionary',[('operations','as'),('arguments','as')],'ab',
    'Implement AddWord(word) and Search(pattern) on one WordDictionary instance. Search succeeds if a stored word matches the entire pattern; a dot matches exactly one arbitrary lowercase letter. Inserts may repeat. The displayed result includes only search results.',
    ['The equally sized operations and arguments arrays have at most 3000 entries; operations are addWord or search.','Words contain lowercase English letters; patterns may additionally contain dots; lengths are at most 100 and may be zero.'],
    [([['addWord','addWord','search','search','search'],['cat','car','ca.','c..t','...']],[True,False,True]), ([['search','addWord','search'],['','','']],[False,True])],mode='dictionary')
add('Word Search II','Tries','Hard','FindWords',[('board','as'),('words','as')],'as',
    'Return every distinct dictionary word that can be traced through horizontally or vertically adjacent board cells. A cell may occur at most once in a word\'s path. Return each found word once, in any order. Each board string is one row.',
    ['1 ≤ rows, columns ≤ 12; all rows have equal length and lowercase English letters.','0 ≤ words.length ≤ 1000; words are nonempty lowercase strings of length at most 20; duplicates may occur.'],
    [([['ab','cd'],['ab','ac','aba','bd','ab']],['ab','ac','bd']), ([['a'],['a','aa']],['a'])],comparison='unordered')
add('Find Median from Data Stream','Heap','Hard','MedianFinder',[('operations','as'),('values','ai')],'ad',
    'Implement AddNum(value) and FindMedian() on one MedianFinder instance. A median is the middle sorted value for odd size or the mean of the two middle values for even size. The displayed result contains only median queries; the corresponding values entry for a query is ignored.',
    ['The equally sized arrays have at most 3000 operations: addNum or findMedian.','Every query follows at least one insertion; inserted values are signed 32-bit integers.'],
    [([['addNum','addNum','findMedian','addNum','findMedian'],[5,1,0,9,0]],[3.0,5.0]), ([['addNum','addNum','findMedian'],[-2147483648,2147483647,0]],[-0.5])],mode='median')
add('Word Search','Graphs','Medium','Exist',[('board','as'),('word','s')],'b',
    'Return whether word can be traced in the board using horizontal and vertical steps. Each cell may be visited at most once along that path. Each board string is one row; diagonal steps are forbidden.',
    ['1 ≤ rows, columns ≤ 12; all rows have equal length and lowercase English letters.','word contains 1 to 20 lowercase English letters.'],
    [([['ab','cd'],'abd'],True), ([['ab','cd'],'aba'],False), ([['ab','cd'],'ad'],False)])
add('Number of Islands','Graphs','Medium','NumIslands',[('grid','as')],'i',
    'Count connected groups of land cells in the rectangular grid. A 1 denotes land and a 0 water. Connections are horizontal or vertical, never diagonal. Each grid string is one row.',
    ['1 ≤ rows, columns ≤ 100; all rows have equal length and contain only 0 and 1.'],
    [([['100','010','001']],3), ([['110','010','001']],2), ([['000']],0)])
add('Clone Graph','Graphs','Medium','CloneGraph',[('node','graph')],'graph',
    'Return a deep copy of the undirected connected graph reachable from node. Every cloned node must be new and preserve its label and neighbor relationships; no cloned node or neighbor may refer to an original. Preserve the input graph. An empty graph has a null starting node. Example adjacency arrays list neighbors by labels 1 through n, with starting label 1.',
    ['0 ≤ number of nodes ≤ 100; labels are exactly 1 through n; edges are undirected, with no duplicates or self-loops.','Neighbor order is immaterial.'],
    [([[[2,3],[1],[1]]],[[2,3],[1],[1]]), ([[]],[]), ([[[]]],[[]])],mode='graph_clone')
add('Pacific Atlantic Water Flow','Graphs','Medium','PacificAtlantic',[('heights','aai')],'aai',
    'Water can flow from a cell to a horizontal or vertical neighbor of equal or lower height. The Pacific borders the top and left edges, and the Atlantic the bottom and right edges. Return every [row,column] cell from which water can reach both oceans, in any order.',
    ['1 ≤ rows, columns ≤ 100; all rows have equal length; 0 ≤ height ≤ 1000000.'],
    [([[[1,2],[4,3]]],[[0,1],[1,0],[1,1]]), ([[[8]]],[[0,0]]), ([[[1,1,1]]],[[0,0],[0,1],[0,2]])],comparison='unordered')
add('Course Schedule','Graphs','Medium','CanFinish',[('numCourses','i'),('prerequisites','aai')],'b',
    'Courses are numbered 0 through numCourses-1. Each pair [a,b] requires finishing b before starting a. Return whether all courses can be completed, equivalently whether the prerequisite graph has no directed cycle.',
    ['0 ≤ numCourses ≤ 1000; at most 3000 prerequisite pairs; each endpoint is a valid course; duplicate pairs are allowed.'],
    [([3,[[1,0],[2,1]]],True), ([2,[[1,0],[0,1]]],False), ([0,[]],True), ([1,[[0,0]]],False)])
add('Number of Connected Components in an Undirected Graph','Graphs','Medium','CountComponents',[('n','i'),('edges','aai')],'i',
    'Count the connected components of an undirected graph on vertices 0 through n-1. Isolated vertices each form a component. Each edge is a pair of endpoints.',
    ['0 ≤ n ≤ 1000; at most 3000 edges; endpoints are valid and different; duplicate edges are allowed.'],
    [([5,[[0,1],[1,2],[3,4]]],2), ([3,[]],3), ([0,[]],0)])
add('Graph Valid Tree','Graphs','Medium','ValidTree',[('n','i'),('edges','aai')],'b',
    'Return whether the undirected graph is a tree: it has at least one vertex, is connected, and has no cycle. Vertices are numbered 0 through n-1. A self-loop or repeated undirected edge prevents it from being a tree.',
    ['0 ≤ n ≤ 1000; at most 3000 edges; endpoints are valid vertex indices.'],
    [([4,[[0,1],[1,2],[1,3]]],True), ([3,[[0,1],[1,2],[2,0]]],False), ([1,[]],True), ([0,[]],False), ([2,[[0,1],[1,0]]],False)])
add('Alien Dictionary','Graphs','Hard','AlienOrder',[('words','as')],'s',
    'The words are sorted according to an unknown alphabet order. Return any string listing every distinct appearing character exactly once in an order consistent with that sorting. Return an empty string when no such order exists, including when a longer word appears before its own prefix. Alphabet symbols are lowercase English letters.',
    ['0 ≤ words.length ≤ 1000; each word has at most 100 letters and may be empty.','Ordinary lexicographic comparison is used with the unknown character order.'],
    [([['za','zb','ca','cb']],'zabc'), ([['ab','a']],''), ([['a','b','a']],''), ([[]],'')],comparison='alien')
add('Climbing Stairs','Dynamic Programming','Easy','ClimbStairs',[('n','i')],'i',
    'A staircase has n steps. Each move climbs either one or two steps. Return the number of different move sequences that reach the top exactly.',
    ['1 ≤ n ≤ 45; the answer fits a signed 32-bit integer.'],
    [([4],5), ([1],1), ([2],2)])
add('House Robber','Dynamic Programming','Medium','Rob',[('nums','ai')],'i',
    'Choose houses along a straight street to maximize the sum of their nonnegative values, without choosing adjacent houses. Return the greatest total; choosing no house is allowed.',
    ['0 ≤ nums.length ≤ 3000; 0 ≤ nums[i] ≤ 10000.'],
    [([[3,7,4,9]],16), ([[]],0), ([[5]],5)])
add('House Robber II','Dynamic Programming','Medium','Rob',[('nums','ai')],'i',
    'Choose nonadjacent houses to maximize the sum of their nonnegative values, with the houses arranged in a circle. The first and last houses are adjacent when there is more than one house. Choosing no house is allowed.',
    ['0 ≤ nums.length ≤ 3000; 0 ≤ nums[i] ≤ 10000.'],
    [([[4,1,2,7]],8), ([[5]],5), ([[]],0), ([[2,3]],3)])
add('Decode Ways','Dynamic Programming','Medium','NumDecodings',[('s','s')],'i',
    'Digits 1 through 26 encode the letters A through Z. Return how many ways the entire digit string can be split into valid letter codes. A code cannot have a leading zero. Return zero when no decoding exists.',
    ['1 ≤ s.length ≤ 100; s contains only digits; the answer fits a signed 32-bit integer.'],
    [(['121'],3), (['06'],0), (['2101'],1), (['0'],0)])
add('Coin Change','Dynamic Programming','Medium','CoinChange',[('coins','ai'),('amount','i')],'i',
    'You have unlimited copies of each positive coin denomination. Return the fewest coins whose sum is amount, or -1 if it cannot be formed. Amount zero needs zero coins.',
    ['1 ≤ coins.length ≤ 20; denominations are distinct integers from 1 to 10000.','0 ≤ amount ≤ 10000.'],
    [([[2,5],11],4), ([[4],6],-1), ([[3],0],0)])
add('Maximum Product Subarray','Dynamic Programming','Medium','MaxProduct',[('nums','ai')],'i',
    'Return the largest product of a nonempty contiguous subarray. Negative values and zeros are allowed.',
    ['1 ≤ nums.length ≤ 3000; -10 ≤ nums[i] ≤ 10.','Every contiguous-subarray product fits a signed 32-bit integer.'],
    [([[-2,3,-4]],24), ([[0,-2,0]],0), ([[-3]],-3)])
add('Word Break','Dynamic Programming','Medium','WordBreak',[('s','s'),('wordDict','as')],'b',
    'Return whether s can be formed by concatenating words from wordDict. A dictionary word can be used repeatedly; words must cover s without gaps. The empty string can be formed using no words.',
    ['0 ≤ s.length ≤ 3000; at most 1000 nonempty dictionary words; all characters are lowercase English letters.'],
    [(['catscat',['cat','s']],True), (['catsdog',['cat','dog']],False), (['',[]],True)])
add('Longest Increasing Subsequence','Dynamic Programming','Medium','LengthOfLIS',[('nums','ai')],'i',
    'Return the greatest length of a strictly increasing subsequence. Chosen positions must increase but need not be adjacent; equal values cannot extend the subsequence.',
    ['0 ≤ nums.length ≤ 3000; values are signed 32-bit integers.'],
    [([[4,1,3,2,5]],3), ([[2,2,2]],1), ([[]],0)])
add('Unique Paths','Dynamic Programming','Medium','UniquePaths',[('m','i'),('n','i')],'i',
    'Count paths from the top-left to the bottom-right cell of an m-row, n-column grid when each move goes one cell right or one cell down. There are no obstacles.',
    ['1 ≤ m,n ≤ 100; the answer fits a signed 32-bit integer.'],
    [([3,4],10), ([1,5],1), ([1,1],1)])
add('Jump Game','Dynamic Programming','Medium','CanJump',[('nums','ai')],'b',
    'Start at index zero. From index i you may move forward by any number of positions from 1 through nums[i]. Return whether the last index is reachable. A one-element array is already at its last index.',
    ['1 ≤ nums.length ≤ 3000; 0 ≤ nums[i] ≤ 3000.'],
    [([[2,0,1,0]],True), ([[1,0,2]],False), ([[0]],True)])
add('Combination Sum IV','Dynamic Programming','Medium','CombinationSum4',[('nums','ai'),('target','i')],'i',
    'Count ordered sequences of values from nums whose sum is target. Values may be used repeatedly. Different orders count separately: [1,2] and [2,1] are different. Target zero has one sequence, the empty sequence.',
    ['1 ≤ nums.length ≤ 20; values are distinct integers from 1 to 1000.','0 ≤ target ≤ 1000; the answer fits a signed 32-bit integer.'],
    [([[1,3],4],3), ([[2,4],3],0), ([[5],0],1)])
add('Maximum Subarray','Dynamic Programming','Medium','MaxSubArray',[('nums','ai')],'i',
    'Return the greatest sum of a nonempty contiguous subarray.',
    ['1 ≤ nums.length ≤ 3000; -10000 ≤ nums[i] ≤ 10000.'],
    [([[-4,3,-1,5,-8]],7), ([[-5,-2,-7]],-2), ([[0]],0)])
add('Number of 1 Bits','Bit Manipulation','Easy','HammingWeight',[('n','l')],'i',
    'Count the 1 bits in the unsigned 32-bit binary representation of n. n is passed in a 64-bit integer type so all unsigned 32-bit values are representable in every supported language.',
    ['0 ≤ n ≤ 4294967295.'],
    [([13],3), ([0],0), ([4294967295],32)])
add('Counting Bits','Bit Manipulation','Easy','CountBits',[('n','i')],'ai',
    'Return an array of length n+1 whose ith entry is the number of 1 bits in the nonnegative integer i.',
    ['0 ≤ n ≤ 100000.'],
    [([5],[0,1,1,2,1,2]), ([0],[0])])
add('Reverse Bits','Bit Manipulation','Easy','ReverseBits',[('n','l')],'l',
    'Reverse the order of all 32 bits of the unsigned integer n, including leading zero bits, and return the resulting unsigned value. Both input and output use a 64-bit integer type.',
    ['0 ≤ n ≤ 4294967295.'],
    [([1],2147483648), ([0],0), ([4294967295],4294967295), ([13],2952790016)])
add('Sum of Two Integers','Bit Manipulation','Medium','GetSum',[('a','i'),('b','i')],'i',
    'Return the sum of a and b without using the + or - arithmetic operators in your solution. Use bit operations to propagate carries. The mathematical sum fits a signed 32-bit integer.',
    ['-1000000000 ≤ a,b ≤ 1000000000.'],
    [([7,-3],4), ([-6,-8],-14), ([0,0],0), ([1000000000,1000000000],2000000000)])

assert len(SPECS) == 75
assert len({s['id'] for s in SPECS}) == 75
assert not any(s['title'] == 'Longest Common Subsequence' for s in SPECS)
