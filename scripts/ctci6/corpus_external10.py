"""Independent ordinal line sorting plus observed resource/ownership contracts."""
import itertools
import json
import random

def oracle(ref,args):return sorted(args[0])
def cases(spec):
    args=[spec['example'][0]]
    for n in range(4):
        for lines in itertools.product(('','b',' A','a'),repeat=n):
            for limit in (2,3,8):args.append([list(lines),limit,[]])
    for lines in (['','',''],['A','a',' A','a ','!','~'],['prefix','pre','prefix '],['z']*17,list(reversed([str(i) for i in range(33)]))):
        for limit in (2,4,1024):args.append([lines,limit,[]])
    rng=random.Random(1006)
    for _ in range(25):
        lines=[''.join(rng.choice(' abABC09~!') for _ in range(rng.randrange(12))) for _ in range(rng.randrange(4,55))]
        args.append([lines,rng.choice((2,3,7,32)),[]])
    args += [[['%05d'%(20000-i) for i in range(20000)],512,[]],[['same']*20000,1024,[]],[[' '*40,'~'*40,'']*100,16,[]]]
    unique={json.dumps(a):a for a in args};result=[]
    for a in unique.values():
        assert len(a[0])<=20000 and 2<=a[1]<=1024 and a[2]==[] and all(len(s)<=40 and all(32<=ord(c)<=126 for c in s) for s in a[0])
        result.append(dict(arguments=a,expected=oracle(spec['ref'],a)))
    return result

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True or observed.get('ownedResult') is not True:return False
    actual=observed.get('actual');n=len(case['arguments'][0]);limit=case['arguments'][1];io_limit=8*n*((max(1,n)-1).bit_length()+2)+128
    if type(actual) is not list or any(type(line) is not str for line in actual) or actual!=case['expected']:return False
    for field,maximum in [('peakRecords',limit),('liveRecords',0),('reads',io_limit),('writes',io_limit),('createdFiles',4*n+64),('maxStreams',16)]:
        if type(observed.get(field)) is not int or not 0<=observed[field]<=maximum:return False
    return True
