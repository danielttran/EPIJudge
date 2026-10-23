"""Independent tree interval traversal oracle for the XML token protocol."""
import itertools
import json
import random

def oracle(ref,args):
    names,texts,children,owners,attributes,values,code_names,codes=args
    if not names:return []
    lookup=dict(zip(code_names,map(str,codes)));result=[]
    # Cursor frames descend one child at a time, unlike solution enter/exit event expansion.
    stack=[(0,0,False)]
    while stack:
        node,cursor,opened=stack.pop()
        if not opened:
            result.append(lookup[names[node]])
            for index,owner in enumerate(owners):
                if owner==node:result.extend([lookup[attributes[index]],values[index]])
            result.append('0')
            if texts[node]:result.extend([texts[node],'0']);continue
        if cursor==len(children[node]):result.append('0')
        else:stack.extend([(node,cursor+1,True),(children[node][cursor],0,False)])
    return result

def fixture(parents,text_choice=0):
    n=len(parents)+1;children=[[] for _ in range(n)]
    for node,parent in enumerate(parents,1):children[parent].append(node)
    return [['node']*n,['Text' if text_choice>>i&1 and not children[i] else '' for i in range(n)],children,[],[],[],['node','key','other'],[7,2,9]]

def cases(spec):
    args=[spec['example'][0],[[],[],[],[],[],[],['node'],[1]]]
    for n in range(1,6):
        for parents in itertools.product(*(range(i) for i in range(1,n))):
            for mask in range(1<<n):args.append(fixture(parents,mask))
    args += [fixture([i-1 for i in range(1,1000)],1<<999),fixture([0]*999)]
    rng=random.Random(1612)
    for _ in range(100):
        n=rng.randrange(1,31);row=fixture([rng.randrange(i) for i in range(1,n)],rng.randrange(1<<n));owners=[rng.randrange(n) for _ in range(rng.randrange(40))];seen=set()
        for owner in owners:
            key=rng.choice(['key','other'])
            if (owner,key) in seen:continue
            seen.add((owner,key));row[3].append(owner);row[4].append(key);row[5].append(rng.choice(['','A B',' ','Value']))
        args.append(row)
    row=fixture([0,0]);row[3:6]=[[2,0,1,0],['key','key','other','other'],['Last','A B','',' ']];args.append(row)
    row=fixture([i-1 for i in range(1,1000)]);row[3:6]=[list(range(1000)),['key']*1000,['A B']*1000];args.append(row)
    row=fixture([]);row[3:6]=[[0],['key'],['X'*100]];args.append(row)
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('16.12',a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    return isinstance(observed,dict) and observed.get('mutationOk') is True and type(observed.get('actual')) is list and all(type(value) is str for value in observed['actual']) and observed['actual']==case['expected']
