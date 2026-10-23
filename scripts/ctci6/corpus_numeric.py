"""Exact-rational arithmetic parsing and sorted-prefix stream oracles."""
import bisect
from fractions import Fraction
import itertools
import json
import math
import random
import re

def calculate(expression):
    tokens=re.findall(r'\d+|[+*/-]',expression)
    # Independent precedence-climbing parser, retaining exact rational values.
    position=0
    def parse(minimum):
        nonlocal position
        left=Fraction(int(tokens[position]));position+=1
        while position<len(tokens):
            op=tokens[position];priority=1 if op in '+-' else 2
            if priority<minimum:break
            position+=1;right=parse(priority+1)
            left=left+right if op=='+' else left-right if op=='-' else left*right if op=='*' else left/right
        return left
    result=parse(1)
    assert position==len(tokens)
    return result

def allowed(expression):
    parts=re.split(r'([+-])',expression);total=Fraction(0)
    for index in range(0,len(parts),2):
        chain=re.split(r'([*/])',parts[index]);value=Fraction(int(chain[0]))
        for i in range(1,len(chain),2):
            number=int(chain[i+1])
            if chain[i]=='/' and number==0:return False
            value=value*number if chain[i]=='*' else value/number
            if abs(value)>1000000:return False
        total=total+value if index==0 or parts[index-1]=='+' else total-value
        if abs(total)>1000000:return False
    return True

def oracle(ref,args):
    if ref=='16.26':return float(calculate(args[0]))
    ordered=[];result=[]
    for value in args[0]:
        bisect.insort(ordered,value);n=len(ordered)
        result.append(float(ordered[n//2]) if n%2 else (ordered[n//2-1]+ordered[n//2])/2)
    return result

def cases(spec):
    ref=spec['ref'];rng=random.Random(16261720);args=[spec['example'][0]]
    if ref=='16.26':
        args += [[str(n)] for n in range(101)]
        args += [[f'{a}{op}{b}{other}{c}'] for a,b,c in itertools.product(range(5),repeat=3) for op,other in itertools.product('+-*/',repeat=2) if (op!='/' or b!=0) and (other!='/' or c!=0)]
        args += [[value] for value in ['1/2','8/4/2','10-3*2','100*100*100','0/100','1/3*3','100-100+1/100','100/3*3-100','+'.join(['100']*51),'*'.join(['1']*51),'/'.join(['100']+['1']*50),'100*100*100/100*100-1000000'] if all(int(v)<=100 for v in re.findall(r'\d+',value)) and allowed(value)]
        for _ in range(300):
            text=str(rng.randrange(101))
            for _ in range(rng.randrange(1,51)):
                op=rng.choice('+-*/');text+=op+str(rng.randrange(1 if op=='/' else 0,101))
            if allowed(text):args.append([text])
    else:
        args += [[list(values)] for n in range(7) for values in itertools.product((-1,0,1),repeat=n)]
        args += [[values] for values in [list(range(10000)),list(range(9999,-1,-1)),[-2147483648,2147483647]*5000,[2147483647]*10000,[-2147483648]*10000]]
        args += [[[rng.randrange(-2147483648,2147483648) for _ in range(rng.randrange(100))]] for _ in range(100)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected']
    def finite(value):return type(value) in (int,float) and math.isfinite(value)
    if ref=='16.26':return finite(actual) and abs(actual-expected)<=max(1e-6,1e-9*abs(expected))
    return type(actual) is list and len(actual)==len(expected) and all(finite(a) and a==b for a,b in zip(actual,expected))
