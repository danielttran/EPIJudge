"""Independent transitive closure and permutation/heap order oracles."""
import itertools
import heapq
import json
import random

def oracle(ref,args):
    if ref=='4.1':
        n,edges,start,target=args
        reachable=[False]*n;reachable[start]=True
        # Repeated relaxation, not reference BFS adjacency/queue traversal.
        changed=True
        while changed:
            changed=False
            for before,after in edges:
                if reachable[before] and not reachable[after]:reachable[after]=True;changed=True
        return reachable[target]
    n,edges=args
    if n<=6:
        for order in itertools.permutations(range(n)):
            positions={value:i for i,value in enumerate(order)}
            if all(positions[a]<positions[b] for a,b in edges):return list(order)
        return []
    incoming=[set() for _ in range(n)];outgoing=[set() for _ in range(n)]
    for a,b in edges:incoming[b].add(a);outgoing[a].add(b)
    ready=[i for i in range(n) if not incoming[i]];heapq.heapify(ready);result=[]
    while ready:
        node=heapq.heappop(ready);result.append(node)
        for child in outgoing[node]:
            incoming[child].remove(node)
            if not incoming[child]:heapq.heappush(ready,child)
    return result if len(result)==n else []

def cases(spec):
    ref=spec['ref'];rng=random.Random(int(ref.replace('.',''))+40000);args=[spec['example'][0]]
    if ref=='4.1':
        edges=[(a,b) for a in range(3) for b in range(3)]
        args += [[3,[list(edge) for i,edge in enumerate(edges) if mask>>i&1],start,target] for mask in range(1<<len(edges)) for start in range(3) for target in range(3)]
        edges=[(a,b) for a in range(4) for b in range(4) if a!=b]
        args += [[4,[list(edge) for i,edge in enumerate(edges) if mask>>i&1],0,3] for mask in range(1<<len(edges))]
        args += [[1000,[[i,i+1] for i in range(999)],0,999],[1000,[[i,i+1] for i in range(999)],999,0],[1,[],0,0],[2,[[0,0]]*10000,0,1],[2,[[0,1]]*10000,0,1]]
        for _ in range(100):
            n=rng.randrange(1,51);args.append([n,[[rng.randrange(n),rng.randrange(n)] for _ in range(rng.randrange(200))],rng.randrange(n),rng.randrange(n)])
    else:
        edges=[(a,b) for a in range(4) for b in range(4) if a!=b]
        args += [[4,[list(edge) for i,edge in enumerate(edges) if mask>>i&1]] for mask in range(1<<len(edges))]
        args += [[0,[]],[1,[]],[1,[[0,0]]],[200,[]],[200,[[i,i+1] for i in range(199)]],[200,[[i,i+1] for i in range(199)]+[[199,0]]],[2,[[0,1]]*10000],[4,[[0,1],[2,3],[3,2]]]]
        for _ in range(100):
            n=rng.randrange(1,51);args.append([n,[[rng.randrange(n),rng.randrange(n)] for _ in range(rng.randrange(200))]])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    if ref=='4.1':return type(actual) is bool and actual==case['expected']
    if type(actual) is not list or any(type(v) is not int for v in actual):return False
    if not actual:return not case['expected']
    n,edges=case['arguments']
    if len(actual)!=n or set(actual)!=set(range(n)):return False
    positions={node:index for index,node in enumerate(actual)}
    return all(positions[a]<positions[b] for a,b in edges)

_previous_tree_oracle=oracle
_previous_tree_cases=cases
_previous_tree_observation=valid_observation
from functools import lru_cache

@lru_cache(None)
def shapes(size):
    if size==0:return (None,)
    return tuple((left,right) for count in range(size) for left in shapes(count) for right in shapes(size-count-1))

def tree_view(shape,values=None):
    rows=[]
    def build(part):
        if part is None:return -1
        index=len(rows);rows.append([0,-1,-1])
        rows[index][1]=build(part[0]);rows[index][2]=build(part[1]);return index
    selected=build(shape)
    if values is not None:
        for row,value in zip(rows,values):row[0]=value
    return dict(nodes=rows,selected=selected)

def descendants(rows,start):
    result=[];stack=[start] if start!=-1 else []
    while stack:
        node=stack.pop();result.append(node)
        for child in rows[node][1:]:
            if child!=-1:stack.append(child)
    return result

def parents(rows):
    result=[-1]*len(rows)
    for index,row in enumerate(rows):
        for child in row[1:]:
            if child!=-1:result[child]=index
    return result

def inorder(rows,start):
    result=[];stack=[];node=start
    while node!=-1 or stack:
        while node!=-1:stack.append(node);node=rows[node][1]
        node=stack.pop();result.append(node);node=rows[node][2]
    return result

def bst_view(shape):
    view=tree_view(shape)
    for value,index in enumerate(inorder(view['nodes'],view['selected'])):view['nodes'][index][0]=value-3
    return view

def chain(size,value=0,right=False):
    return dict(nodes=[[value(i) if callable(value) else value,-1 if right or i+1==size else i+1,i+1 if right and i+1<size else -1] for i in range(size)],selected=0 if size else -1)

def shuffled(view,rng):
    n=len(view['nodes']);order=list(range(n));rng.shuffle(order);mapping={old:new for new,old in enumerate(order)}
    return dict(nodes=[[view['nodes'][old][0]]+[mapping[child] if child!=-1 else -1 for child in view['nodes'][old][1:]] for old in order],selected=mapping[view['selected']] if view['selected']!=-1 else -1)

def oracle(ref,args):
    if ref not in ('4.4','4.5','4.6','4.8','4.10','4.12'):return _previous_tree_oracle(ref,args)
    view=args[0];rows=view['nodes'];root=view['selected']
    if ref=='4.4':
        def height(start):
            frontier=[start] if start!=-1 else [];result=0
            while frontier:
                result+=1;frontier=[child for node in frontier for child in rows[node][1:] if child!=-1]
            return result
        return all(abs(height(rows[node][1])-height(rows[node][2]))<=1 for node in descendants(rows,root))
    if ref=='4.5':
        return all(all(rows[child][0]<=rows[node][0] for child in descendants(rows,rows[node][1])) and all(rows[child][0]>rows[node][0] for child in descendants(rows,rows[node][2])) for node in descendants(rows,root))
    if ref=='4.6':
        if root==-1:return -1
        parent=parents(rows);component=root
        while parent[component]!=-1:component=parent[component]
        order=inorder(rows,component);index=order.index(root)+1
        return order[index] if index<len(order) else -1
    if ref=='4.8':
        parent=parents(rows);ancestors=set();node=root
        while node!=-1:ancestors.add(node);node=parent[node]
        node=args[1]
        while node!=-1:
            if node in ancestors:return node
            node=parent[node]
        return -1
    if ref=='4.10':
        other=args[1];smallrows=other['nodes'];small=other['selected']
        if small==-1:return True
        for candidate in descendants(rows,root):
            stack=[(candidate,small)];valid=True
            while stack:
                a,b=stack.pop()
                if a==-1 or b==-1:
                    if a!=b:valid=False;break
                elif rows[a][0]!=smallrows[b][0]:valid=False;break
                else:stack.extend(zip(rows[a][1:],smallrows[b][1:]))
            if valid:return True
        return False
    target=args[1];answer=0
    for start in descendants(rows,root):
        stack=[(start,0)]
        while stack:
            node,total=stack.pop();total+=rows[node][0];answer+=total==target
            stack.extend((child,total) for child in rows[node][1:] if child!=-1)
    return answer

def cases(spec):
    ref=spec['ref']
    if ref not in ('4.4','4.5','4.6','4.8','4.10','4.12'):return _previous_tree_cases(spec)
    rng=random.Random(int(ref.replace('.',''))+400000);args=[spec['example'][0]]
    if ref=='4.4':
        args += [[tree_view(shape)] for n in range(8) for shape in shapes(n)]
        args += [[chain(1000)],[chain(1000,right=True)]]
        for _ in range(50):
            view=tree_view(rng.choice(shapes(rng.randrange(1,8))));view['selected']=rng.randrange(len(view['nodes']));args.append([shuffled(view,rng)])
    elif ref in ('4.5','4.12'):
        for n in range(5):
            for shape in shapes(n):
                for values in itertools.product((-1,0,1),repeat=n):
                    view=tree_view(shape,values)
                    args += [[view]] if ref=='4.5' else [[view,target] for target in (-2,-1,0,1,2)]
        if ref=='4.5':
            args += [[chain(1000,0)],[chain(1000,0,right=True)],[chain(1000,lambda i:i-500,right=True)],[{'nodes':[[-2147483648,-1,1],[2147483647,-1,-1]],'selected':0}],[{'nodes':[[2147483647,1,-1],[-2147483648,-1,-1]],'selected':0}],[{'nodes':[[10,1,-1],[5,-1,2],[12,-1,-1]],'selected':1}]]
        else:
            args += [[chain(1000),0],[chain(1000,1000),1000000],[chain(1000,-1000),-1000000],[{'nodes':[[0,1,2],[0,-1,-1],[0,-1,-1]],'selected':0},0],[{'nodes':[[99,1,-1],[1,2,-1],[2,-1,-1]],'selected':1},3]]
    elif ref=='4.6':
        for n in range(6):
            for shape in shapes(n):
                base=bst_view(shape)
                for selected in range(-1,n):args.append([dict(base,selected=selected)])
        args += [[dict(chain(1000,0),selected=i)] for i in (0,1,500,999,-1)]
        args += [[dict(chain(1000,lambda i:i-500,right=True),selected=i)] for i in (0,1,500,999)]
        args += [[{'nodes':[[0,1,2],[-2147483648,-1,-1],[2147483647,-1,-1]],'selected':i}] for i in range(3)]
    elif ref=='4.8':
        for n in range(6):
            for shape in shapes(n):
                base=tree_view(shape,[7]*n)
                args += [[dict(base,selected=a),b] for a in range(-1,n) for b in range(-1,n)]
        forest={'nodes':[[9,1,-1],[9,-1,-1],[9,-1,3],[9,-1,-1]],'selected':0}
        args += [[dict(forest,selected=a),b] for a in range(-1,4) for b in range(-1,4)]
        args += [[dict(chain(1000),selected=a),b] for a,b in ((999,0),(999,500),(998,999),(500,500),(-1,999))]
    else:
        views=[tree_view(shape,values) for n in range(4) for shape in shapes(n) for values in itertools.product((-1,1),repeat=n)]
        args += [[large,small] for large in views for small in views]
        args += [[chain(1000),chain(500)],[chain(1000),chain(500,lambda i:1 if i==499 else 0)],[{'nodes':[[12,-1,-1]],'selected':0},{'nodes':[[2,-1,-1]],'selected':0}],[{'nodes':[[1,1,-1],[1,-1,-1]],'selected':0},{'nodes':[[1,-1,1],[1,-1,-1]],'selected':0}]]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if ref not in ('4.4','4.5','4.6','4.8','4.10','4.12'):return _previous_tree_observation(ref,case,observed)
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected']
    return type(actual) is type(expected) and actual==expected

_previous_output_oracle=oracle
_previous_output_cases=cases
_previous_output_observation=valid_observation

def canonical_minimal(values):
    if not values:return dict(root=-1,nodes=[])
    rows=[];queue=[]
    def append(lower,upper,parent):
        if lower>=upper:return -1
        middle=(lower+upper)//2;index=len(rows);rows.append([values[middle],-1,-1,parent]);queue.append((index,lower,upper,middle));return index
    append(0,len(values),-1);head=0
    while head<len(queue):
        index,lower,upper,middle=queue[head];head+=1
        rows[index][1]=append(lower,middle,index);rows[index][2]=append(middle+1,upper,index)
    return dict(root=0,nodes=rows)

def minimal_valid(values,actual):
    if type(actual) is not dict or type(actual.get('root')) is not int or type(actual.get('nodes')) is not list:return False
    root,rows=actual['root'],actual['nodes'];n=len(values)
    if not n:return root==-1 and rows==[]
    if len(rows)!=n or root<0 or root>=n:return False
    computed=[-1]*n
    for index,row in enumerate(rows):
        if type(row) is not list or len(row)!=4 or any(type(v) is not int for v in row):return False
        if not -2147483648<=row[0]<=2147483647 or any(v< -1 or v>=n for v in row[1:]):return False
        for child in row[1:3]:
            if child!=-1:
                if computed[child]!=-1:return False
                computed[child]=index
    if computed[root]!=-1 or any(computed[i]==-1 for i in range(n) if i!=root):return False
    if any(row[3]!=computed[i] for i,row in enumerate(rows)):return False
    seen=set();frontier=[root];height=0
    while frontier:
        height+=1;following=[]
        for node in frontier:
            if node in seen:return False
            seen.add(node);following += [v for v in rows[node][1:3] if v!=-1]
        frontier=following
    if len(seen)!=n:return False
    ordered=[];stack=[];node=root
    while node!=-1 or stack:
        while node!=-1:stack.append(node);node=rows[node][1]
        node=stack.pop();ordered.append(rows[node][0]);node=rows[node][2]
    least=0;capacity=0
    while capacity<n:least+=1;capacity=2*capacity+1
    return ordered==values and height==least

def oracle(ref,args):
    if ref=='4.2':return canonical_minimal(args[0])
    if ref=='4.3':
        view=args[0];rows=view['nodes'];result=[];stack=[(view['selected'],0)] if view['selected']!=-1 else []
        while stack:
            node,depth=stack.pop()
            if depth==len(result):result.append([])
            result[depth].append(node)
            if rows[node][2]!=-1:stack.append((rows[node][2],depth+1))
            if rows[node][1]!=-1:stack.append((rows[node][1],depth+1))
        return result
    if ref=='4.9':
        view=args[0];rows=view['nodes'];selected=descendants(rows,view['selected']);parent=parents(rows);result=[]
        for order in itertools.permutations(selected):
            positions={node:index for index,node in enumerate(order)}
            if all(parent[node] not in positions or positions[parent[node]]<positions[node] for node in order):result.append([rows[node][0] for node in order])
        return sorted(result)
    return _previous_output_oracle(ref,args)

def cases(spec):
    ref=spec['ref']
    if ref not in ('4.2','4.3','4.9'):return _previous_output_cases(spec)
    rng=random.Random(int(ref.replace('.',''))+4000000);args=[spec['example'][0]]
    if ref=='4.2':
        args += [[[value for bit,value in enumerate(range(-3,4)) if mask>>bit&1]] for mask in range(1<<7)]
        args += [[[-2147483648]],[ [2147483647] ],[[-2147483648,2147483647]],[[-2147483648]+list(range(998))+[2147483647]],[list(range(1000))]]
        args += [[sorted(rng.sample(range(-1000000,1000001),rng.randrange(1001))) ] for _ in range(40)]
    elif ref=='4.3':
        args += [[tree_view(shape)] for n in range(7) for shape in shapes(n)]
        for n in range(5):
            for shape in shapes(n):
                base=tree_view(shape,[7]*n)
                args += [[dict(base,selected=i)] for i in range(-1,n)]
        heap=dict(nodes=[[0,2*i+1 if 2*i+1<1000 else -1,2*i+2 if 2*i+2<1000 else -1] for i in range(1000)],selected=0)
        args += [[chain(1000)],[heap]]
        for _ in range(50):args.append([shuffled(tree_view(rng.choice(shapes(rng.randrange(1,8)))),rng)])
    else:
        args += [[bst_view(shape)] for n in range(7) for shape in shapes(n)]
        args += [[bst_view(rng.choice(shapes(8)))] for _ in range(7)]
        args += [[{'nodes':[[0,1,2],[-2147483648,-1,-1],[2147483647,-1,-1]],'selected':0}],[{'nodes':[[0,1,2],[-2147483648,-1,-1],[2147483647,-1,-1]],'selected':1}]]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if ref not in ('4.2','4.3','4.9'):return _previous_output_observation(ref,case,observed)
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    if ref=='4.2':return minimal_valid(case['arguments'][0],actual)
    if type(actual) is not list or any(type(row) is not list or any(type(v) is not int for v in row) for row in actual):return False
    if ref=='4.3':return actual==case['expected']
    canonical=[tuple(row) for row in actual]
    return len(canonical)==len(set(canonical)) and set(canonical)=={tuple(row) for row in case['expected']}
