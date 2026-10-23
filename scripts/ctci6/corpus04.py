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
