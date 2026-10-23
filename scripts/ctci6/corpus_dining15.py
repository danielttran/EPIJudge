"""Any safe eating order is accepted; all roles must complete their requested bites."""
import itertools,json,random

def oracle(ref,args):return [role for role in range(args[0]) for _ in range(args[1])]
def cases(spec):
 args=[spec['example'][0]]
 for n in (2,3,4):
  for order in itertools.permutations(range(n)):args.append([n,2,list(order),0,[]])
 for n in (2,5,6):
  args.extend([[n,0,list(reversed(range(n))),0,[]],[n,4,list(reversed(range(n))),(1<<n)-1,[]]])
 rng=random.Random(1503)
 for n in (5,6):
  for _ in range(4):
   order=list(range(n));rng.shuffle(order);args.append([n,3,order,rng.randrange(1<<n),[]])
 return [dict(arguments=a,expected=oracle(spec['ref'],a)) for a in {json.dumps(a):a for a in args}.values()]
def valid_observation(ref,case,observed):
 if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
 actual=observed.get('actual');n,bites=case['arguments'][:2]
 return type(actual) is list and all(type(v) is int and 0<=v<n for v in actual) and len(actual)==n*bites and all(actual.count(role)==bites for role in range(n))
