"""Set-difference oracle for hidden consecutive-range bit-only queries."""
import itertools
import json
import random

def oracle(ref,args):return next(iter(set(range(len(args[0])+1))-set(args[0])))
def cases(spec):
    args=[spec['example'][0]];rng=random.Random(1704)
    for n in range(7):
        for missing in range(n+1):
            values=[v for v in range(n+1) if v!=missing]
            args += [[list(order)] for order in itertools.permutations(values)]
    for n in (7,8,15,16,31,32,63,64,127,128,9999,10000):
        for missing in {0,1,n//2,n-1,n}:
            values=[v for v in range(n+1) if v!=missing];rng.shuffle(values);args.append([values])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('17.4',a)) for a in distinct.values()]
def valid_observation(ref,case,observed):
    return isinstance(observed,dict) and observed.get('mutationOk') is True and type(observed.get('actual')) is int and observed['actual']==case['expected'] and type(observed.get('probes')) is int and 0<=observed['probes']<=4*len(case['arguments'][0])+32
