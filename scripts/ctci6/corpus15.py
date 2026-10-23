"""All launch permutations and independent role-entry delays; no simulated workers."""
import itertools,json

def oracle(ref,args):return [0,1,2]
def cases(spec):
    args=[spec['example'][0]]+[[list(order),mask,[]] for order in itertools.permutations(range(3)) for mask in range(4)]
    return [dict(arguments=a,expected=[0,1,2]) for a in {json.dumps(a):a for a in args}.values()]
def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('actual')==[0,1,2]

_order_cases=cases
_order_oracle=oracle
_order_observation=valid_observation
def cases(spec):
    if spec['ref']=='15.7':
        from corpus_fizz15 import cases as run
        return run(spec)
    return _order_cases(spec)
def oracle(ref,args):
    if ref=='15.7':
        from corpus_fizz15 import oracle as run
        return run(ref,args)
    return _order_oracle(ref,args)
def valid_observation(ref,case,observed):
    if ref=='15.7':
        from corpus_fizz15 import valid_observation as run
        return run(ref,case,observed)
    return _order_observation(ref,case,observed)

_fizz_cases=cases
_fizz_oracle=oracle
_fizz_observation=valid_observation
def cases(spec):
    if spec['ref']=='15.3':
        from corpus_dining15 import cases as run
        return run(spec)
    return _fizz_cases(spec)
def oracle(ref,args):
    if ref=='15.3':
        from corpus_dining15 import oracle as run
        return run(ref,args)
    return _fizz_oracle(ref,args)
def valid_observation(ref,case,observed):
    if ref=='15.3':
        from corpus_dining15 import valid_observation as run
        return run(ref,case,observed)
    return _fizz_observation(ref,case,observed)

_dining_cases=cases
_dining_oracle=oracle
_dining_observation=valid_observation
def cases(spec):
    if spec['ref']=='15.4':
        from corpus_locks15 import cases as run
        return run(spec)
    return _dining_cases(spec)
def oracle(ref,args):
    if ref=='15.4':
        from corpus_locks15 import oracle as run
        return run(ref,args)
    return _dining_oracle(ref,args)
def valid_observation(ref,case,observed):
    if ref=='15.4':
        from corpus_locks15 import valid_observation as run
        return run(ref,case,observed)
    return _dining_observation(ref,case,observed)
