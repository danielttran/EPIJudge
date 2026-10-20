"""Deterministic edge cases and small randomized corpora, independently evaluated."""
import random
from copy import deepcopy
from oracle import solve

R=random.Random(750375)
def small_tree():
    if R.random()<.15:return []
    out=[R.randint(-8,8)]; pending=2
    while pending and len(out)<14:
        pending-=1
        if R.random()<.3: out.append(None)
        else:out.append(R.randint(-8,8));pending+=2
    while out and out[-1] is None:out.pop()
    return out

def bst(values):
    def build(v):
        if not v:return None
        m=len(v)//2;return [v[m],build(v[:m]),build(v[m+1:])]
    root=build(sorted(values));q=[root] if root else [];out=[]
    for n in q:
        out.append(n[0] if n else None)
        if n:q.extend(n[1:])
    while out and out[-1] is None:out.pop()
    return out

def make(s):
    m=s['method'];mode=s['mode']
    if mode=='strings_codec':return [[ ''.join(R.choice('012:#\n\x00abc') for _ in range(R.randrange(10))) for _ in range(R.randrange(6))]]
    if mode=='tree_codec':return [small_tree()]
    if mode in ('trie','dictionary'):
        ops=[];words=[];stored=[]
        for _ in range(25):
            insertion=R.random()<.4
            word=''.join(R.choice('abc') for _ in range(R.randrange(5)))
            if insertion: op='insert' if mode=='trie' else 'addWord';stored.append(word)
            else:
                op=R.choice(['search','startsWith']) if mode=='trie' else 'search'
                if stored and R.random()<.6:word=R.choice(stored)
                if mode=='dictionary' and R.random()<.5:word=''.join('.' if R.random()<.3 else c for c in word)
            ops.append(op);words.append(word)
        return [ops,words]
    if mode=='median':
        ops=['addNum'];values=[R.randint(-20,20)]
        for _ in range(20):ops.append(R.choice(['addNum','findMedian']));values.append(R.randint(-20,20))
        return [ops+['findMedian'],values+[0]]
    if m=='TwoSum':
        while True:
            nums=[R.randint(-12,12) for _ in range(R.randint(2,10))];i,j=R.sample(range(len(nums)),2);target=nums[i]+nums[j]
            if sum(nums[u]+nums[v]==target for u in range(len(nums)) for v in range(u+1,len(nums)))==1:return [nums,target]
    if m=='TopKFrequent':
        values=R.sample(range(-12,13),R.randint(1,5));nums=[v for i,v in enumerate(values) for _ in range(i+1)];R.shuffle(nums);return [nums,R.randint(1,len(values))]
    if m in ('ContainsDuplicate','LongestConsecutive','ThreeSum','LengthOfLIS'):return [[R.randint(-5,5) for _ in range(R.randrange(10))]]
    if m=='ProductExceptSelf':return [[R.randint(-2,2) for _ in range(R.randint(2,10))]]
    if m=='MaxArea':return [[R.randrange(12) for _ in range(R.randint(2,10))]]
    if m=='MaxProfit':return [[R.randrange(20) for _ in range(R.randint(1,10))]]
    if m=='CombinationSum':return [R.sample(range(2,10),R.randint(1,5)),R.randint(1,16)]
    if m in ('Insert','Merge','EraseOverlapIntervals','CanAttendMeetings','MinMeetingRooms'):
        intervals=[]
        for _ in range(R.randrange(7)):
            start=R.randrange(15);intervals.append([start,start+R.randint(1,5)])
        if m=='Insert':
            clean=[]
            for a,b in sorted(intervals):
                if not clean or a>clean[-1][1]:clean.append([a,b])
            start=R.randrange(15);return [clean,[start,start+R.randrange(6)]]
        return [intervals]
    if m=='MissingNumber':
        n=R.randrange(12);missing=R.randrange(n+1);v=[i for i in range(n+1) if i!=missing];R.shuffle(v);return [v]
    if m in ('IsAnagram','GroupAnagrams'):
        word=lambda:''.join(R.choice('abc') for _ in range(R.randrange(7)))
        if m=='GroupAnagrams':return [[word() for _ in range(R.randrange(10))]]
        x=word();return [x,''.join(R.sample(x,len(x))) if R.random()<.5 else word()]
    if m in ('IsPalindrome','LengthOfLongestSubstring','CharacterReplacement','MinWindow','LongestPalindrome','CountSubstrings','IsValid'):
        alphabet={'IsPalindrome':'aAbB01 ,!','LengthOfLongestSubstring':'ab01 !','CharacterReplacement':'ABC','MinWindow':'abAB','LongestPalindrome':'abc01','CountSubstrings':'abc','IsValid':'()[]{}'}[m]
        x=''.join(R.choice(alphabet) for _ in range(R.randrange(12)))
        if m=='CharacterReplacement':return [x,R.randrange(len(x)+1)]
        if m=='MinWindow':return [x,''.join(R.choice(alphabet) for _ in range(R.randint(1,5)))]
        return [x]
    if m in ('Rotate','SpiralOrder','SetZeroes','PacificAtlantic'):
        rows=R.randint(1,5);cols=rows if m=='Rotate' else R.randint(1,5)
        return [[[R.randrange(5) for _ in range(cols)] for _ in range(rows)]]
    if m in ('FindMin','Search'):
        v=sorted(R.sample(range(-20,21),R.randint(1,10)));k=R.randrange(len(v));v=v[k:]+v[:k]
        return [v] if m=='FindMin' else [v,R.choice(v) if R.random()<.6 else 30]
    if m in ('ReverseList','ReorderList','MergeTwoLists','HasCycle','RemoveNthFromEnd','MergeKLists'):
        v=[R.randint(-5,5) for _ in range(R.randrange(10))]
        if m=='MergeTwoLists':return [sorted(v),sorted(R.choices(range(-5,6),k=R.randrange(7)))]
        if m=='HasCycle':return [v,R.randrange(-1,len(v)) if v else -1]
        if m=='RemoveNthFromEnd':v=v or [0];return [v,R.randint(1,len(v))]
        if m=='MergeKLists':return [[sorted(R.choices(range(-5,6),k=R.randrange(6))) for _ in range(R.randrange(5))]]
        return [v]
    if m in ('InvertTree','MaxDepth','IsSameTree','IsSubtree','LevelOrder','MaxPathSum','IsValidBST'):
        v=small_tree()
        if m=='MaxPathSum':return [v or [-1]]
        if m in ('IsSameTree','IsSubtree'):return [v,deepcopy(v) if R.random()<.4 else small_tree()]
        return [bst(R.sample(range(-20,21),R.randrange(10))) if m=='IsValidBST' and R.random()<.5 else v]
    if m in ('BuildTree','LowestCommonAncestor','KthSmallest'):
        values=R.sample(range(-30,31),R.randint(2,10));t=bst(values)
        if m=='LowestCommonAncestor':return [t,*R.sample(values,2)]
        if m=='KthSmallest':return [t,R.randint(1,len(values))]
        from oracle import tree,inorder
        root=tree(t)
        def pre(n):return [n.val]+pre(n.left)+pre(n.right) if n else []
        return [pre(root),inorder(root)]
    if m in ('Exist','FindWords','NumIslands'):
        rows=R.randint(1,4);cols=R.randint(1,4);alphabet='01' if m=='NumIslands' else 'abc'
        board=[''.join(R.choice(alphabet) for _ in range(cols)) for _ in range(rows)]
        if m=='NumIslands':return [board]
        word=lambda:''.join(R.choice('abc') for _ in range(R.randint(1,6)))
        return [board,word() if m=='Exist' else [word() for _ in range(R.randrange(8))]]
    if mode=='graph_clone':
        n=R.randrange(9);adj=[set() for _ in range(n)]
        for i in range(1,n):j=R.randrange(i);adj[i].add(j+1);adj[j].add(i+1)
        for i in range(n):
            for j in range(i):
                if R.random()<.25:adj[i].add(j+1);adj[j].add(i+1)
        return [[sorted(row) for row in adj]]
    if m in ('CanFinish','CountComponents','ValidTree'):
        n=R.randrange(8);edges=[]
        if n:
            for _ in range(R.randrange(12)):
                u,v=R.randrange(n),R.randrange(n)
                if m!='CountComponents' or u!=v:edges.append([u,v])
        return [n,edges]
    if m=='AlienOrder':
        alphabet=list('abcd');R.shuffle(alphabet);rank={c:i for i,c in enumerate(alphabet)}
        words=[''.join(R.choice(alphabet) for _ in range(R.randrange(5))) for _ in range(R.randrange(8))]
        words.sort(key=lambda w:tuple(rank[c] for c in w))
        if R.random()<.3:words.reverse()
        return [words]
    if m=='ClimbStairs':return [R.randint(1,20)]
    if m=='Rob':return [[R.randrange(15) for _ in range(R.randrange(11))]]
    if m=='NumDecodings':return [''.join(R.choice('0123456789') for _ in range(R.randint(1,12))) ]
    if m=='CoinChange':return [R.sample(range(1,12),R.randint(1,5)),R.randrange(35)]
    if m=='MaxProduct':return [[R.randint(-2,2) for _ in range(R.randint(1,10))]]
    if m=='WordBreak':return [''.join(R.choice('ab') for _ in range(R.randrange(12))), [''.join(R.choice('ab') for _ in range(R.randint(1,4))) for _ in range(R.randrange(8))]]
    if m=='UniquePaths':return [R.randint(1,10),R.randint(1,10)]
    if m=='CanJump':return [[R.randrange(5) for _ in range(R.randint(1,12))]]
    if m=='CombinationSum4':return [R.sample(range(1,8),R.randint(1,5)),R.randrange(16)]
    if m=='MaxSubArray':return [[R.randint(-10,10) for _ in range(R.randint(1,12))]]
    if m in ('HammingWeight','ReverseBits'):return [R.randrange(1<<32)]
    if m=='CountBits':return [R.randrange(30)]
    if m=='GetSum':return [R.randint(-1000000000,1000000000),R.randint(-1000000000,1000000000)]
    raise ValueError(s['id'])

def extend(s):
    cases=deepcopy(s['cases']);seen={repr(c['arguments']) for c in cases}
    for _ in range(24):
        a=make(s)
        if repr(a) not in seen:
            cases.append(dict(arguments=a,expected=solve(s,a)));seen.add(repr(a))
    chain=[1]
    for i in range(2,1001):chain.extend([None,i])
    boundary=[]
    if s['method'] in ('MaxDepth','InvertTree') or s['mode']=='tree_codec':boundary.append([chain])
    if s['method']=='ClimbStairs':boundary.append([45])
    if s['method']=='CountBits':boundary.append([100000])
    if s['method']=='GetSum':boundary.append([-1000000000,-1000000000])
    for a in boundary:
        if repr(a) not in seen:cases.append(dict(arguments=a,expected=solve(s,a)))
    return cases
