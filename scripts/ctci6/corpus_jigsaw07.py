"""Independent oriented-edge constraints and small exact-cover existence oracle."""
import itertools,json,random

def valid_placement(args,actual):
    size,pieces=args
    if type(actual) is not list or len(actual)!=len(pieces):return False
    if any(type(p) is not list or len(p)!=2 or any(type(v) is not int for v in p) or not 0<=p[0]<len(pieces) or not 0<=p[1]<4 for p in actual):return False
    if len({p[0] for p in actual})!=len(pieces):return False
    board=[]
    for index,turn in actual:board.append(pieces[index][-turn:]+pieces[index][:-turn] if turn else pieces[index][:])
    for position,edges in enumerate(board):
        r,c=divmod(position,size)
        if any((value==0)!=boundary for value,boundary in zip(edges,(r==0,c==size-1,r==size-1,c==0))):return False
        if r and edges[0]+board[position-size][2]!=0:return False
        if c and edges[3]+board[position-1][1]!=0:return False
    return True

def oracle(ref,args):
    size,pieces=args
    # Independent column-first exact-cover enumeration, with cached oriented rows.
    options=[(i,t,p[-t:]+p[:-t] if t else p[:]) for i,p in enumerate(pieces) for t in range(4)]
    board={};used=set();positions=[r*size+c for c in range(size) for r in range(size)]
    def visit(k):
        if k==len(positions):return [[board[i][0],board[i][1]] for i in range(len(pieces))]
        pos=positions[k];r,c=divmod(pos,size)
        for i,t,edges in options:
            if i in used:continue
            if any((v==0)!=b for v,b in zip(edges,(r==0,c==size-1,r==size-1,c==0))):continue
            if r and board[pos-size][2][2]+edges[0]!=0:continue
            if c and board[pos-1][2][1]+edges[3]!=0:continue
            board[pos]=(i,t,edges);used.add(i);result=visit(k+1)
            if result is not None:return result
            used.remove(i);del board[pos]
        return None
    result=visit(0)
    return [] if result is None else result

def cases(spec):
    rng=random.Random(706);args=[spec['example'][0],[1,[[0,0,0,0]]],[1,[[0,1,0,0]]]]
    for size in (2,3):
        pieces=[[0]*4 for _ in range(size*size)];label=1
        for r in range(size):
            for c in range(size):
                index=r*size+c
                if c+1<size:pieces[index][1]=label;pieces[index+1][3]=-label;label+=1
                if r+1<size:pieces[index][2]=label;pieces[index+size][0]=-label;label+=1
        for _ in range(55):
            shuffled=[]
            for p in pieces:
                turn=rng.randrange(4);shuffled.append(p[-turn:]+p[:-turn] if turn else p[:])
            rng.shuffle(shuffled);args.append([size,shuffled])
            bad=[p[:] for p in shuffled]
            index=next(i for i,p in enumerate(bad) if any(p));side=next(s for s,v in enumerate(bad[index]) if v);bad[index][side]=1000000
            args.append([size,bad])
    # All input orderings and independent piece turns of a 2x2 assembly.
    base=[[0,1,2,0],[0,0,3,-1],[-2,4,0,0],[-3,0,0,-4]]
    for permutation in itertools.permutations(range(4)):
        for turn in range(4):args.append([2,[(base[i][-turn:]+base[i][:-turn]) if turn else base[i][:] for i in permutation]])
    unique={json.dumps(a):a for a in args};result=[]
    for a in unique.values():
        expected=oracle(spec['ref'],a)
        assert not expected or valid_placement(a,expected)
        result.append(dict(arguments=a,expected=expected))
    return result

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    return actual==[] if case['expected']==[] else valid_placement(case['arguments'],actual)
