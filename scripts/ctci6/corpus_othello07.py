"""Independent precomputed-ray Othello rules and deterministic complete game traces."""
import itertools,json,random

def initial(size):
    m=size//2;board={(r,c):0 for r in range(size) for c in range(size)}
    board[m-1,m-1]=board[m,m]=2;board[m-1,m]=board[m,m-1]=1
    return board

def rays(size):
    return {cell:[[p for k in range(1,size) if 0<=(p:=(cell[0]+dr*k,cell[1]+dc*k))[0]<size and 0<=p[1]<size] for dr,dc in itertools.product((-1,0,1),repeat=2) if (dr,dc)!=(0,0)] for cell in itertools.product(range(size),repeat=2)}

def choices(board,color,lines):
    moves={}
    for cell in board:
        if board[cell]:continue
        captured=set()
        for line in lines[cell]:
            own=next((i for i,p in enumerate(line) if board[p]!=3-color),len(line))
            if 0<own<len(line) and board[line[own]]==color:captured.update(line[:own])
        if captured:moves[cell]=captured
    return moves

def oracle(ref,args):
    size,actions=args;board=initial(size);lines=rays(size);turn=1 if choices(board,1,lines) else 0
    def snapshot(accepted):return [turn,accepted,list(board.values()).count(1),list(board.values()).count(2)]+[board[r,c] for r in range(size) for c in range(size)]
    trace=[snapshot(0)]
    for r,c,color in actions:
        accepted=0
        if turn and color==turn:
            captured=choices(board,color,lines).get((r,c))
            if captured:
                for cell in captured|{(r,c)}:board[cell]=color
                accepted=1
                turn=3-color if choices(board,3-color,lines) else color if choices(board,color,lines) else 0
        trace.append(snapshot(accepted))
    return trace

def cases(spec):
    args=[spec['example'][0]]
    for size in (2,4,6,8):
        alphabet=[[r,c,color] for r in range(-1,size+1) for c in range(-1,size+1) for color in (0,1,2,3)]
        for action in alphabet:args.append([size,[action,action]])
    rng=random.Random(708);pass_count=0
    for size,games in ((4,60),(6,12),(8,12)):
        for _ in range(games):
            board=initial(size);lines=rays(size);turn=1;actions=[]
            while turn:
                options=choices(board,turn,lines)
                if not options:break
                cell=rng.choice(sorted(options));color=turn
                # Wrong player and occupied-cell attempts interleaved with complete valid play.
                if rng.randrange(3)==0:actions.append([*cell,3-color])
                for p in options[cell]|{cell}:board[p]=color
                actions.append([*cell,color])
                turn=3-color if choices(board,3-color,lines) else color if choices(board,color,lines) else 0
                if turn==color:pass_count+=1
            actions += [[0,0,1],[-2147483648,2147483647,2]]
            assert len(actions)<=100
            args.append([size,actions])
    assert pass_count>0
    unique={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(spec['ref'],a)) for a in unique.values()]

def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('actual')==case['expected']
