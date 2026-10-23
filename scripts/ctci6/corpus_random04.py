"""Multiset operation semantics independent of any BST shape or private cache."""
from collections import Counter
import itertools
import json

def transitions(args):
    operations,arguments=args;counts=Counter();total=0;results=[];changes=[]
    for operation,values in zip(operations,arguments):
        added=[];removed=[]
        if operation=='RandomBst':result=None
        elif operation=='Insert':counts[values[0]]+=1;total+=1;added=[values[0]];result=None
        elif operation=='Delete':
            result=counts[values[0]]>0
            if result:
                counts[values[0]]-=1;total-=1;removed=[values[0]]
                if counts[values[0]]==0:del counts[values[0]]
        elif operation=='Find':result=[values[0]] if counts[values[0]]>0 else []
        elif operation=='GetRandomNode':
            ordered=sorted(counts.elements());result=[ordered[len(ordered)//2]] if ordered else []
        else:raise ValueError('Unknown tree operation '+operation)
        results.append(result);changes.append(dict(added=added,removed=removed,count=total))
    return dict(results=results,finalValues=sorted(counts.elements())),changes

def oracle(ref,args):return transitions(args)[0]
def transcript(actions):
    operations=['RandomBst'];arguments=[[]]
    for operation,value in actions:operations.append(operation);arguments.append([] if operation=='GetRandomNode' else [value])
    return [operations,arguments]

def cases(spec):
    args=[spec['example'][0]];alphabet=[(operation,value) for operation in ('Insert','Delete','Find') for value in (0,1)]
    args += [transcript(actions) for size in range(5) for actions in itertools.product(alphabet,repeat=size)]
    for size in range(4):
        for values in itertools.product((-1,0,1),repeat=size):
            args.append(transcript([('Insert',v) for v in values]+[('Find',0),('GetRandomNode',None),('Delete',0),('Find',0),('GetRandomNode',None)]))
    for values,deletions in [([5,1,2,3],[1,5]),([4,2,6,1,3,5,5,7],[4,5]),([7,7,7],[7,7]),([-2147483648,2147483647,0,-2147483648],[-2147483648,2147483647]),(list(range(1000)),[500,0]),(list(range(999,-1,-1)),[500,999]),([7]*1000,[7,7])]:
        actions=[('Insert',v) for v in values]+[('GetRandomNode',None)]
        for value in deletions:actions += [('Delete',value),('Find',value),('GetRandomNode',None)]
        args.append(transcript(actions))
    args.append(transcript([('Insert',v) for v in range(1000)]+[('Delete',v) for v in range(1000)]+[('GetRandomNode',None)]))
    unique={json.dumps(a):a for a in args};result=[]
    for arguments in unique.values():
        operations,values=arguments
        assert operations[0]=='RandomBst' and values[0]==[] and len(operations)==len(values)<=2005 and operations.count('GetRandomNode')<=3
        _,changes=transitions(arguments);assert all(0<=row['count']<=1000 for row in changes)
        result.append(dict(arguments=arguments,expected=oracle('4.11',arguments)))
    return result

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True or observed.get('uniformOk') is not True:return False
    actual=observed.get('actual');changes=observed.get('changes')
    if not isinstance(actual,dict) or type(actual.get('results')) is not list:return False
    expected,wanted_changes=transitions(case['arguments']);results=actual['results'];operations,arguments=case['arguments']
    if len(results)!=len(operations) or type(changes) is not list or len(changes)!=len(operations):return False
    counts=Counter()
    for operation,values,result,change,wanted in zip(operations,arguments,results,changes,wanted_changes):
        if not isinstance(change,dict) or type(change.get('count')) is not int:return False
        for key in ('added','removed'):
            if type(change.get(key)) is not list or any(type(v) is not int for v in change[key]):return False
        if change!=wanted:return False
        if operation in ('RandomBst','Insert'):
            if result is not None:return False
            if operation=='Insert':counts[values[0]]+=1
        elif operation=='Delete':
            present=counts[values[0]]>0
            if type(result) is not bool or result!=present:return False
            if present:counts[values[0]]-=1
        else:
            if type(result) is not list or any(type(v) is not int for v in result):return False
            if operation=='Find':
                if result!=([values[0]] if counts[values[0]] else []):return False
            elif sum(counts.values())==0:
                if result!=[]:return False
            elif len(result)!=1 or counts[result[0]]<=0:return False
    final=actual.get('finalValues')
    return type(final) is list and all(type(v) is int for v in final) and final==expected['finalValues']
