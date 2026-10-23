"""Independent union-find group oracle, separate from unchanged hard-task graders."""
import itertools
import json
import random

def groups(args):
    names,frequencies,synonyms=args;parent=list(range(len(names)))
    def find(node):
        while parent[node]!=node:parent[node]=parent[parent[node]];node=parent[node]
        return node
    for first,second in synonyms:parent[find(first)]=find(second)
    members={}
    for index in range(len(names)):members.setdefault(find(index),[]).append(index)
    return {min(ids):(set(ids),sum(frequencies[i] for i in ids)) for ids in members.values()}

def oracle(ref,args):return [[representative,total] for representative,(_,total) in sorted(groups(args).items())]

def name(index):
    result=''
    while True:
        result=chr(65+index%26)+result;index=index//26-1
        if index<0:return 'Name'+result

def cases(spec):
    rng=random.Random(1707);args=[spec['example'][0]]
    edges=[(a,b) for a in range(4) for b in range(a+1,4)]
    for mask in range(1<<len(edges)):
        synonyms=[list(edge) for index,edge in enumerate(edges) if mask>>index&1]
        args += [[[name(i) for i in range(4)],list(freq),synonyms] for freq in itertools.product((0,1,2),repeat=4)]
    args += [[[],[],[]],[['John','john'],[1,2],[]],[['A','B','C'],[1,2,3],[[0,1],[1,0],[0,0],[1,2]]],[[name(i) for i in range(200)],[1000000]*200,[[i,i+1] for i in range(199)]],[[name(i) for i in range(200)],[0]*200,[[0,0]]*10000]]
    for _ in range(100):
        n=rng.randrange(1,31);args.append([[name(i) for i in range(n)],[rng.randrange(1000001) for _ in range(n)],[[rng.randrange(n),rng.randrange(n)] for _ in range(rng.randrange(100))]])
    distinct={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle('17.7',a)) for a in distinct.values()]

def valid_observation(ref,case,observed):
    if not isinstance(observed,dict) or observed.get('mutationOk') is not True:return False
    actual=observed.get('actual')
    if type(actual) is not list or any(type(row) is not list or len(row)!=2 or any(type(v) is not int for v in row) for row in actual):return False
    components=groups(case['arguments']);lookup={name:(representative,total) for representative,(names,total) in components.items() for name in names};seen=set()
    for representative,total in actual:
        if representative not in lookup:return False
        group,expected=lookup[representative]
        if group in seen or total!=expected:return False
        seen.add(group)
    return len(seen)==len(components)
