"""Ordered-subsequence contract; random examples do not force one coin mapping."""
import itertools
import json
import random

def oracle(ref,args):return args[0][::2]
def cases(spec):
    arrays=[spec['example'][0][0]]
    for n in range(5):arrays.extend(map(list,itertools.product((-1,0,1),repeat=n)))
    arrays += [list(range(n)) for n in (5,6,10,64,1000)]
    arrays += [[7]*n for n in (5,6,64,1000)]
    arrays += [[-2147483648,2147483647,-2147483648,0,2147483647],[-2147483648]*500+[2147483647]*500]
    rng=random.Random(1308)
    arrays += [[rng.randrange(-5,6) for _ in range(rng.randrange(6,35))] for _ in range(12)]
    unique={json.dumps(a):a for a in arrays}
    return [dict(arguments=[a,[]],expected=oracle(spec['ref'],[a,[]])) for a in unique.values()]
def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True or observed.get('uniformOk') is not True:return False
    result=observed.get('actual')
    if type(result) is not list or any(type(v) is not int for v in result):return False
    index=0;values=case['arguments'][0]
    for value in result:
        while index<len(values) and values[index]!=value:index+=1
        if index==len(values):return False
        index+=1
    return True
