"""Exact pair-enumeration oracle/property grader for maximum collinear occurrences."""
import itertools
import json
import math
import random

def score(points,line):
    a,b,c=line
    return sum(a*x+b*y+c==0 for x,y in points)

def oracle(ref,args):
    points=args[0]
    if not points:return []
    choices=[]
    for i,(x,y) in enumerate(points):
        for u,v in points[i+1:]:
            if (x,y)==(u,v):continue
            a,b=v-y,x-u;c=-a*x-b*y
            divisor=math.gcd(math.gcd(abs(a),abs(b)),abs(c));a//=divisor;b//=divisor;c//=divisor
            if a<0 or (a==0 and b<0):a,b,c=-a,-b,-c
            choices.append([a,b,c])
    return min(choices,key=lambda line:(-score(points,line),line)) if choices else [1,0,-points[0][0]]

def cases(spec):
    rng=random.Random(1614);args=[spec['example'][0]]
    grid=[[-1,-1],[-1,0],[0,-1],[0,0],[1,1]]
    args += [[[list(point) for point in points]] for n in range(5) for points in itertools.product(grid,repeat=n)]
    args += [[[[0,0],[1000,1],[999,1],[998,1]]],[[[1000,-1000]]*100],[[[i-50,i-50] for i in range(100)]],[[[0,0]]*99+[[1,1]]]]
    args += [[[[rng.randrange(-1000,1001),rng.randrange(-1000,1001)] for _ in range(rng.randrange(30))]] for _ in range(100)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('16.14',a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');points=case['arguments'][0]
    if type(actual) is not list or any(type(v) is not int or not -2147483648<=v<=2147483647 for v in actual):return False
    if not points:return actual==[]
    return len(actual)==3 and (actual[0]!=0 or actual[1]!=0) and score(points,actual)==score(points,case['expected'])
