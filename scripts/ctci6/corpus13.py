"""Independent index-based aggregation oracle, not a copied filter pipeline."""
import itertools
import json
import random

def oracle(ref,args):
    total=0
    for record in args[0]:
        if record[1]==args[1]:total+=record[2]
    return total

def cases(spec):
    args=[spec['example'][0]]
    alphabet=[['same','A',0],['same','A',2],['same','B',3]]
    for n in range(5):
        for rows in itertools.product(alphabet,repeat=n):
            for target in ('A','B','a',''):args.append([list(rows),target])
    args += [[[],target] for target in ('','🌏',' A')]
    args += [[[[str(i),target,1000000] for i in range(1000)],target] for target in ('','🌏','West')]
    args += [[[['n',' A',7],['n','A',11],['n','a',13],['n','é',17],['n','é',19],['n','🌏',23]],target] for target in (' A','A','a','é','é','🌏','')]
    rng=random.Random(1307)
    for _ in range(80):
        rows=[[str(i),rng.choice(('A','a','B','','🌏')),rng.randrange(1000001)] for i in range(rng.randrange(80))]
        args.append([rows,rng.choice(('A','a','B','','🌏','missing'))])
    unique={json.dumps(a):a for a in args}
    return [dict(arguments=a,expected=oracle(spec['ref'],a)) for a in unique.values()]

def valid_observation(ref,case,observed):return isinstance(observed,dict) and observed.get('mutationOk') is True and type(observed.get('actual')) is int and observed['actual']==case['expected']
