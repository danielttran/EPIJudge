"""Independent oracles and boundary corpora for the first hard batch."""
import json
import random
import itertools
from functools import lru_cache
from collections import Counter

@lru_cache(None)
def multiples():
    import heapq
    pending=[1];seen={1};result=[]
    for _ in range(501):
        value=heapq.heappop(pending);result.append(value)
        for factor in (3,5,7):
            candidate=value*factor
            if candidate not in seen:seen.add(candidate);heapq.heappush(pending,candidate)
    return result

def oracle(ref,args):
    if ref=='17.1':return (args[0]+args[1]+2147483648)%4294967296-2147483648
    if ref=='17.6':
        digits=str(args[0])
        @lru_cache(None)
        def count(position,tight):
            if position==len(digits):return 1,0
            limit=int(digits[position]) if tight else 9
            ways=twos=0
            for digit in range(limit+1):
                suffix,occurrences=count(position+1,tight and digit==limit)
                ways+=suffix;twos+=occurrences+(suffix if digit==2 else 0)
            return ways,twos
        return count(0,True)[1]
    if ref=='17.9':return multiples()[args[0]]
    if ref=='17.10':
        values=args[0]
        return [value for value,count in Counter(values).items() if count>len(values)//2]
    if ref=='17.16':
        values=args[0]
        if len(values)<=9:
            return max((sum(v for i,v in enumerate(values) if mask&(1<<i))
                        for mask in range(1<<len(values)) if not mask&(mask<<1)),default=0)
        # Independent suffix table for larger boundaries; child uses rolling prefixes.
        suffix=[0]*(len(values)+2)
        for i in range(len(values)-1,-1,-1):suffix[i]=max(suffix[i+1],values[i]+suffix[i+2])
        return suffix[0]
    if ref=='17.21':
        values=args[0];left=[];highest=0
        for h in values:highest=max(highest,h);left.append(highest)
        right=[];highest=0
        for h in reversed(values):highest=max(highest,h);right.append(highest)
        return sum(min(a,b)-h for a,b,h in zip(left,reversed(right),values))
    raise ValueError(ref)

def cases(spec):
    ref=spec['ref'];rng=random.Random(17000+int(ref.split('.')[1]));args=[spec['example'][0]]
    if ref=='17.1':
        boundary=[-2147483648,-2147483647,-65536,-1,0,1,65536,2147483646,2147483647]
        args += [[a,b] for a in boundary for b in boundary]
        args += [[a,b] for a in range(-20,21) for b in range(-20,21)]
        args += [[(1<<bit)-1,1] for bit in range(32)]
        args += [[rng.randrange(-2147483648,2147483648),rng.randrange(-2147483648,2147483648)] for _ in range(300)]
    elif ref=='17.6':
        args += [[n] for n in range(501)]
        for power in range(10):
            for digit in (1,2,3):
                args += [[n] for n in (digit*10**power-1,digit*10**power,digit*10**power+1) if 0<=n<=2147483647]
        args += [[2147483647],[222222222],[1222222222]]+[[rng.randrange(2147483648)] for _ in range(100)]
    elif ref=='17.9':args += [[k] for k in range(501)]
    elif ref=='17.10':
        args += [[list(v)] for n in range(8) for v in itertools.product((-1,0,1),repeat=n)]
        args += [[[-1]*10000],[[2147483647]*5001+[-2147483648]*4999],[[-2147483648]*5000+[2147483647]*5000]]
        args += [[[rng.randrange(-4,5) for _ in range(rng.randrange(50))]] for _ in range(100)]
    elif ref=='17.16':
        args += [[list(v)] for n in range(8) for v in itertools.product((0,15,30),repeat=n)]
        args += [[[1000000]*1000],[[0]*1000],[[1000000,1]*500]]
        args += [[[rng.randrange(1000001) for _ in range(rng.randrange(50))]] for _ in range(70)]
    else:
        args += [[list(v)] for n in range(8) for v in itertools.product((0,1,3),repeat=n)]
        args += [[[100000]+[0]*9998+[100000]],[[0]*10000],[list(range(10000))]]
        args += [[[rng.randrange(100001) for _ in range(rng.randrange(50))]] for _ in range(100)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected']
    return (type(actual) is int and actual==expected) if type(expected) is int else (type(actual) is list and all(type(v) is int for v in actual) and actual==expected)
