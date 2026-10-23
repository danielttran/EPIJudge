"""Trusted finite-map semantics, independent of linked collision-chain logic."""
import itertools
import json
import random

def oracle(ref,args):
    kind,capacity,operations,keys,values=args;table={};seen=[];results=[None]
    for operation,key,value in zip(operations[1:],keys[1:],values[1:]):
        if key not in seen:seen.append(key)
        if operation=='Put':table[key]=value;result=None
        elif operation=='Get':result=table[key] if key in table else {'error':'missing'}
        elif operation=='Remove':
            result=key in table
            if result:del table[key]
        elif operation=='Contains':result=key in table
        else:raise ValueError(operation)
        results.append(result)
    return dict(results=results,finalEntries=[[key,table[key]] for key in seen if key in table])

def make(kind,capacity,actions):
    key_default='' if kind=='text-number' else 0;value_default=0 if kind=='text-number' else ''
    return [kind,capacity,['HashTable']+[a[0] for a in actions],[key_default]+[a[1] for a in actions],[value_default]+[a[2] for a in actions]]

def cases(spec):
    args=[spec['example'][0]];rng=random.Random(712)
    for kind in ('text-number','number-text'):
        keys=['alpha','beta','Alpha','', 'é','é','🌲','01','1'] if kind=='text-number' else [32768,65536,0,-2147483648,2147483647,-1,1,2]
        value_a=0 if kind=='text-number' else '';value_b=7 if kind=='text-number' else '🌲';value_c=-2147483648 if kind=='text-number' else 'replacement'
        alphabet=[('Put',keys[0],value_a),('Put',keys[0],value_c),('Put',keys[1],value_b)]+[(op,key,value_a) for op in ('Get','Remove','Contains') for key in keys[:2]]
        for capacity in (1,2,7):
            for n in range(4):
                for actions in itertools.product(alphabet,repeat=n):args.append(make(kind,capacity,actions))
            args.append(make(kind,capacity,[('Put',key,value_b) for key in keys]+[('Get',key,value_a) for key in keys]+[('Remove',key,value_a) for key in keys[1::2]]+[('Get',key,value_a) for key in keys]+[('Contains',key,value_a) for key in keys]))
        for _ in range(50):
            actions=[]
            for _ in range(70):
                value=rng.randrange(-2147483648,2147483648) if kind=='text-number' else rng.choice(('', '0','🌲','é','é','value'))
                actions.append((rng.choice(('Put','Get','Remove','Contains')),rng.choice(keys),value))
            args.append(make(kind,rng.choice((1,3,11)),actions))
        many=[f'key-{i}' for i in range(1000)] if kind=='text-number' else list(range(-500,500))
        for capacity in (1,31):
            actions=[('Put',key,(i if kind=='text-number' else str(i))) for i,key in enumerate(many)]
            args.append(make(kind,capacity,actions))
            args.append(make(kind,capacity,actions+[('Remove',key,value_a) for key in many]+[('Get',many[0],value_a),('Contains',many[-1],value_a)]))
    unique={json.dumps(a):a for a in args};result=[]
    for a in unique.values():
        assert 1<=len(a[2])<=2005 and len(a[2])==len(a[3])==len(a[4])
        result.append(dict(arguments=a,expected=oracle(spec['ref'],a)))
    return result

def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and type(observed.get('actual')) is dict and observed['actual']==case['expected']
