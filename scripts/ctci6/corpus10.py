"""Independent sorting/search references and property-aware grading."""
import json
import random
import itertools
from collections import Counter

def key(word):return ''.join(sorted(word))

def oracle(ref,args):
    if ref=='10.1':return sorted(args[0][:args[1]]+args[2])
    if ref=='10.2':return sorted(args[0],key=lambda word:(key(word),word))
    if ref in ('10.3','10.5'):
        if ref=='10.5' and args[1]=='':return -1
        return next((i for i,v in enumerate(args[0]) if v==args[1]),-1)
    if ref=='10.9':
        return next(([r,c] for r,row in enumerate(args[0]) for c,value in enumerate(row) if value==args[1]),[-1,-1])
    if ref=='10.11':
        result=sorted(args[0])
        for i in range(1,len(result)-1,2):result[i],result[i+1]=result[i+1],result[i]
        return result
    raise ValueError(ref)

def cases(spec):
    ref=spec['ref'];rng=random.Random(101000+int(ref.split('.')[1]));args=[spec['example'][0]]
    if ref=='10.1':
        sequences=[list(v) for n in range(5) for v in itertools.combinations_with_replacement((-1,0,1),n)]
        args += [[first+[2147483647]*len(second),len(first),second.copy()] for first in sequences for second in sequences]
        args += [[[0]*5000,0,list(range(5000))],[list(range(5000)),5000,[]],[list(range(0,10000,2))+[-2147483648]*5000,5000,list(range(1,10000,2))],[[-2147483648,2147483647,99,99],2,[-2147483648,2147483647]]]
    elif ref=='10.2':
        args += [[list(words)] for n in range(7) for words in itertools.product(('', 'ab','ba','a'),repeat=n)]
        args += [[['a'*20]*200],[[chr(97+i//26)+chr(97+i%26) for i in range(200)]]]
        for _ in range(45):
            words=[''.join(rng.choice('abcde') for _ in range(rng.randrange(21))) for _ in range(rng.randrange(40))]
            args.append([words])
    elif ref=='10.3':
        args += [[[],target] for target in (-1,0,1)]
        for n in range(1,8):
            for sorted_values in itertools.combinations_with_replacement((-1,0,1,2),n):
                for rotation in range(n):
                    values=list(sorted_values[rotation:]+sorted_values[:rotation])
                    args += [[values,target] for target in (-2,-1,0,1,2,3)]
        args += [[[1]*10000,target] for target in (1,2)]
        args += [[list(range(4999,10000))+list(range(4999)),target] for target in (0,4999,9999,10000)]
        args += [[[2147483647,-2147483648,0],target] for target in (-2147483648,0,2147483647,1)]
    elif ref=='10.5':
        for n in range(8):
            for words in itertools.product(('','a','b'),repeat=n):
                nonempty=[w for w in words if w]
                if nonempty==sorted(nonempty):args += [[list(words),target] for target in ('','a','b','c')]
        args += [[['']*10000,target] for target in ('','a')]
        args += [[['a']+['']*9998+['z'],target] for target in ('a','b','z')]
        args += [[['']*9999+['z'],'z'],[['z']+['']*9999,'z']]
    elif ref=='10.9':
        args += [[[],0],[[[]],1]]
        for rows,cols in ((1,3),(3,1),(2,3),(3,2)):
            for cells in itertools.product((0,1,2),repeat=rows*cols):
                matrix=[list(cells[r*cols:(r+1)*cols]) for r in range(rows)]
                if all(matrix[r][c]<=matrix[r][c+1] for r in range(rows) for c in range(cols-1)) and all(matrix[r][c]<=matrix[r+1][c] for r in range(rows-1) for c in range(cols)):
                    args += [[matrix,target] for target in (-1,0,1,2,3)]
        args += [[[[r+c for c in range(50)] for r in range(50)],target] for target in (0,49,98,99)]
        args += [[[[-2147483648,-2147483648],[2147483647,2147483647]],target] for target in (-2147483648,0,2147483647)]
    else:
        args += [[list(values)] for n in range(8) for values in itertools.product((-1,0,1),repeat=n)]
        args += [[list(range(9999,-1,-1))],[[-2147483648]*10000],[[-2147483648,2147483647]*5000]]
        for _ in range(75):
            args.append([[rng.randrange(-100,101) for _ in range(rng.randrange(50))]])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    if ref in ('10.3','10.5'):
        if type(actual) is not int:return False
        values,target=case['arguments']
        if ref=='10.5' and target=='':return actual==-1
        return case['expected']==-1 if actual==-1 else 0<=actual<len(values) and values[actual]==target
    if ref=='10.2':
        if type(actual) is not list or any(type(w) is not str for w in actual) or Counter(actual)!=Counter(case['arguments'][0]):return False
        closed=set();previous=None
        for word in actual:
            current=key(word)
            if current!=previous:
                if current in closed:return False
                closed.add(current);previous=current
        return True
    if type(actual) is not list or any(type(v) is not int for v in actual):return False
    if ref=='10.9':
        if len(actual)!=2:return False
        if actual==[-1,-1]:return case['expected']==[-1,-1]
        row,col=actual;matrix,target=case['arguments']
        return 0<=row<len(matrix) and 0<=col<len(matrix[row]) and matrix[row][col]==target
    if ref=='10.11':
        return Counter(actual)==Counter(case['arguments'][0]) and all(actual[i]>=actual[i-1] and (i+1==len(actual) or actual[i]>=actual[i+1]) for i in range(1,len(actual),2))
    return actual==case['expected']
