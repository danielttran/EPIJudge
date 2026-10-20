from __future__ import annotations
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0): self.val, self.neighbors = val, []
def two_sum(nums: list[int], target: int) -> list[int]:
    return solve(SPEC, [nums, target])


"""Independent, simple mathematical oracles for authored examples and small corpora.

These operate on serialized values, not on the runner's structure adapters.
Slow exhaustive methods are intentional; corpus inputs are bounded accordingly.
"""
import sys
sys.setrecursionlimit(10000)
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, permutations
from math import comb, prod

class OracleNode:
    def __init__(self, val): self.val, self.left, self.right = val, None, None

def tree(values):
    if not values: return None
    root = OracleNode(values[0]); queue = deque([root]); it = iter(values[1:])
    while queue:
        node = queue.popleft()
        for side in ['left','right']:
            value = next(it, None)
            if value is not None:
                child=OracleNode(value); setattr(node,side,child); queue.append(child)
    return root

def flatten(root):
    if root is None: return []
    out=[]; q=deque([root])
    while q:
        n=q.popleft(); out.append(n.val if n else None)
        if n: q.extend([n.left,n.right])
    while out and out[-1] is None: out.pop()
    return out

def same(a,b):
    if a is None or b is None: return a is b
    return a.val==b.val and same(a.left,b.left) and same(a.right,b.right)

def inorder(n): return inorder(n.left)+[n.val]+inorder(n.right) if n else []

def windows(s):
    return (s[i:j] for i in range(len(s)) for j in range(i+1,len(s)+1))

def neighbors(r,c,m,n):
    for x,y in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0<=x<m and 0<=y<n: yield x,y

def word_exists(board,word):
    m,n=len(board),len(board[0])
    def visit(r,c,i,seen):
        if board[r][c]!=word[i]: return False
        if i==len(word)-1: return True
        return any((x,y) not in seen and visit(x,y,i+1,seen|{(x,y)}) for x,y in neighbors(r,c,m,n))
    return any(visit(r,c,0,{(r,c)}) for r in range(m) for c in range(n))

def solve(spec,a):
    method, mode = spec['method'], spec['mode']
    x = a[0] if a else None
    if mode in ('strings_codec','tree_codec','graph_clone'): return x
    if mode in ('trie','dictionary'):
        stored=set(); out=[]
        for op,arg in zip(*a):
            if op in ('insert','addWord'): stored.add(arg)
            elif op=='startsWith': out.append(any(w.startswith(arg) for w in stored))
            elif mode=='trie': out.append(arg in stored)
            else: out.append(any(len(w)==len(arg) and all(p=='.' or p==v for p,v in zip(arg,w)) for w in stored))
        return out
    if mode=='median':
        values=[]; out=[]
        for op,v in zip(*a):
            if op=='addNum': values.append(v); values.sort()
            else:
                n=len(values); out.append((values[(n-1)//2]+values[n//2])/2)
        return out
    if method=='TwoSum': return next([i,j] for i,j in combinations(range(len(x)),2) if x[i]+x[j]==a[1])
    if method=='ContainsDuplicate': return len(set(x))<len(x)
    if method=='TopKFrequent': return [v for v,_ in Counter(x).most_common(a[1])]
    if method=='ProductExceptSelf': return [prod(x[:i]+x[i+1:]) for i in range(len(x))]
    if method=='LongestConsecutive': return max((next((i for i in range(1,len(set(x))+1) if v+i not in set(x)),len(set(x))) for v in set(x)), default=0)
    if method=='ThreeSum': return [list(t) for t in sorted({tuple(sorted(t)) for t in combinations(x,3) if sum(t)==0})]
    if method=='MaxArea': return max((min(x[i],x[j])*(j-i) for i,j in combinations(range(len(x)),2)),default=0)
    if method=='MaxProfit': return max([0]+[x[j]-x[i] for i,j in combinations(range(len(x)),2)])
    if method=='CombinationSum':
        out=[]
        def dfs(i,remaining,path):
            if remaining==0: out.append(path); return
            for j in range(i,len(x)):
                if x[j]<=remaining: dfs(j,remaining-x[j],path+[x[j]])
        dfs(0,a[1],[]); return out
    if method in ('Insert','Merge'):
        intervals=sorted(x+([a[1]] if method=='Insert' else [])); out=[]
        for start,end in intervals:
            if out and start<=out[-1][1]: out[-1][1]=max(out[-1][1],end)
            else: out.append([start,end])
        return out
    if method=='EraseOverlapIntervals':
        return len(x)-max((len(sub) for k in range(len(x)+1) for sub in combinations(sorted(x),k) if all(sub[i-1][1]<=sub[i][0] for i in range(1,k))),default=0)
    if method=='CanAttendMeetings': return all(a1[1]<=b[0] or b[1]<=a1[0] for a1,b in combinations(x,2))
    if method=='MinMeetingRooms': return max((sum(start<=t<end for start,end in x) for t in {p for row in x for p in row}),default=0)
    if method=='MissingNumber': return next(v for v in range(len(x)+1) if v not in x)
    if method=='IsAnagram': return Counter(x)==Counter(a[1])
    if method=='GroupAnagrams':
        groups={}
        for word in x: groups.setdefault(''.join(sorted(word)),[]).append(word)
        return list(groups.values())
    if method=='IsPalindrome':
        s=''.join(c.lower() for c in x if c.isascii() and c.isalnum()); return s==s[::-1]
    if method=='LengthOfLongestSubstring': return max([0]+[len(w) for w in windows(x) if len(set(w))==len(w)])
    if method=='CharacterReplacement': return max([0]+[len(w) for w in windows(x) if len(w)-max(Counter(w).values())<=a[1]])
    if method=='MinWindow': return min((w for w in windows(x) if not (Counter(a[1])-Counter(w))),key=len,default='')
    if method=='LongestPalindrome': return max((w for w in windows(x) if w==w[::-1]),key=len,default='')
    if method=='CountSubstrings': return sum(w==w[::-1] for w in windows(x))
    if method=='IsValid':
        previous=None
        while previous!=x:
            previous=x
            for pair in ['()','[]','{}']: x=x.replace(pair,'')
        return x==''
    if method=='Rotate': return [list(row) for row in zip(*x[::-1])]
    if method=='SpiralOrder':
        rows=[r[:] for r in x]; out=[]
        while rows:
            out+=rows.pop(0)
            if rows: rows=[list(r) for r in zip(*rows)][::-1]
        return out
    if method=='SetZeroes': return [[0 if 0 in x[r] or any(row[c]==0 for row in x) else v for c,v in enumerate(row)] for r,row in enumerate(x)]
    if method=='FindMin': return min(x)
    if method=='Search': return x.index(a[1]) if a[1] in x else -1
    if method=='ReverseList': return x[::-1]
    if method=='MergeTwoLists': return sorted(x+a[1])
    if method=='HasCycle': return a[1]>=0
    if method=='ReorderList':
        out=[]
        for i in range((len(x)+1)//2):
            out.append(x[i])
            if len(x)-1-i!=i: out.append(x[-1-i])
        return out
    if method=='RemoveNthFromEnd': return x[:len(x)-a[1]]+x[len(x)-a[1]+1:]
    if method=='MergeKLists': return sorted(v for row in x for v in row)
    if method=='InvertTree':
        def invert(t):
            if t: t.left,t.right=invert(t.right),invert(t.left)
            return t
        return flatten(invert(tree(x)))
    if method=='MaxDepth':
        def depth(t): return 1+max(depth(t.left),depth(t.right)) if t else 0
        return depth(tree(x))
    if method=='IsSameTree': return same(tree(x),tree(a[1]))
    if method=='IsSubtree':
        sub=tree(a[1])
        def contains(t): return sub is None or t is not None and (same(t,sub) or contains(t.left) or contains(t.right))
        return contains(tree(x))
    if method=='LevelOrder':
        q=[tree(x)] if x else []; out=[]
        while q: out.append([n.val for n in q]); q=[c for n in q for c in [n.left,n.right] if c]
        return out
    if method=='BuildTree':
        def build(pre,ino):
            if not pre: return None
            i=ino.index(pre[0]); n=OracleNode(pre[0]); n.left=build(pre[1:i+1],ino[:i]); n.right=build(pre[i+1:],ino[i+1:]); return n
        return flatten(build(*a))
    if method=='MaxPathSum':
        root=tree(x); nodes=[]; graph={}
        def visit(n,parent=None):
            if not n: return
            nodes.append(n); graph[n]=[c for c in [parent,n.left,n.right] if c]; visit(n.left,n); visit(n.right,n)
        visit(root)
        def paths(n,prev): return max([n.val]+[n.val+paths(c,n) for c in graph[n] if c is not prev])
        return max(paths(n,None) for n in nodes)
    if method=='LowestCommonAncestor':
        t=tree(x)
        while max(a[1:])<t.val or min(a[1:])>t.val: t=t.left if max(a[1:])<t.val else t.right
        return t.val
    if method=='IsValidBST':
        v=inorder(tree(x)); return all(v[i-1]<v[i] for i in range(1,len(v)))
    if method=='KthSmallest': return inorder(tree(x))[a[1]-1]
    if method=='FindWords': return [w for w in dict.fromkeys(a[1]) if word_exists(x,w)]
    if method=='Exist': return word_exists(*a)
    if method=='NumIslands':
        unvisited={(r,c) for r,row in enumerate(x) for c,v in enumerate(row) if v=='1'}; count=0
        while unvisited:
            count+=1; q=[unvisited.pop()]
            while q:
                r,c=q.pop()
                for p in neighbors(r,c,len(x),len(x[0])):
                    if p in unvisited: unvisited.remove(p); q.append(p)
        return count
    if method=='PacificAtlantic':
        out=[]; m,n=len(x),len(x[0])
        for r in range(m):
            for c in range(n):
                seen={(r,c)}; q=[(r,c)]
                while q:
                    i,j=q.pop()
                    for u,v in neighbors(i,j,m,n):
                        if (u,v) not in seen and x[u][v]<=x[i][j]: seen.add((u,v)); q.append((u,v))
                if any(i==0 or j==0 for i,j in seen) and any(i==m-1 or j==n-1 for i,j in seen): out.append([r,c])
        return out
    if method=='CanFinish':
        @lru_cache(None)
        def search(done):
            if len(done)==x: return True
            return any(search(tuple(sorted(done+(v,)))) for v in range(x) if v not in done and all(b in done for aa,b in a[1] if aa==v))
        return search(())
    if method in ('CountComponents','ValidTree'):
        groups=[{i} for i in range(x)]
        for u,v in a[1]:
            left=next(g for g in groups if u in g); right=next(g for g in groups if v in g)
            if left is not right: left.update(right); groups.remove(right)
        return len(groups) if method=='CountComponents' else x>0 and len(groups)==1 and len(a[1])==x-1
    if method=='AlienOrder':
        chars=sorted(set(''.join(x)))
        for order in permutations(chars):
            rank={c:i for i,c in enumerate(order)}; keys=[tuple(rank[c] for c in w) for w in x]
            if keys==sorted(keys): return ''.join(order)
        return ''
    if method=='ClimbStairs':
        return sum(comb(x-t,t) for t in range(x//2+1))
    if method=='Rob':
        return max((sum(x[i] for i in range(len(x)) if mask>>i&1) for mask in range(1<<len(x)) if all(not (mask>>i&3==3) for i in range(len(x)-1)) and not (spec['title']=='House Robber II' and len(x)>1 and mask&1 and mask>>(len(x)-1)&1)),default=0)
    if method=='NumDecodings':
        @lru_cache(None)
        def decode(i):
            if i==len(x): return 1
            if x[i]=='0': return 0
            return decode(i+1)+(decode(i+2) if i+1<len(x) and int(x[i:i+2])<=26 else 0)
        return decode(0)
    if method=='CoinChange':
        distances={0:0}; q=deque([0])
        while q:
            v=q.popleft()
            if v==a[1]: return distances[v]
            for c in x:
                if v+c<=a[1] and v+c not in distances: distances[v+c]=distances[v]+1; q.append(v+c)
        return -1
    if method=='MaxProduct': return max(prod(x[i:j]) for i in range(len(x)) for j in range(i+1,len(x)+1))
    if method=='WordBreak':
        @lru_cache(None)
        def segment(i): return i==len(x) or any(x.startswith(w,i) and segment(i+len(w)) for w in a[1])
        return segment(0)
    if method=='LengthOfLIS': return max((len(sub) for k in range(len(x)+1) for sub in combinations(x,k) if all(sub[i-1]<sub[i] for i in range(1,k))),default=0)
    if method=='UniquePaths': return comb(sum(a)-2,a[0]-1)
    if method=='CanJump':
        seen={0}
        for i in range(len(x)):
            if i in seen: seen.update(range(i+1,min(len(x),i+x[i]+1)))
        return len(x)-1 in seen
    if method=='CombinationSum4':
        @lru_cache(None)
        def count(v): return 1 if v==0 else sum(count(v-c) for c in x if c<=v)
        return count(a[1])
    if method=='MaxSubArray': return max(sum(x[i:j]) for i in range(len(x)) for j in range(i+1,len(x)+1))
    if method=='HammingWeight': return bin(x).count('1')
    if method=='CountBits': return [bin(i).count('1') for i in range(x+1)]
    if method=='ReverseBits': return int(f'{x:032b}'[::-1],2)
    if method=='GetSum': return sum(a)
    raise ValueError(spec['id'])

def equivalent(spec,actual,expected,args):
    if spec['comparison']=='alien':
        words=args[0]; chars=set(''.join(words))
        if expected=='': return actual==''
        if len(actual)!=len(chars) or set(actual)!=chars: return False
        rank={c:i for i,c in enumerate(actual)}; keys=[tuple(rank[c] for c in w) for w in words]
        return keys==sorted(keys)
    if spec['comparison'] in ('unordered','nested'):
        import json
        def normalize(v, nested):
            if not isinstance(v,list): return v
            values=[normalize(x, nested) if nested else x for x in v]
            return sorted(values,key=lambda x:json.dumps(x,sort_keys=True))
        return normalize(actual,spec['comparison']=='nested')==normalize(expected,spec['comparison']=='nested')
    return actual==expected

SPEC={'method': 'TwoSum', 'mode': 'function', 'title': 'Two Sum', 'id': 'blind75_two_sum'}
