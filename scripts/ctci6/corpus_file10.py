"""Interval-union absent-value oracle; never expands the fixture file."""
import json

def oracle(ref,args):
    missing=0
    for start,end in sorted(args[0]):
        if start>missing:break
        missing=max(missing,end+1)
    return missing

def cases(spec):
    examples=[[],[[0,0]],[[1,1]],[[0,2],[4,4]],[[2147483647,2147483647]],[[0,7]],[[8,15],[0,6]],[[0,1048575]],[[0,1048574],[1048576,1048580]],[[2147483640,2147483647],[0,7]],[[0,999],[1001,2000]]]
    args=[spec['example'][0]]+[[ranges,small] for ranges in examples for small in (False,True)]
    args += [[ranges,False] for ranges in [[[0,7],[0,7],[9,9]],[[0,0]]*100,[[0,1048575],[0,1048575]]]]
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('10.7',a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual');reads=observed.get('reads');resets=observed.get('resets');ranges,small=case['arguments'];length=sum(end-start+1 for start,end in ranges)
    return type(actual) is int and 0<=actual<=2147483647 and all(not start<=actual<=end for start,end in ranges) and type(reads) is int and 0<=reads<=(2 if small else 1)*(length+1) and type(resets) is int and 0<=resets<=(1 if small else 0)
