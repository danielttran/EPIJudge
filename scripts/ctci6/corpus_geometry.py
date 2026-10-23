"""Rational boundary-intersection oracles for independently authored plane tasks."""
from fractions import Fraction as F
import itertools
import json
import math
import random

TOL=1e-6

def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(a,b,p):return cross(a,b,p)==0 and all(min(a[i],b[i])<=p[i]<=max(a[i],b[i]) for i in (0,1))
def segment(points):
    a,b,c,d=points
    common=[p for p in points if on(a,b,p) and on(c,d,p)]
    if common:return list(min(common))
    # A proper crossing has strictly opposite orientation on each line.
    if cross(a,b,c)*cross(a,b,d)>=0 or cross(c,d,a)*cross(c,d,b)>=0:return []
    # Solve implicit line equations with exact rational Cramer's rule.
    aa,bb=b[1]-a[1],a[0]-b[0];cc=aa*a[0]+bb*a[1]
    dd,ee=d[1]-c[1],c[0]-d[0];ff=dd*c[0]+ee*c[1]
    determinant=aa*ee-bb*dd
    return [F(cc*ee-bb*ff,determinant),F(aa*ff-cc*dd,determinant)]

def center(square):return [F(2*square[0]+square[2],2),F(2*square[1]+square[2],2)]
def square_crossings(square,origin,direction):
    x,y,side=square;dx,dy=direction;found=set()
    if dx:
        for edge in (x,x+side):
            parameter=F(edge-origin[0],dx);height=origin[1]+parameter*dy
            if y<=height<=y+side:found.add((F(edge),height))
    if dy:
        for edge in (y,y+side):
            parameter=F(edge-origin[1],dy);horizontal=origin[0]+parameter*dx
            if x<=horizontal<=x+side:found.add((horizontal,F(edge)))
    return found

def square_line(squares):
    first,second=map(center,squares);direction=[second[i]-first[i] for i in (0,1)]
    if direction==[0,0]:direction=[F(0),F(1)]
    points=set().union(*(square_crossings(s,first,direction) for s in squares))
    ordered=sorted(points)
    return list(ordered[0]+ordered[-1])

def oracle(ref,args):return [float(v) for v in (segment(args[0]) if ref=='16.3' else square_line(args[0]))]

def cases(spec):
    rng=random.Random(16031613);ref=spec['ref'];args=[spec['example'][0]]
    if ref=='16.3':
        grid=list(itertools.product(range(2),repeat=2))
        args += [[[list(p) for p in points]] for points in itertools.product(grid,repeat=4)]
        special=[[[0,0],[4,0],[2,0],[6,0]],[[0,0],[0,4],[0,1],[0,3]],[[0,0],[1000,1],[0,1],[999,2]],[[1000,-1000],[-1000,1000],[-1000,-1000],[1000,1000]],[[0,0],[3,3],[0,2],[3,0]],[[1,1],[1,1],[0,0],[2,2]]]
        for points in special:
            for first,second in itertools.product((False,True),repeat=2):args.append([[*(points[1::-1] if first else points[:2]),*(points[:1:-1] if second else points[2:])]])
        args += [[[[rng.randrange(-1000,1001),rng.randrange(-1000,1001)] for _ in range(4)]] for _ in range(300)]
    else:
        squares=[[x,y,side] for x,y,side in itertools.product(range(-1,2),range(-1,2),range(1,4))]
        args += [[[first,second]] for first,second in itertools.product(squares,repeat=2)]
        args += [[[[0,0,1000],[499,499,2]]],[[[-1000,-1000,1000],[1000,1000,1000]]],[[[-1000,1000,1],[1000,-1000,1]]]]
        args += [[[[rng.randrange(-1000,1001),rng.randrange(-1000,1001),rng.randrange(1,1001)] for _ in range(2)]] for _ in range(300)]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(ref,a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    if type(actual) is not list or any(type(v) not in (int,float) or not math.isfinite(v) for v in actual):return False
    if ref=='16.3':
        if not case['expected']:return actual==[]
        if len(actual)!=2:return False
        a,b,c,d=case['arguments'][0]
        # A point segment and every nonparallel pair has a unique intersection.
        if a==b or c==d or (b[0]-a[0])*(d[1]-c[1])!=(b[1]-a[1])*(d[0]-c[0]):
            return all(abs(x-y)<=TOL for x,y in zip(actual,case['expected']))
        # For a positive-length collinear overlap, compare against its projection.
        low=[max(min(a[i],b[i]),min(c[i],d[i])) for i in (0,1)]
        high=[min(max(a[i],b[i]),max(c[i],d[i])) for i in (0,1)]
        parameter_axis=0 if abs(b[0]-a[0])>=abs(b[1]-a[1]) else 1
        parameter=min(high[parameter_axis],max(low[parameter_axis],actual[parameter_axis]))
        t=(parameter-a[parameter_axis])/(b[parameter_axis]-a[parameter_axis])
        point=[a[i]+t*(b[i]-a[i]) for i in (0,1)]
        return all(abs(x-y)<=TOL for x,y in zip(actual,point))
    if len(actual)!=4:return False
    first,second=map(center,case['arguments'][0])
    if first!=second:
        expected=case['expected']
        return all(abs(a-b)<=TOL for a,b in zip(actual,expected)) or all(abs(a-b)<=TOL for a,b in zip(actual,expected[2:]+expected[:2]))
    start,end=actual[:2],actual[2:];direction=[end[i]-start[i] for i in (0,1)];scale=max(map(abs,direction))
    if scale<=2*TOL:return False
    unit=[v/scale for v in direction]
    # A chosen direction defines exact boundary targets through the common center.
    radius=max(s[2] for s in case['arguments'][0])/2
    expected=[float(first[i])-radius*unit[i] for i in (0,1)]+[float(first[i])+radius*unit[i] for i in (0,1)]
    return all(abs(a-b)<=TOL for a,b in zip(actual,expected))
