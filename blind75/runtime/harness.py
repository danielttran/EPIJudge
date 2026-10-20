import json, time, contextlib, io, sys
sys.setrecursionlimit(10000)
import solution as user

class ContractError(Exception): pass

def check(ok, message='The result violates the problem contract.'):
    if not ok: raise ContractError(message)

def list_nodes(head):
    nodes=[]; seen=set()
    while head is not None:
        check(id(head) not in seen, 'Output list contains a cycle.')
        seen.add(id(head)); nodes.append(head); head=head.next
    return nodes

def nodes(root,kind):
    if kind=='list': return list_nodes(root)
    if kind=='lists': return [n for head in root for n in list_nodes(head)]
    if kind in ('tree','graph'):
        out=[]; seen=set(); q=[root] if root is not None else []
        while q:
            n=q.pop()
            if id(n) in seen:
                check(kind=='graph','Tree contains a cycle or shared child.'); continue
            seen.add(id(n)); out.append(n)
            q.extend(n.neighbors if kind=='graph' else [c for c in [n.left,n.right] if c is not None])
        return out
    return []

def load(v,kind):
    if kind=='list':
        head=None
        for value in reversed(v): head=user.ListNode(value,head)
        return head
    if kind=='lists': return [load(row,'list') for row in v]
    if kind=='tree':
        if not v: return None
        root=user.TreeNode(v[0]); q=[root]; i=1
        for n in q:
            for side in ('left','right'):
                if i<len(v) and v[i] is not None:
                    child=user.TreeNode(v[i]); setattr(n,side,child); q.append(child)
                i+=1
        return root
    if kind=='graph':
        nn=[user.Node(i+1) for i in range(len(v))]
        for n,row in zip(nn,v): n.neighbors=[nn[i-1] for i in row]
        return nn[0] if nn else None
    return v

def dump(v,kind):
    if kind=='list': return [n.val for n in list_nodes(v)]
    if kind=='tree_node': return v.val if v else None
    if kind=='tree':
        nodes(v,'tree'); out=[]; q=[v] if v else []
        for n in q:
            out.append(n.val if n else None)
            if n: q.extend([n.left,n.right])
        while out and out[-1] is None: out.pop()
        return out
    if kind=='graph':
        nn=sorted(nodes(v,'graph'),key=lambda n:n.val)
        check([n.val for n in nn]==list(range(1,len(nn)+1)), 'Graph labels must remain unique and contiguous.')
        return [sorted(c.val for c in n.neighbors) for n in nn]
    return v

def execute(raw):
    args=[load(v,k) for v,k in zip(raw,KINDS)]
    mode=MODE; snapshot={}; original=[]
    for value,kind in zip(args,KINDS): original.extend(nodes(value,kind))
    snapshot={id(n):n.val for n in original}
    original_links={id(n):tuple(n.neighbors) if hasattr(n,'neighbors') else (n.left,n.right) if hasattr(n,'left') else (n.next,) for n in original}
    rows=list(args[0]) if mode=='matrix_inplace' else []
    before=dump(args[0],KINDS[0]) if mode in ('tree_codec','graph_clone') else None
    if mode=='list_cycle':
        nn=list_nodes(args[0]); pos=raw[1]
        if pos>=0: nn[-1].next=nn[pos]
        edges=[n.next for n in nn]
        actual=getattr(user,METHOD)(*args)
        check(all(n.next is p for n,p in zip(nn,edges)), 'Cycle detection must preserve input links.')
        check(all(n.val==snapshot[id(n)] for n in nn), 'Cycle detection must preserve values.')
    elif mode=='strings_codec': actual=user.Codec().decode(user.Codec().encode(args[0]))
    elif mode=='tree_codec': actual=user.Codec().deserialize(user.Codec().serialize(args[0]))
    elif mode in ('trie','dictionary','median'):
        obj=getattr(user,CLASS)(); actual=[]
        for op,value in zip(*args):
            result=getattr(obj,OP_NAMES[op])(value) if op not in ('findMedian',) else obj.find_median()
            if op not in ('insert','addWord','addNum'): actual.append(result)
    else:
        actual=getattr(user,METHOD)(*args)
        if mode in ('matrix_inplace','list_reorder'): actual=args[0]
    if mode=='matrix_inplace': check(len(rows)==len(args[0]) and all(x is y for x,y in zip(rows,args[0])), 'Preserve each matrix row object.')
    if mode in ('list_reuse','list_remove','list_reorder','tree_inplace','tree_node','tree_codec','graph_clone'):
        kind='list' if mode.startswith('list_') else 'graph' if mode=='graph_clone' else 'tree'
        after=nodes(actual,kind) if mode!='tree_node' else ([actual] if actual else [])
        if mode=='list_remove':
            index=len(original)-args[1]; expected=[n for i,n in enumerate(original) if i!=index]
            check({id(n) for n in after}=={id(n) for n in expected}, 'Remove exactly the requested original node.')
        elif mode in ('list_reuse','list_reorder','tree_inplace'): check({id(n) for n in after}==set(snapshot), 'Reuse exactly the original nodes.')
        elif mode=='tree_node': check(actual is not None and id(actual) in snapshot,'Return an original tree node.')
        else:
            check(not any(id(n) in snapshot for n in after), 'The copy shares nodes with the input.')
            check(dump(args[0],KINDS[0])==before,'Preserve the original structure.')
            for n in original:
                links=tuple(n.neighbors) if kind=='graph' else (n.left,n.right)
                check(len(links)==len(original_links[id(n)]) and ({id(x) for x in links}=={id(x) for x in original_links[id(n)]} if kind=='graph' else all(x is y for x,y in zip(links,original_links[id(n)]))), 'Preserve the original node links.')
        check(all(n.val==snapshot[id(n)] for n in original),'Preserve original node values.')
        if mode=='tree_inplace': check(actual is args[0], 'Return the original root.')
    return dump(actual,OUTPUT)

results=[]
for raw in json.load(open('cases.json',encoding='utf-8')):
    start=time.perf_counter(); actual=None; error=None; invalid=False
    try:
        with contextlib.redirect_stdout(io.StringIO()): actual=execute(raw)
    except ContractError as ex: invalid=True; error=str(ex)
    except Exception as ex: error=type(ex).__name__+': '+str(ex)
    results.append(dict(actual=actual,error=error if not invalid else None,validationFailed=invalid,elapsedMs=(time.perf_counter()-start)*1000))
with open('results.json','w',encoding='utf-8') as f: json.dump(results,f)
