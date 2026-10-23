"""Independent ordinary FizzBuzz output oracle; execution must use four actual roles."""
import itertools,json

def oracle(ref,args):
 return [('Fizz' if value%3==0 else '')+('Buzz' if value%5==0 else '') or str(value) for value in range(1,args[0]+1)]
def cases(spec):
 args=[spec['example'][0]]+[[15,list(order),0,[]] for order in itertools.permutations(range(4))]
 for limit in (0,1,2,3,4,5,14,16,30,100):args.append([limit,[3,2,1,0],limit%16,[]])
 args += [[16,[1,3,0,2],mask,[]] for mask in range(16)]
 return [dict(arguments=a,expected=oracle(spec['ref'],a)) for a in {json.dumps(a):a for a in args}.values()]
def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('actual')==case['expected']
