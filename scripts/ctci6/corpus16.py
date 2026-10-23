"""Independent moderate-task oracles and positive/boundary/negative corpora."""
import itertools
import math
import random
import json

def oracle(ref,args):
    if ref=='16.5':
        n=args[0]
        if n<=250:
            text=str(math.factorial(n));return len(text)-len(text.rstrip('0'))
        power=5;result=0
        while power<=n:result+=n//power;power*=5
        return result
    if ref=='16.7':return max(args)
    if ref=='16.11':
        count,short,long=args
        if count<=12:
            lengths={0}
            for _ in range(count):lengths={v+piece for v in lengths for piece in (short,long)}
            return sorted(lengths)
        return sorted({short*(count-i)+long*i for i in range(count+1)})
    if ref=='16.15':
        guess,secret=args
        remaining=[i for i in range(4) if guess[i]!=secret[i]]
        pseudo=max((sum(guess[i]==secret[j] for i,j in zip(remaining,p)) for p in itertools.permutations(remaining)),default=0)
        return [4-len(remaining),pseudo]
    if ref=='16.16':
        original=args[0];sorted_values=sorted(original)
        mismatches=[i for i in range(len(original)) if original[i]!=sorted_values[i]]
        return [mismatches[0],mismatches[-1]] if mismatches else [-1,-1]
    if ref=='16.17':
        values=args[0]
        return max([0]+[sum(values[a:b]) for a in range(len(values)) for b in range(a+1,len(values)+1)])
    raise ValueError(ref)

def cases(spec):
    ref=spec['ref'];rng=random.Random(int(ref.replace('.',''))+16000);args=[spec['example'][0]]
    if ref=='16.5':
        args += [[n] for n in range(301)]
        power=5
        while power<=2147483647:
            args += [[n] for n in (power-1,power,power+1) if n<=2147483647];power*=5
        args += [[2147483647]]+[[rng.randrange(2147483648)] for _ in range(100)]
    elif ref=='16.7':
        values=[-2147483648,-2147483647,-65536,-1,0,1,65536,2147483646,2147483647]
        args += [[a,b] for a in values for b in values]
        args += [[a,b] for a in range(-16,17) for b in range(-16,17)]
        args += [[rng.randrange(-2147483648,2147483648),rng.randrange(-2147483648,2147483648)] for _ in range(1000)]
    elif ref=='16.11':
        args += [[count,short,long] for count in range(13) for short in range(1,6) for long in range(short,6)]
        args += [[10000,1,100000],[10000,100000,100000],[0,1,100000],[1,99999,100000]]
    elif ref=='16.15':
        codes=[''.join(code) for code in itertools.product('RGBY',repeat=4)]
        for secret in codes:
            args += [[guess,secret] for guess in ('RRRR','GGGG','BBBB','YYYY',secret,secret[::-1],secret[1:]+secret[:1])]
        binary=[''.join(code) for code in itertools.product('RG',repeat=4)]
        args += [[a,b] for a in binary for b in binary]
        args += [[rng.choice(codes),rng.choice(codes)] for _ in range(250)]
    elif ref=='16.16':
        args += [[list(values)] for count in range(7) for values in itertools.product((-1,0,1),repeat=count)]
        args += [[[]],[[0]],[[2147483647,-2147483648]], [list(range(10000))], [list(range(9999,-1,-1))]]
        args += [[[rng.randrange(-100,101) for _ in range(rng.randrange(30))]] for _ in range(100)]
    elif ref=='16.17':
        args += [[list(values)] for count in range(6) for values in itertools.product((-2,-1,0,1,2),repeat=count)]
        args += [[[1000000]*1000],[[-1000000]*1000],[[0]*1000]]
        args += [[[rng.randrange(-100,101) for _ in range(rng.randrange(30))]] for _ in range(100)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected']
    if type(expected) is int:return type(actual) is int and actual==expected
    return type(actual) is list and all(type(v) is int for v in actual) and actual==expected
