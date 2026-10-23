"""Morris traversal of private fixture copies establishes original inorder IDs."""
from functools import lru_cache
import itertools
import json
import random

def oracle(ref,args):
    wire=args[0];rows=[row.copy() for row in wire['nodes']];node=wire['selected'];order=[]
    while node!=-1:
        if rows[node][1]==-1:order.append(node);node=rows[node][2];continue
        previous=rows[node][1]
        while rows[previous][2] not in (-1,node):previous=rows[previous][2]
        if rows[previous][2]==-1:rows[previous][2]=node;node=rows[node][1]
        else:rows[previous][2]=-1;order.append(node);node=rows[node][2]
    return dict(head=order[0] if order else -1,order=order,values=[rows[i][0] for i in order],previous=[-1]+order[:-1] if order else [],next=order[1:]+[-1] if order else [],cycle=False)

@lru_cache(None)
def shapes(n):
    if n==0:return (None,)
    return tuple((left,right) for size in range(n) for left in shapes(size) for right in shapes(n-1-size))
def fixture(shape,values):
    rows=[]
    def build(part):
        if part is None:return -1
        index=len(rows);rows.append([0,-1,-1]);rows[index][1]=build(part[0]);rows[index][2]=build(part[1]);return index
    root=build(shape);wire=dict(nodes=rows,selected=root);order=oracle('17.12',[wire])['order']
    for node,value in zip(order,values):rows[node][0]=value
    return wire

def inserted(values):
    rows=[]
    for value in values:
        if not rows:rows.append([value,-1,-1]);continue
        node=0
        while True:
            side=1 if value<rows[node][0] else 2
            if rows[node][side]==-1:rows[node][side]=len(rows);rows.append([value,-1,-1]);break
            node=rows[node][side]
    return dict(nodes=rows,selected=0 if rows else -1)

def cases(spec):
    args=[spec['example'][0]]
    for n in range(7):
        for shape in shapes(n):
            args += [[fixture(shape,values)] for values in itertools.combinations_with_replacement((-1,0,1),n)]
    for values in (range(1000),range(999,-1,-1),[0]*1000,[-2147483648,2147483647,0]):args.append([inserted(values)])
    rng=random.Random(1712)
    for _ in range(100):
        wire=inserted([rng.randrange(-100,101) for _ in range(rng.randrange(1,101))]);permutation=list(range(len(wire['nodes'])));rng.shuffle(permutation);remap={old:new for new,old in enumerate(permutation)}
        args.append([dict(nodes=[[wire['nodes'][old][0],remap.get(wire['nodes'][old][1],-1),remap.get(wire['nodes'][old][2],-1)] for old in permutation],selected=remap[wire['selected']])])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('17.12',a)) for a in distinct.values()]

def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('actual')==case['expected']
