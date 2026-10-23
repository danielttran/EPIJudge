"""Physical list slicing is an oracle independent of offset indexing."""
import itertools
import json
import random

def oracle(ref,args):
    kind,initial,operations,operands,newValues=args;values=initial.copy();results=[None]
    for operation,operand,newValue in zip(operations[1:],operands[1:],newValues[1:]):
        if operation=='Rotate':
            if values:shift=operand%len(values);values=values[shift:]+values[:shift]
            result=None
        elif operation in ('Get','Set'):
            if not 0<=operand<len(values):result={'error':'index'}
            elif operation=='Get':result=values[operand]
            else:values[operand]=newValue;result=None
        elif operation=='Iterate':result=values.copy()
        elif operation=='IterateTwice':result=[values.copy(),values.copy()]
        else:raise ValueError(operation)
        results.append(result)
    return dict(results=results,finalValues=values)

def make(kind,initial,actions):
    default=0 if kind=='number' else ''
    return [kind,initial,['CircularArray']+[a[0] for a in actions],[0]+[a[1] for a in actions],[default]+[a[2] for a in actions]]

def cases(spec):
    args=[spec['example'][0]];rng=random.Random(709)
    for kind in ('number','text'):
        default=0 if kind=='number' else '';replacement=-2147483648 if kind=='number' else '🌲'
        for initial in ([],[7] if kind=='number' else ['7'],[7,0,7] if kind=='number' else ['','7','🌲']):
            n=len(initial);alphabet=[('Rotate',s,default) for s in (-2147483648,-3,-1,0,1,3,2147483647)]
            alphabet += [(op,index,replacement) for op in ('Get','Set') for index in sorted(set((-1,0,n-1,n)))]
            alphabet += [('Iterate',0,default),('IterateTwice',0,default)]
            for length in range(3):
                for actions in itertools.product(alphabet,repeat=length):args.append(make(kind,initial,actions))
        initial=list(range(1000)) if kind=='number' else [str(i) for i in range(1000)]
        args.append(make(kind,initial,[('Rotate',-2147483648,default),('Get',0,default),('Set',999,replacement),('IterateTwice',0,default),('Get',1000,default),('Set',-1,replacement),('Rotate',2147483647,default),('Iterate',0,default)]))
        for _ in range(35):
            initial=[rng.randrange(-20,21) if kind=='number' else rng.choice(('', 'é','é','🌲','01','1')) for _ in range(rng.randrange(12))]
            actions=[]
            for _ in range(50):
                op=rng.choice(('Rotate','Get','Set','Iterate','IterateTwice'));operand=rng.randrange(-2147483648,2147483648) if op=='Rotate' else rng.randrange(-1,len(initial)+2);value=rng.randrange(-2147483648,2147483648) if kind=='number' else rng.choice(('', '🌲','01','1','é'))
                actions.append((op,operand,value))
            args.append(make(kind,initial,actions))
    unique={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(spec['ref'],a)) for a in unique.values()]
def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and type(observed.get('actual')) is dict and observed['actual']==case['expected']

_previous_oracle=oracle
_previous_cases=cases
_previous_observation=valid_observation
def oracle(ref,args):
    if ref=='7.12':
        from corpus_hash07 import oracle as run
        return run(ref,args)
    return _previous_oracle(ref,args)
def cases(spec):
    if spec['ref']=='7.12':
        from corpus_hash07 import cases as run
        return run(spec)
    return _previous_cases(spec)
def valid_observation(ref,case,observed):
    if ref=='7.12':
        from corpus_hash07 import valid_observation as run
        return run(ref,case,observed)
    return _previous_observation(ref,case,observed)
