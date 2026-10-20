"""Review checks independent of the answer oracle: types and input preconditions."""
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def require(ok,message):
    if not ok:raise AssertionError(message)

def validate(s,a):
    m=s['method'];mode=s['mode'];require(len(a)==len(s['params'])+(mode=='list_cycle'),'argument count')
    def typed(v,t):
        if t in ('i','l'):return type(v) is int and (-2147483648<=v<=2147483647 if t=='i' else -(1<<63)<=v<(1<<63))
        if t=='s':return isinstance(v,str) and v.isascii()
        if t=='b':return type(v)is bool
        if t in ('list','ai'):return isinstance(v,list) and all(typed(x,'i') for x in v)
        if t in ('lists','aai'):return isinstance(v,list) and all(typed(row,'ai') for row in v)
        if t=='as':return isinstance(v,list) and all(typed(x,'s') for x in v)
        if t=='tree':
            if not isinstance(v,list) or v and (v[0] is None or v[-1] is None):return False
            pending=1
            for x in v:
                if pending<=0 or x is not None and not typed(x,'i'):return False
                pending+=-1 if x is None else 1
            return True
        if t=='graph':return isinstance(v,list) and all(isinstance(row,list) and all(type(x)is int for x in row) for row in v)
        return False
    for v,p in zip(a,s['params']):require(typed(v,p['type']),'invalid '+p['name']+' type/structure')
    x=a[0]
    if m=='TwoSum':require(sum(x[i]+x[j]==a[1] for i,j in combinations(range(len(x)),2))==1,'Two Sum requires exactly one index pair')
    if m=='TopKFrequent':
        counts=sorted(Counter(x).values(),reverse=True);k=a[1];require(1<=k<=len(counts),'top-k range');require(k==len(counts) or counts[k-1]>counts[k],'top-k boundary tie')
    if m in ('CombinationSum','CombinationSum4','CoinChange'):require(len(x)>0 and len(x)==len(set(x)) and min(x)>0,'positive distinct candidates')
    if m=='MissingNumber':require(len(set(x))==len(x) and all(0<=v<=len(x) for v in x),'missing number range/distinctness')
    if m in ('Insert','Merge','EraseOverlapIntervals','CanAttendMeetings','MinMeetingRooms'):
        require(all(len(row)==2 and row[0]<=row[1] for row in x),'interval shape/order')
        if m not in ('Insert','Merge'):require(all(row[0]<row[1] for row in x),'positive-length interval')
        if m=='Insert':require(x==sorted(x) and all(x[i-1][1]<x[i][0] for i in range(1,len(x))),'sorted disjoint closed intervals');require(len(a[1])==2 and a[1][0]<=a[1][1],'new interval')
    if m in ('Rotate','SpiralOrder','SetZeroes','PacificAtlantic','Exist','FindWords','NumIslands'):
        require(bool(x) and len(x[0])>0 and all(len(r)==len(x[0]) for r in x),'nonempty rectangular grid')
        if m=='Rotate':require(len(x)==len(x[0]),'square rotation input')
    if m in ('FindMin','Search'):
        require(len(x)==len(set(x)),'distinct rotated values')
        if x:require(sum(x[i]>x[(i+1)%len(x)] for i in range(len(x)))<=1,'rotated sorted input')
        if m=='FindMin':require(bool(x),'minimum requires nonempty input')
    if m=='MergeTwoLists':require(all(row==sorted(row) for row in a),'sorted list inputs')
    if m=='MergeKLists':require(all(row==sorted(row) for row in x),'sorted list inputs')
    if mode=='list_cycle':require(type(a[1])is int and -1<=a[1]<len(x) if x else a[1]==-1,'cycle setup index')
    if m=='RemoveNthFromEnd':require(1<=a[1]<=len(x),'removal index')
    if m in ('LowestCommonAncestor','KthSmallest'):
        from oracle import tree,inorder
        values=inorder(tree(x));require(values==sorted(set(values)) and values,'strict BST input')
        if m=='LowestCommonAncestor':require(a[1]!=a[2] and a[1] in values and a[2] in values,'LCA nodes must exist')
        else:require(1<=a[1]<=len(values),'kth rank')
    if m=='BuildTree':require(set(x)==set(a[1]) and len(set(x))==len(x)==len(a[1]),'distinct matching traversals')
    if mode in ('trie','dictionary','median'):
        require(len(a[0])==len(a[1]),'operation/value lengths');insertions=0
        allowed={'trie':{'insert','search','startsWith'},'dictionary':{'addWord','search'},'median':{'addNum','findMedian'}}[mode]
        for op,v in zip(*a):
            require(op in allowed,'operation name')
            if mode=='median':
                if op=='addNum':insertions+=1
                else:require(insertions>0,'median of empty stream')
            else:require(all(c in 'abcdefghijklmnopqrstuvwxyz'+('.' if mode=='dictionary' and op=='search' else '') for c in v),'trie alphabet')
    if mode=='graph_clone':
        n=len(x)
        for i,row in enumerate(x):require(len(row)==len(set(row)) and all(1<=v<=n and v!=i+1 and i+1 in x[v-1] for v in row),'simple undirected graph')
        seen={1} if n else set();todo=list(seen)
        while todo:
            for v in x[todo.pop()-1]:
                if v not in seen:seen.add(v);todo.append(v)
        require(len(seen)==n,'clone input must be connected')
    if m in ('CanFinish','CountComponents','ValidTree'):
        require(x>=0 and all(len(row)==2 and all(0<=v<x for v in row) for row in a[1]),'graph endpoints')
        if m=='CountComponents':require(all(u!=v for u,v in a[1]),'components contract excludes loops')
    if m=='WordBreak':require(all(len(w)>0 for w in a[1]),'nonempty dictionary words')
    if m in ('MaxProduct','MaxSubArray','MaxPathSum','CanJump','MaxProfit'):require(bool(x),'nonempty input')
    if m=='MinWindow':require(bool(a[1]),'nonempty target')
    if m in ('HammingWeight','ReverseBits'):require(0<=x<1<<32,'unsigned 32-bit input')
    if m=='NumDecodings':require(bool(x) and all(c in '0123456789' for c in x),'nonempty digits')

if __name__=='__main__':
    from oracle import solve,equivalent
    catalog=json.loads((ROOT/'blind75/catalog.json').read_text());count=0
    for s in catalog:
        cases=json.loads((ROOT/'blind75/cases'/f'{s["id"]}.json').read_text())
        for i,c in enumerate(cases):
            try:validate(s,c['arguments']);require(equivalent(s,solve(s,c['arguments']),c['expected'],c['arguments']),'oracle disagreement')
            except AssertionError as ex:raise AssertionError(f'{s["id"]} row {i+1}: {ex}') from ex
            count+=1
    print(f'PASS independent input preconditions and mathematical oracle: {len(catalog)} problems, {count} cases')
