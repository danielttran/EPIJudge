"""Independent set/zero-component Minesweeper state oracle."""
import itertools,json,random

def oracle(ref,args):
    board,actions=args;rows,cols=len(board),len(board[0]);mines={(r,c) for r in range(rows) for c in range(cols) if board[r][c]};all_cells=set(itertools.product(range(rows),range(cols)))
    def neighbors(cell):
        r,c=cell
        return {(nr,nc) for nr,nc in all_cells if max(abs(nr-r),abs(nc-c))==1}
    adjacent={cell:len(neighbors(cell)&mines) for cell in all_cells}
    revealed=set();flagged=set();detonated=set();state=0;trace=[]
    def snapshot(accepted):return [state,accepted]+[11 if cell in detonated else adjacent[cell] if cell in revealed else 10 if cell in flagged else 9 for cell in itertools.product(range(rows),range(cols))]
    trace.append(snapshot(0))
    for r,c,kind in actions:
        cell=(r,c);accepted=0
        if state==0 and cell in all_cells:
            if kind==1 and cell not in revealed and cell not in detonated:
                flagged.symmetric_difference_update({cell});accepted=1
            elif kind==0 and cell not in revealed and cell not in flagged:
                accepted=1
                if cell in mines:detonated.add(cell);state=2
                else:
                    # Flood as a fixed point of zero-connected cells, then their safe boundary.
                    reachable={cell};old=set()
                    while old!=reachable:
                        old=reachable.copy()
                        for zero in old:
                            if adjacent[zero]==0:reachable |= neighbors(zero)-mines-flagged
                    revealed |= reachable
                    if revealed==all_cells-mines:state=1
        trace.append(snapshot(accepted))
    return trace

def cases(spec):
    args=[spec['example'][0]]
    for rows,cols in ((1,1),(1,2),(2,1),(2,2)):
        for mask in range((1<<(rows*cols))-1):
            board=[[mask>>(r*cols+c)&1 for c in range(cols)] for r in range(rows)]
            alphabet=[[r,c,kind] for r in range(rows) for c in range(cols) for kind in (0,1)]+[[-1,0,0],[rows,cols,1]]
            for first,second in itertools.product(alphabet,repeat=2):args.append([board,[first,second,first]])
    rng=random.Random(710)
    for _ in range(45):
        rows,cols=rng.randrange(1,8),rng.randrange(1,8);board=[[int(rng.random()<.25) for _ in range(cols)] for _ in range(rows)];board[0][0]=0
        actions=[[rng.randrange(-1,rows+1),rng.randrange(-1,cols+1),rng.randrange(2)] for _ in range(40)]
        actions += [[r,c,0] for r in range(rows) for c in range(cols)]
        args.append([board,actions[:100]])
    for board in ([[0]*12 for _ in range(12)],[[int((r,c)==(11,11)) for c in range(12)] for r in range(12)]):
        args.append([board,[[0,0,1],[1,1,0],[0,0,0],[0,0,1],[0,0,0],[11,11,0]]])
    unique={json.dumps(a):a for a in args};out=[]
    for a in unique.values():
        assert 1<=len(a[0])<=12 and 1<=len(a[0][0])<=12 and len(a[1])<=100
        out.append(dict(arguments=a,expected=oracle(spec['ref'],a)))
    return out

def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and observed.get('actual')==case['expected']
