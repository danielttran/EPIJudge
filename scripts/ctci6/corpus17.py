"""Independent oracles and boundary corpora for the first hard batch."""
import json
import random
import itertools
from functools import lru_cache
from collections import Counter

@lru_cache(None)
def multiples():
    import heapq
    pending=[1];seen={1};result=[]
    for _ in range(501):
        value=heapq.heappop(pending);result.append(value)
        for factor in (3,5,7):
            candidate=value*factor
            if candidate not in seen:seen.add(candidate);heapq.heappush(pending,candidate)
    return result

def oracle(ref,args):
    if ref=='17.1':return (args[0]+args[1]+2147483648)%4294967296-2147483648
    if ref=='17.6':
        digits=str(args[0])
        @lru_cache(None)
        def count(position,tight):
            if position==len(digits):return 1,0
            limit=int(digits[position]) if tight else 9
            ways=twos=0
            for digit in range(limit+1):
                suffix,occurrences=count(position+1,tight and digit==limit)
                ways+=suffix;twos+=occurrences+(suffix if digit==2 else 0)
            return ways,twos
        return count(0,True)[1]
    if ref=='17.9':return multiples()[args[0]]
    if ref=='17.10':
        values=args[0]
        return [value for value,count in Counter(values).items() if count>len(values)//2]
    if ref=='17.16':
        values=args[0]
        if len(values)<=9:
            return max((sum(v for i,v in enumerate(values) if mask&(1<<i))
                        for mask in range(1<<len(values)) if not mask&(mask<<1)),default=0)
        # Independent suffix table for larger boundaries; child uses rolling prefixes.
        suffix=[0]*(len(values)+2)
        for i in range(len(values)-1,-1,-1):suffix[i]=max(suffix[i+1],values[i]+suffix[i+2])
        return suffix[0]
    if ref=='17.21':
        values=args[0];left=[];highest=0
        for h in values:highest=max(highest,h);left.append(highest)
        right=[];highest=0
        for h in reversed(values):highest=max(highest,h);right.append(highest)
        return sum(min(a,b)-h for a,b,h in zip(left,reversed(right),values))
    raise ValueError(ref)

def cases(spec):
    ref=spec['ref'];rng=random.Random(17000+int(ref.split('.')[1]));args=[spec['example'][0]]
    if ref=='17.1':
        boundary=[-2147483648,-2147483647,-65536,-1,0,1,65536,2147483646,2147483647]
        args += [[a,b] for a in boundary for b in boundary]
        args += [[a,b] for a in range(-20,21) for b in range(-20,21)]
        args += [[(1<<bit)-1,1] for bit in range(32)]
        args += [[rng.randrange(-2147483648,2147483648),rng.randrange(-2147483648,2147483648)] for _ in range(300)]
    elif ref=='17.6':
        args += [[n] for n in range(501)]
        for power in range(10):
            for digit in (1,2,3):
                args += [[n] for n in (digit*10**power-1,digit*10**power,digit*10**power+1) if 0<=n<=2147483647]
        args += [[2147483647],[222222222],[1222222222]]+[[rng.randrange(2147483648)] for _ in range(100)]
    elif ref=='17.9':args += [[k] for k in range(501)]
    elif ref=='17.10':
        args += [[list(v)] for n in range(8) for v in itertools.product((-1,0,1),repeat=n)]
        args += [[[-1]*10000],[[2147483647]*5001+[-2147483648]*4999],[[-2147483648]*5000+[2147483647]*5000]]
        args += [[[rng.randrange(-4,5) for _ in range(rng.randrange(50))]] for _ in range(100)]
    elif ref=='17.16':
        args += [[list(v)] for n in range(8) for v in itertools.product((0,15,30),repeat=n)]
        args += [[[1000000]*1000],[[0]*1000],[[1000000,1]*500]]
        args += [[[rng.randrange(1000001) for _ in range(rng.randrange(50))]] for _ in range(70)]
    else:
        args += [[list(v)] for n in range(8) for v in itertools.product((0,1,3),repeat=n)]
        args += [[[100000]+[0]*9998+[100000]],[[0]*10000],[list(range(10000))]]
        args += [[[rng.randrange(100001) for _ in range(rng.randrange(50))]] for _ in range(100)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected']
    return (type(actual) is int and actual==expected) if type(expected) is int else (type(actual) is list and all(type(v) is int for v in actual) and actual==expected)

_previous_oracle=oracle
_previous_cases=cases

def oracle(ref,args):
    if ref=='17.5':
        text=args[0];best=0;answer=[-1,-1]
        if len(text)>100:
            groups={0:[-1]};balance=0
            for i,char in enumerate(text):
                balance += -1 if char.isdigit() else 1
                groups.setdefault(balance,[]).append(i)
            for positions in groups.values():
                length=positions[-1]-positions[0];start=positions[0]+1
                if length>best or length==best and length>0 and start<answer[0]:best=length;answer=[start,positions[-1]]
            return answer
        for left in range(len(text)):
            balance=0
            for right in range(left,len(text)):
                balance+=-1 if text[right].isdigit() else 1
                if balance==0 and right-left+1>best:best=right-left+1;answer=[left,right]
        return answer
    if ref=='17.14':return sorted(args[0])[:args[1]]
    if ref=='17.18':
        big,small=args;needed=set(small);best=len(big)+1;answer=[-1,-1]
        if not needed:return answer
        if len(big)>100:
            from bisect import bisect_left
            positions={v:[] for v in small}
            for i,value in enumerate(big):
                if value in positions:positions[value].append(i)
            for left in range(len(big)):
                found=[]
                for indexes in positions.values():
                    at=bisect_left(indexes,left)
                    if at==len(indexes):break
                    found.append(indexes[at])
                if len(found)!=len(small):break
                right=max(found)
                if right-left+1<best:best=right-left+1;answer=[left,right]
            return answer
        for left in range(len(big)):
            seen=set()
            for right in range(left,len(big)):
                seen.add(big[right])
                if needed<=seen:
                    if right-left+1<best:best=right-left+1;answer=[left,right]
                    break
        return answer
    if ref=='17.19':return sorted(set(range(1,len(args[0])+3))-set(args[0]))
    if ref=='17.23':
        matrix=args[0];n=len(matrix)
        for size in range(n,0,-1):
            for row in range(n-size+1):
                for col in range(n-size+1):
                    if all(matrix[row][c]==0 and matrix[row+size-1][c]==0 for c in range(col,col+size)) and all(matrix[r][col]==0 and matrix[r][col+size-1]==0 for r in range(row,row+size)):
                        return [row,col,size]
        return []
    if ref=='17.24':
        matrix=args[0];rows=len(matrix);cols=len(matrix[0]) if rows else 0
        if not rows or not cols:return []
        prefix=[[0]*(cols+1) for _ in range(rows+1)]
        for r in range(rows):
            for c in range(cols):prefix[r+1][c+1]=matrix[r][c]+prefix[r][c+1]+prefix[r+1][c]-prefix[r][c]
        best=None;answer=[]
        for top in range(rows):
            for bottom in range(top,rows):
                for left in range(cols):
                    for right in range(left,cols):
                        value=prefix[bottom+1][right+1]-prefix[top][right+1]-prefix[bottom+1][left]+prefix[top][left]
                        if best is None or value>best:best=value;answer=[value,top,left,bottom,right]
        return answer
    return _previous_oracle(ref,args)

def cases(spec):
    ref=spec['ref']
    if ref not in ('17.5','17.14','17.18','17.19','17.23','17.24'):return _previous_cases(spec)
    rng=random.Random(171000+int(ref.split('.')[1]));args=[spec['example'][0]]
    if ref=='17.5':
        args += [[''.join(chars)] for n in range(10) for chars in itertools.product('A1',repeat=n)]
        args += [['aZ09B1'],['A'*5000+'1'*5000],['z'*10000],['0'*10000]]
        args += [[''.join(rng.choice('aBZ019') for _ in range(rng.randrange(35)))] for _ in range(80)]
    elif ref=='17.14':
        args += [[list(values),k] for n in range(7) for values in itertools.product((-1,0,1),repeat=n) for k in range(n+1)]
        args += [[[-2147483648,2147483647,0,-2147483648],k] for k in range(5)]
        args += [[list(range(9999,-1,-1)),k] for k in (0,1,5000,10000)]
        for _ in range(80):
            values=[rng.randrange(-30,31) for _ in range(rng.randrange(35))]
            args.append([values,rng.randrange(len(values)+1)])
    elif ref=='17.18':
        targets=[list(v) for n in range(4) for v in itertools.combinations((0,1,2),n)]
        args += [[list(big),small] for n in range(6) for big in itertools.product((0,1,2),repeat=n) for small in targets]
        args += [[list(range(10000)),[9998,9999]],[[0]*10000,[0]],[[0]*10000,[1]], [[2147483647,0,-2147483648],[-2147483648,2147483647]]]
    elif ref=='17.19':
        for n in range(2,16):
            for a,b in itertools.combinations(range(1,n+1),2):
                values=[v for v in range(1,n+1) if v not in (a,b)];rng.shuffle(values);args.append([values])
        args += [[[v for v in range(1,100001) if v not in missing]] for missing in ((1,100000),(33333,66666),(99999,100000))]
        for _ in range(60):
            n=rng.randrange(2,201);missing=set(rng.sample(range(1,n+1),2));values=[v for v in range(1,n+1) if v not in missing];rng.shuffle(values);args.append([values])
    elif ref=='17.23':
        args += [[[]]]
        for n in range(1,4):
            args += [[[[cells[r*n+c] for c in range(n)] for r in range(n)]] for cells in itertools.product((0,1),repeat=n*n)]
        args += [[[[0]*40 for _ in range(40)]],[[[1]*40 for _ in range(40)]]]
        args += [[[[0 if r in (0,39) or c in (0,39) else 1 for c in range(40)] for r in range(40)]]]
        args += [[[[rng.randrange(2) for _ in range(7)] for _ in range(7)]] for _ in range(40)]
    else:
        args += [[[]],[[[]]]]
        for rows,cols in ((1,1),(1,3),(3,1),(2,3),(3,2)):
            args += [[[[cells[r*cols+c] for c in range(cols)] for r in range(rows)]] for cells in itertools.product((-1,0,1),repeat=rows*cols)]
        args += [[[[1000000]*30 for _ in range(30)]],[[[-1000000]*30 for _ in range(30)]],[[[0]*30 for _ in range(30)]]]
        args += [[[[rng.randrange(-15,16) for _ in range(5)] for _ in range(4)]] for _ in range(45)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

_previous_text_oracle=oracle
_previous_text_cases=cases

def oracle(ref,args):
    if ref=='17.11':
        words,first,second=args
        return min((abs(i-j) for i,word in enumerate(words) if word==first for j,other in enumerate(words) if other==second),default=-1)
    if ref=='17.15':
        from functools import lru_cache
        words=args[0]
        for candidate in sorted(set(words),key=lambda word:(-len(word),word)):
            components=set(words)-{candidate}
            @lru_cache(None)
            def spell(suffix):
                if suffix in components:return True
                return any(suffix[:cut] in components and spell(suffix[cut:]) for cut in range(1,len(suffix)))
            if spell(candidate):return candidate
        return ''
    if ref=='17.17':
        import re
        text,patterns=args
        return [[m.start() for m in re.finditer('(?='+re.escape(pattern)+')',text)] for pattern in patterns]
    return _previous_text_oracle(ref,args)

def cases(spec):
    ref=spec['ref']
    if ref not in ('17.11','17.15','17.17'):return _previous_text_cases(spec)
    rng=random.Random(int(ref.replace('.',''))+170000);args=[spec['example'][0]]
    if ref=='17.11':
        args += [[list(words),'a','b'] for n in range(7) for words in itertools.product(('a','b','x'),repeat=n)]
        args += [[['a']*9999+['b'],'a','b'],[['a']+['x']*9998+['b'],'a','b'],[['x']*10000,'a','b']]
        for _ in range(100):args.append([[rng.choice(('a','b','x')) for _ in range(rng.randrange(100))],'a','b'])
    elif ref=='17.15':
        vocabulary=['a','b','ab','ba','aa','aba','bab']
        args += [[[word for i,word in enumerate(vocabulary) if mask>>i&1]] for mask in range(1<<len(vocabulary))]
        args += [[['cat','cat']],[['cat','dog','dogcat','catdog']],[['a','a'*40]],[['a'*40]*200],[['a','a'*40]+['b'*39+'c']*198]]
        for _ in range(100):args.append([[''.join(rng.choice('abc') for _ in range(rng.randrange(1,11))) for _ in range(rng.randrange(30))]])
    else:
        patterns=[''.join(chars) for n in range(4) for chars in itertools.product('ab',repeat=n)]+['c','aba','']
        args += [[''.join(text),patterns] for n in range(7) for text in itertools.product('ab',repeat=n)]
        args += [['',[]],['a'*1000,['a'*20]*100],['ab'*500,['ab','ba','']*33+['x']]]
        for _ in range(100):args.append([''.join(rng.choice('abc') for _ in range(rng.randrange(50))),[''.join(rng.choice('abc') for _ in range(rng.randrange(10))) for _ in range(rng.randrange(15))]])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

_previous_numeric_observation=valid_observation

def valid_observation(ref,case,observed):
    if ref not in ('17.15','17.17'):return _previous_numeric_observation(ref,case,observed)
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    if ref=='17.15':return type(actual) is str and actual==case['expected']
    return type(actual) is list and all(type(row) is list and all(type(value) is int for value in row) for row in actual) and actual==case['expected']

_previous_structured_oracle=oracle
_previous_structured_cases=cases
_previous_structured_observation=valid_observation
STRUCTURED_REFS=('17.8','17.13','17.22','17.25','17.26')

def oracle(ref,args):
    if ref=='17.8':
        people=args[0]
        @lru_cache(None)
        def ending(index):
            candidates=[ending(before)+(index,) for before in range(len(people)) if people[before][0]<people[index][0] and people[before][1]<people[index][1]]
            return min(candidates,key=lambda row:(-len(row),row)) if candidates else (index,)
        return list(min((ending(i) for i in range(len(people))),key=lambda row:(-len(row),row),default=()))
    if ref=='17.13':
        text,dictionary=args;words=set(dictionary)
        @lru_cache(None)
        def split(start):
            if start==len(text):return 0,()
            choices=[]
            for end in range(start+1,len(text)+1):
                word=text[start:end];cost,tail=split(end);choices.append((cost+(0 if word in words else len(word)),(word,)+tail))
            return min(choices)
        return list(split(0)[1])
    if ref=='17.22':
        start,stop,dictionary=args;words=sorted({word for word in dictionary if len(word)==len(start)})
        queue=[start];previous={start:None}
        for word in queue:
            if word==stop:
                path=[]
                while word is not None:path.append(word);word=previous[word]
                return path[::-1]
            for candidate in words:
                if candidate not in previous and sum(a!=b for a,b in zip(word,candidate))==1:previous[candidate]=word;queue.append(candidate)
        return []
    if ref=='17.25':
        words=set(args[0]);maximum=max(map(len,words),default=0)
        groups={length:sorted(word for word in words if len(word)==length) for length in range(1,maximum+1)}
        for area in range(maximum*maximum,0,-1):
            for height in range(1,maximum+1):
                if area%height:continue
                width=area//height
                if width>maximum or not groups[width] or not groups[height]:continue
                for rows in itertools.product(groups[width],repeat=height):
                    if all(''.join(row[column] for row in rows) in words for column in range(width)):return list(rows)
        return []
    if ref=='17.26':
        ids,documents=args;sets=list(map(set,documents));rows=[]
        for left in range(len(ids)):
            for right in range(left+1,len(ids)):
                intersection=len(sets[left]&sets[right])
                if intersection:rows.append([min(ids[left],ids[right]),max(ids[left],ids[right]),intersection,len(sets[left]|sets[right])])
        return sorted(rows)
    return _previous_structured_oracle(ref,args)

def cases(spec):
    ref=spec['ref']
    if ref not in STRUCTURED_REFS:return _previous_structured_cases(spec)
    rng=random.Random(int(ref.replace('.',''))+17000000);args=[spec['example'][0]]
    if ref=='17.8':
        dimensions=[(a,b) for a in range(1,4) for b in range(1,4)]
        args += [[[list(person) for person in people]] for n in range(4) for people in itertools.product(dimensions,repeat=n)]
        args += [[[list(person) for person in people]] for people in itertools.product(((1,1),(1,2),(2,1),(2,2)),repeat=4)]
        args += [[[[i+1,i+1] for i in range(200)]],[[[200-i,200-i] for i in range(200)]],[[[1,1]]*200],[[[1,i+1] for i in range(200)]],[[[i+1,1] for i in range(200)]],[[[1,1],[1000000,1000000]]]]
        args += [[[[rng.randrange(1,101),rng.randrange(1,101)] for _ in range(rng.randrange(30))]] for _ in range(100)]
    elif ref=='17.13':
        vocab=['a','b','ab','ba','aba'];texts=[''.join(v) for n in range(6) for v in itertools.product('ab',repeat=n)]
        args += [[text,[word for index,word in enumerate(vocab) if mask>>index&1]] for mask in range(1<<len(vocab)) for text in texts]
        words=['a'*20]+[''.join(rng.choice('bcdef') for _ in range(20)) for _ in range(199)]
        args += [['x'*200,[]],['a'*200,words],['abc',['ab','bc']],['abcabc',['abc']]]
    elif ref=='17.22':
        vocabulary=[''.join(v) for v in itertools.product('ab',repeat=3)]
        for mask in range(1,1<<len(vocabulary)):
            words=[word for index,word in enumerate(vocabulary) if mask>>index&1]
            args += [[start,stop,words] for start in words for stop in words]
        large=[''.join(v) for v in itertools.product('abcdef',repeat=4)][:1000]
        args += [[large[0],large[-1],large],['cat','dog',['cat','dog','cat','cot','cog','it','elephant']],['a','a',['a']],['cat','dog',['cat','dog']]]
    elif ref=='17.25':
        vocab=['a','b','aa','ab','ba','bb']
        args += [[[word for index,word in enumerate(vocab) if mask>>index&1]] for mask in range(1<<len(vocab))]
        vocab=[''.join(v) for v in itertools.product('ab',repeat=3)]
        args += [[[word for index,word in enumerate(vocab) if mask>>index&1]] for mask in range(1<<len(vocab))]
        args += [[['aa']],[['ab']],[['ab','a','b']],[[''.join(v) for v in itertools.product('ab',repeat=5)][:20]]]
        pool=[''.join(v) for n in range(1,4) for v in itertools.product('abc',repeat=n)]
        args += [[rng.sample(pool,rng.randrange(6))] for _ in range(50)]
    else:
        subsets=[[value for bit,value in enumerate((-1,0,1)) if mask>>bit&1] for mask in range(8)]
        args += [[[10,-2,7][:n],list(docs)] for n in range(4) for docs in itertools.product(subsets,repeat=n)]
        ids=[-2147483648,2147483647]+rng.sample(range(-2000000000,2000000000),198)
        args += [[ids,[list(range(200)) for _ in range(200)]],[ids,[[i] for i in range(200)]],[[-2147483648,2147483647],[[-2147483648,2147483647],[-2147483648]]],[[20,10],[[1,2,3],[2,3,4]]]]
        for _ in range(100):
            n=rng.randrange(15);args.append([rng.sample(range(-100,101),n),[rng.sample(range(-20,21),rng.randrange(15)) for _ in range(n)]])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if ref not in STRUCTURED_REFS:return _previous_structured_observation(ref,case,observed)
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');expected=case['expected'];args=case['arguments']
    if type(actual) is not list:return False
    if ref=='17.8':
        people=args[0]
        return all(type(v) is int for v in actual) and len(actual)==len(expected) and len(set(actual))==len(actual) and all(0<=v<len(people) for v in actual) and all(people[a][0]<people[b][0] and people[a][1]<people[b][1] for a,b in zip(actual,actual[1:]))
    if ref=='17.26':return all(type(row) is list and all(type(v) is int for v in row) for row in actual) and actual==expected
    if any(type(word) is not str for word in actual):return False
    if ref=='17.13':
        text,dictionary=args;words=set(dictionary)
        return all(actual) and ''.join(actual)==text and sum(len(word) for word in actual if word not in words)==sum(len(word) for word in expected if word not in words) if actual else text==''
    if ref=='17.22':
        if not actual:return not expected
        start,stop,dictionary=args;words=set(dictionary)
        return actual[0]==start and actual[-1]==stop and len(set(actual))==len(actual) and all(word in words for word in actual) and all(len(a)==len(b) and sum(x!=y for x,y in zip(a,b))==1 for a,b in zip(actual,actual[1:]))
    if not actual:return not expected
    if not expected:return False
    words=set(args[0]);height=len(actual);width=len(actual[0])
    return width>0 and all(len(row)==width and row in words for row in actual) and all(''.join(row[column] for row in actual) in words for column in range(width)) and height*width==len(expected)*len(expected[0])
