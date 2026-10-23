"""Concrete example outcomes plus property observations for randomized collections."""
from collections import Counter
import json

def oracle(ref,args):
    values=args[0]
    if ref=='17.2':return values[::-1]
    count=args[1]
    return values[:count-1]+[values[count]] if 0<count<len(values) else values[:count]

def cases(spec):
    ref=spec['ref'];args=[spec['example'][0]]
    if ref=='17.2':
        arrays=[list(range(n)) for n in range(6)]+[[7,7,2],[5]*5,[-2147483648,0,2147483647],list(range(52)),list(range(51,-1,-1)),list(range(1000)),[1]*1000]
        args += [[values] for values in arrays]
    else:
        args += [[list(range(n)),count] for n in range(6) for count in range(n+1)]
        args += [[values,count] for values in ([7,7,9],[5]*5,[-2147483648,0,2147483647],[9,3,7,1,5]) for count in range(len(values)+1)]
        args += [[list(range(52)),count] for count in (1,7,26,51)]
        args += [[list(range(1000)),count] for count in (0,1,500,1000)]
        args += [[[7]*1000,500]]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True or observed.get('uniformOk') is not True:return False
    actual=observed.get('actual');values=case['arguments'][0]
    if type(actual) is not list or any(type(v) is not int or not -2147483648<=v<=2147483647 for v in actual):return False
    if ref=='17.2':return Counter(actual)==Counter(values)
    return len(actual)==case['arguments'][1] and not (Counter(actual)-Counter(values))
