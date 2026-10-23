"""Reference trace oracle; the matcher accepts any proven-by-checker uniform mapping."""
import itertools
import json

def oracle(ref,args):
    prefix=args[0];position=0;seed=0x85ebca6b
    def draw():
        nonlocal position,seed
        if position<len(prefix):value=prefix[position];position+=1;return value
        seed=(seed*1664525+1013904223)&0xffffffff
        return seed*5>>32
    while True:
        state=5*draw()+draw()
        if state<21:return state%7

def cases(spec):
    args=[spec['example'][0],[[]]]+[[list(pair)+[0,0]] for pair in itertools.product(range(5),repeat=2)]+[[[4,4]*count+[0,0]] for count in (2,4,8,16)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('16.23',a)) for a in distinct.values()]

def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('uniformOk') is True and type(observed.get('actual')) is int and 0<=observed['actual']<=6
