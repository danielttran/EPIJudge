"""Actual object identities and exact multiset deltas, never expected answers."""
from harness_random04 import uniform_parts

CORE='''
class NodeContract4(Exception):pass
def node_check4(ok,message):
    if not ok:raise NodeContract4(message)
def node_snapshot4(actor):
    root=actor.Root;pending=[] if root is None else [root];nodes=[];identities=set();links=[]
    while pending:
        node=pending.pop();node_check4(isinstance(node,RandomNode),'Use the provided RandomNode API')
        node_check4(id(node) not in identities and len(nodes)<1000,'Root must be a finite proper tree without shared children')
        node_check4(type(node.Data) is int and -2147483648<=node.Data<=2147483647,'Preserve signed integer Data')
        identities.add(id(node));nodes.append(node);links.append((node.Data,node.Left,node.Right))
        if node.Right is not None:pending.append(node.Right)
        if node.Left is not None:pending.append(node.Left)
    ordered=[];stack=[];node=root
    while node is not None or stack:
        while node is not None:stack.append(node);node=node.Left
        node=stack.pop();ordered.append(node);node=node.Right
    values=[node.Data for node in ordered];node_check4(all(a<=b for a,b in zip(values,values[1:])),'Maintain nondecreasing BST inorder values')
    return dict(root=root,nodes=nodes,links=links,ordered=ordered,values=values,rank={id(node):i for i,node in enumerate(ordered)})
def node_query4(actor,before,node):
    node_check4(actor.Root is before['root'] and all(old.Data==raw[0] and old.Left is raw[1] and old.Right is raw[2] for old,raw in zip(before['nodes'],before['links'])),'Find/GetRandomNode must preserve node Data and tree links')
    node_check4(node is None or isinstance(node,RandomNode) and id(node) in before['rank'],'Return an actual current tree node, not a clone or Data value')
    return [] if node is None else [node.Data]
def node_basic4(actor,operation,args):
    if operation=='Insert':node_check4(actor.Insert(args[0]) is None,'Insert returns None');return None
    if operation=='Delete':
        result=actor.Delete(args[0]);node_check4(type(result) is bool,'Delete returns a boolean');return result
    before=node_snapshot4(actor)
    if operation=='Find':return node_query4(actor,before,actor.Find(args[0]))
    if operation=='GetRandomNode':return node_query4(actor,before,actor.GetRandomNode())
    raise NodeContract4('Unknown tree operation')
def node_delta4(before,after):
    i=j=0;added=[];removed=[]
    while i<len(before) and j<len(after):
        if before[i]==after[j]:i+=1;j+=1
        elif before[i]<after[j]:removed.append(before[i]);i+=1
        else:added.append(after[j]);j+=1
    removed.extend(before[i:]);added.extend(after[j:])
    return dict(added=added,removed=removed,count=len(after))
class NodeContext4:
    operations=[]
    arguments=[]
    values=[]
    @staticmethod
    def build():
        actor=RandomBst()
        for operation,args in zip(NodeContext4.operations[1:],NodeContext4.arguments[1:]):node_basic4(actor,operation,args)
        return actor
class NodeShuffle4:
    def __init__(self):self.actor=None
    def Shuffle(self,array):
        if self.actor is None:self.actor=NodeContext4.build()
        before=node_snapshot4(self.actor);node_check4(before['values']==NodeContext4.values and len(array)==len(before['values']),'Repeated tree construction must preserve the operation-prefix multiset')
        chosen=self.actor.GetRandomNode();node_query4(self.actor,before,chosen)
        if not array:node_check4(chosen is None,'Empty-tree GetRandomNode returns null');return
        node_check4(chosen is not None,'Nonempty-tree GetRandomNode returns a current node')
        selected=before['rank'][id(chosen)];remaining=[i for i in range(len(array)) if i!=selected]
        for index in range(len(remaining)-1,0,-1):
            other=RandomSource.GetRandom(0,index);remaining[index],remaining[other]=remaining[other],remaining[index]
        array[:]=[selected]+remaining
'''
ENDING='''
def executeRandomBst4(row):
    operations,arguments=row['arguments'];seed=0x411b57
    def live_draw(lower,upper):
        nonlocal seed
        node_check4(type(lower) is int and type(upper) is int and 0<=lower<=upper<=2147483647,'Use valid inclusive integer random bounds')
        seed=(seed*1664525+1013904223)&0xffffffff
        return lower+(seed*(upper-lower+1)>>32)
    RandomSource.Draw=staticmethod(live_draw)
    actor=RandomBst();before=node_snapshot4(actor);results=[None];changes=[node_delta4([],before['values'])]
    for index in range(1,len(operations)):
        operation=operations[index]
        if operation=='GetRandomNode':
            NodeContext4.operations=operations[:index];NodeContext4.arguments=arguments[:index];NodeContext4.values=before['values'].copy()
            saved=RandomSource.Draw
            try:executeRandom4_11(dict(arguments=[list(range(len(before['values'])))]))
            finally:RandomSource.Draw=staticmethod(saved)
            node_check4(actor.Root is before['root'],'Instances must own independent tree state')
        result=node_basic4(actor,operation,arguments[index]);after=node_snapshot4(actor)
        results.append(result);changes.append(node_delta4(before['values'],after['values']));before=after
    return dict(actual=dict(results=results,finalValues=before['values']),changes=changes,mutationOk=True,uniformOk=True)
'''

def parts(code):
    outside,inside=uniform_parts('python',code+CORE)
    return outside+ENDING,inside
