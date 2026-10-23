"""All launch permutations and independent role-entry delays; no simulated workers."""
import itertools,json

def oracle(ref,args):return [0,1,2]
def cases(spec):
    args=[spec['example'][0]]+[[list(order),mask,[]] for order in itertools.permutations(range(3)) for mask in range(4)]
    return [dict(arguments=a,expected=[0,1,2]) for a in {json.dumps(a):a for a in args}.values()]
def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('actual')==[0,1,2]
