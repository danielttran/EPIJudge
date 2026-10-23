"""Independent per-owner transactional DAG oracle using Kahn topological elimination."""
import json,random

def model(count,declarations,requests):
 orders={};admitted=[]
 for row in declarations:
  owner,path=row[0],row[1:]
  valid=0<=owner<4 and all(0<=r<count for r in path) and len(set(path))==len(path)
  if valid:
   candidate={**orders,owner:path.copy()};edges={r:set() for r in range(count)}
   for sequence in candidate.values():
    for first,second in zip(sequence,sequence[1:]):edges[first].add(second)
   indegree=[sum(resource in neighbors for neighbors in edges.values()) for resource in range(count)];ready=[r for r,d in enumerate(indegree) if d==0];visited=0
   while ready:
    resource=ready.pop();visited+=1
    for other in edges[resource]:
     indegree[other]-=1
     if indegree[other]==0:ready.append(other)
   valid=visited==count
   if valid:orders=candidate
  admitted.append(valid)
 positions={};grants=[]
 for owner,resource in requests:
  path=orders.get(owner,[]);position=positions.get(owner,0);valid=position<len(path) and path[position]==resource
  grants.append(valid)
  if valid:positions[owner]=position+1
 return dict(declarations=admitted,grants=grants),orders

def oracle(ref,args):return model(*args[:3])[0]
def complete(count,declarations):
 _,orders=model(count,declarations,[]);requests=[[-1,0],[4,0],[0,count]]
 for owner,path in sorted(orders.items()):
  if len(path)>1:requests.append([owner,path[1]])
  requests.extend([[owner,r] for r in path])
  if path:requests.append([owner,path[-1]])
 return [count,declarations,requests,[]]
def cases(spec):
 args=[spec['example'][0],complete(1,[]),complete(1,[[0],[1,0],[2,0,0],[-1,0],[4,0]]),complete(2,[[0,0,1],[1,0,1],[2,1,0],[3,1,0]]),complete(3,[[0,0,1],[1,1,2],[0,2,0]]),complete(3,[[0,0,1],[1,1,2],[0,2,0],[0,0,1]]),complete(6,[[0,0,1,2,3,4,5],[1,1,2,3,4,5],[2,5],[3]])]
 args.append([6,[[-2147483648,0],[2147483647,5],[0,-2147483648],[1,2147483647]],[[-2147483648,0],[2147483647,0],[0,-2147483648],[0,2147483647]],[]])
 for count in range(1,7):
  args += [complete(count,[[0,count],[1,-1],[2,0,0],[3]]),complete(count,[[0,*range(count)],[0],[1,*reversed(range(count))]])]
 rng=random.Random(1504)
 for _ in range(45):
  count=rng.randrange(1,7);declarations=[]
  for _ in range(rng.randrange(1,13)):
   path=list(range(count));rng.shuffle(path);path=path[:rng.randrange(count+1)];owner=rng.randrange(4)
   if rng.randrange(9)==0:path.append(count)
   declarations.append([owner,*path])
  args.append(complete(count,declarations))
 out=[]
 for a in {json.dumps(a):a for a in args}.values():
  assert 1<=a[0]<=6 and len(a[1])<=20 and len(a[2])<=40
  out.append(dict(arguments=a,expected=oracle(spec['ref'],a)))
 return out

def valid_observation(ref,case,observed):
 def same(a,b):
  if type(a) is not type(b):return False
  if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
  if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
  return a==b
 return isinstance(observed,dict) and observed.get('mutationOk') is True and same(observed.get('actual'),case['expected'])
