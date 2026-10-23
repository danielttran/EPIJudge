"""Independent moderate-task oracles and positive/boundary/negative corpora."""
import itertools
import math
import random
import json

def oracle(ref,args):
    if ref=='16.5':
        n=args[0]
        if n<=250:
            text=str(math.factorial(n));return len(text)-len(text.rstrip('0'))
        power=5;result=0
        while power<=n:result+=n//power;power*=5
        return result
    if ref=='16.7':return max(args)
    if ref=='16.11':
        count,short,long=args
        if count<=12:
            lengths={0}
            for _ in range(count):lengths={v+piece for v in lengths for piece in (short,long)}
            return sorted(lengths)
        return sorted({short*(count-i)+long*i for i in range(count+1)})
    if ref=='16.15':
        guess,secret=args
        remaining=[i for i in range(4) if guess[i]!=secret[i]]
        pseudo=max((sum(guess[i]==secret[j] for i,j in zip(remaining,p)) for p in itertools.permutations(remaining)),default=0)
        return [4-len(remaining),pseudo]
    if ref=='16.16':
        original=args[0];sorted_values=sorted(original)
        mismatches=[i for i in range(len(original)) if original[i]!=sorted_values[i]]
        return [mismatches[0],mismatches[-1]] if mismatches else [-1,-1]
    if ref=='16.17':
        values=args[0]
        return max([0]+[sum(values[a:b]) for a in range(len(values)) for b in range(a+1,len(values)+1)])
    raise ValueError(ref)

def cases(spec):
    ref=spec['ref'];rng=random.Random(int(ref.replace('.',''))+16000);args=[spec['example'][0]]
    if ref=='16.5':
        args += [[n] for n in range(301)]
        power=5
        while power<=2147483647:
            args += [[n] for n in (power-1,power,power+1) if n<=2147483647];power*=5
        args += [[2147483647]]+[[rng.randrange(2147483648)] for _ in range(100)]
    elif ref=='16.7':
        values=[-2147483648,-2147483647,-65536,-1,0,1,65536,2147483646,2147483647]
        args += [[a,b] for a in values for b in values]
        args += [[a,b] for a in range(-16,17) for b in range(-16,17)]
        args += [[rng.randrange(-2147483648,2147483648),rng.randrange(-2147483648,2147483648)] for _ in range(1000)]
    elif ref=='16.11':
        args += [[count,short,long] for count in range(13) for short in range(1,6) for long in range(short,6)]
        args += [[10000,1,100000],[10000,100000,100000],[0,1,100000],[1,99999,100000]]
    elif ref=='16.15':
        codes=[''.join(code) for code in itertools.product('RGBY',repeat=4)]
        for secret in codes:
            args += [[guess,secret] for guess in ('RRRR','GGGG','BBBB','YYYY',secret,secret[::-1],secret[1:]+secret[:1])]
        binary=[''.join(code) for code in itertools.product('RG',repeat=4)]
        args += [[a,b] for a in binary for b in binary]
        args += [[rng.choice(codes),rng.choice(codes)] for _ in range(250)]
    elif ref=='16.16':
        args += [[list(values)] for count in range(7) for values in itertools.product((-1,0,1),repeat=count)]
        args += [[[]],[[0]],[[2147483647,-2147483648]], [list(range(10000))], [list(range(9999,-1,-1))]]
        args += [[[rng.randrange(-100,101) for _ in range(rng.randrange(30))]] for _ in range(100)]
    elif ref=='16.17':
        args += [[list(values)] for count in range(6) for values in itertools.product((-2,-1,0,1,2),repeat=count)]
        args += [[[1000000]*1000],[[-1000000]*1000],[[0]*1000]]
        args += [[[rng.randrange(-100,101) for _ in range(rng.randrange(30))]] for _ in range(100)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected']
    if type(expected) is int:return type(actual) is int and actual==expected
    return type(actual) is list and all(type(v) is int for v in actual) and actual==expected

_previous_oracle=oracle
_previous_cases=cases

def winners(board):
    if not board:return set()
    n=len(board)
    lines=list(board)+[[board[r][c] for r in range(n)] for c in range(n)]
    lines += [[board[i][i] for i in range(n)],[board[i][n-1-i] for i in range(n)]]
    return {line[0] for line in lines if line[0]!=0 and len(set(line))==1}

def oracle(ref,args):
    if ref=='16.1':return [args[1],args[0]]
    if ref=='16.4':
        found=winners(args[0])
        if len(found)>1:raise ValueError('Dual winner outside admitted domain')
        return next(iter(found),0)
    if ref=='16.10':
        people=args[0]
        return max(range(1900,2001),key=lambda year:sum(birth<=year<=death for birth,death in people))
    if ref=='16.19':
        land=args[0]
        # Independent disjoint-set union of water cells, not component DFS.
        parent={(r,c):(r,c) for r,row in enumerate(land) for c,height in enumerate(row) if height==0}
        def find(p):
            while parent[p]!=p:
                parent[p]=parent[parent[p]];p=parent[p]
            return p
        for r,c in parent:
            for dr,dc in itertools.product((-1,0,1),repeat=2):
                neighbor=(r+dr,c+dc)
                if neighbor in parent:
                    a,b=find((r,c)),find(neighbor)
                    if a!=b:parent[a]=b
        from collections import Counter
        return sorted(Counter(find(p) for p in parent).values())
    return _previous_oracle(ref,args)

def cases(spec):
    ref=spec['ref']
    if ref not in ('16.1','16.4','16.10','16.19'):return _previous_cases(spec)
    rng=random.Random(160000+int(ref.split('.')[1]));args=[spec['example'][0]]
    if ref=='16.1':
        boundary=[-2147483648,-2147483647,-1,0,1,2147483646,2147483647]
        args += [[a,b] for a in boundary for b in boundary]
        args += [[a,b] for a in range(-10,11) for b in range(-10,11)]
        args += [[rng.randrange(-2147483648,2147483648),rng.randrange(-2147483648,2147483648)] for _ in range(100)]
    elif ref=='16.4':
        args += [[[]]]
        for n in range(1,4):
            for cells in itertools.product((0,1,2),repeat=n*n):
                board=[list(cells[r*n:(r+1)*n]) for r in range(n)]
                if len(winners(board))<=1:args.append([board])
        args += [[[[1]*50 for _ in range(50)]],[[[0]*50 for _ in range(50)]]]
        board=[[0]*50 for _ in range(50)]
        for i in range(50):board[i][49-i]=2
        args.append([board])
    elif ref=='16.10':
        periods=[[birth,death] for birth in range(1900,1903) for death in range(birth,1903)]
        args += [[list(people)] for n in range(6) for people in itertools.combinations_with_replacement(periods,n)]
        args += [[[[1900,2000]]*1000],[[[2000,2000]]*1000],[[[1900,1900],[2000,2000]]]]
        for _ in range(100):
            births=[rng.randrange(1900,2001) for _ in range(rng.randrange(30))]
            args.append([[[b,rng.randrange(b,2001)] for b in births]])
    else:
        args += [[[]],[[[]]]]
        args += [[[[cells[r*3+c] for c in range(3)] for r in range(3)]] for cells in itertools.product((0,1),repeat=9)]
        args += [[[[0]*50 for _ in range(50)]],[[[10000]*50 for _ in range(50)]], [[[0,1,0,1,0]]]]
        args += [[[[rng.randrange(4) for _ in range(8)] for _ in range(9)]] for _ in range(50)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

_previous_four_oracle=oracle
_previous_four_cases=cases

def oracle(ref,args):
    if ref=='16.2':
        book,queries=args
        return [sum(word.lower()==query.lower() for word in book) for query in queries]
    if ref=='16.6':
        first,second=args
        return min((abs(a-b) for a in first for b in second),default=-1)
    if ref=='16.21':
        first,second=args;s1,s2=sum(first),sum(second)
        for a in first:
            for b in second:
                if s1-a+b==s2-b+a:return [a,b]
        return []
    if ref=='16.24':
        from collections import Counter
        values,target=args;counts=Counter(values);result=[]
        for value in sorted(counts):
            other=target-value
            if value>other:continue
            repetitions=counts[value]//2 if value==other else min(counts[value],counts[other])
            result += [[value,other] for _ in range(repetitions)]
        return result
    return _previous_four_oracle(ref,args)

def cases(spec):
    ref=spec['ref']
    if ref not in ('16.2','16.6','16.21','16.24'):return _previous_four_cases(spec)
    rng=random.Random(int(ref.replace('.',''))+160000);args=[spec['example'][0]]
    if ref=='16.2':
        words=['a','A','b','BB','bb','Ab']
        args += [[list(book),['a','A','b','bb','BB','ab','z']] for n in range(5) for book in itertools.product(words,repeat=n)]
        args += [[[],[]],[['Z']*1000,['z']*1000],[['AbCdEfGhIjKlMnOpQrSt']*1000,['abcdefghijklmnopqrst','X']*500]]
        for _ in range(100):args.append([[rng.choice(words) for _ in range(rng.randrange(40))],[rng.choice(words+['missing']) for _ in range(rng.randrange(40))]])
    elif ref in ('16.6','16.21'):
        small=[list(v) for n in range(4) for v in itertools.product((-1,0,1),repeat=n)]
        args += [[a,b] for a in small for b in small]
        boundaries=[[],[-2147483648],[2147483647],[-2147483648,2147483647],[0],[1],[-1]]
        args += [[a,b] for a in boundaries for b in boundaries]
        args += [[[2147483647]*1000,[-2147483648]*1000],[[2147483647]*1000,[2147483647]*1000],[list(range(1000)),list(range(1000,2000))]]
        for _ in range(100):args.append([[rng.randrange(-100,101) for _ in range(rng.randrange(30))],[rng.randrange(-100,101) for _ in range(rng.randrange(30))]])
        if ref=='16.21':args += [[[0],[-2147483648,2147483647,2147483647,2147483647,3]]] + [[[0],[-2147483648,-2147483648]],[[2147483647],[2147483647,-2147483648,-2147483648]],[[1,3],[2,2]],[[0,1],[0,0]]]
    else:
        args += [[list(v),target] for n in range(6) for v in itertools.product((-2,0,2),repeat=n) for target in (-4,-2,0,2,4)]
        args += [[[2,2,2],4],[[0]*1000,0],[[-2147483648,2147483647,-1,0],-1],[[2147483647,2147483647],-2],[[-2147483648,-2147483648],0]]
        for _ in range(100):args.append([[rng.randrange(-100,101) for _ in range(rng.randrange(100))],rng.randrange(-200,201)])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

_previous_flat_observation=valid_observation
def valid_observation(ref,case,observed):
    if ref!='16.24':return _previous_flat_observation(ref,case,observed)
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    return type(actual) is list and all(type(row) is list and len(row)==2 and all(type(value) is int for value in row) for row in actual) and actual==case['expected']
