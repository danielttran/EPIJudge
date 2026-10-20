const fs = require('fs');
const user = require('./solution.js');
class ContractError extends Error {}
function check(ok, message='The result violates the problem contract.') { if (!ok) throw new ContractError(message); }
function listNodes(head) {
  const out=[], seen=new Set();
  while(head) { check(!seen.has(head),'Output list contains a cycle.'); seen.add(head); out.push(head); head=head.next; }
  return out;
}
function nodes(root,kind) {
  if(kind==='list') return listNodes(root);
  if(kind==='lists') return root.flatMap(listNodes);
  if(kind!=='tree' && kind!=='graph') return [];
  const out=[],seen=new Set(),q=root?[root]:[];
  while(q.length) {
    const n=q.pop();
    if(seen.has(n)) { check(kind==='graph','Tree contains a cycle or shared child.'); continue; }
    seen.add(n);out.push(n);q.push(...(kind==='graph'?n.neighbors:[n.left,n.right].filter(Boolean)));
  }
  return out;
}
function load(v,kind) {
  if(kind==='list') { let head=null; for(let i=v.length-1;i>=0;i--) head=new user.ListNode(v[i],head); return head; }
  if(kind==='lists') return v.map(row=>load(row,'list'));
  if(kind==='tree') {
    if(!v.length) return null;
    const root=new user.TreeNode(v[0]),q=[root];let i=1;
    for(let k=0;k<q.length;k++) for(const side of ['left','right']) {
      if(i<v.length && v[i]!==null) { const child=new user.TreeNode(v[i]); q[k][side]=child;q.push(child); } i++;
    }
    return root;
  }
  if(kind==='graph') { const nn=v.map((_,i)=>new user.Node(i+1)); nn.forEach((n,i)=>n.neighbors=v[i].map(label=>nn[label-1]));return nn[0]??null; }
  return v;
}
function dump(v,kind) {
  if(kind==='list') return listNodes(v).map(n=>n.val);
  if(kind==='tree_node') return v?.val??null;
  if(kind==='tree') {
    nodes(v,'tree');const out=[],q=v?[v]:[];
    for(let i=0;i<q.length;i++) { const n=q[i];out.push(n?n.val:null);if(n)q.push(n.left,n.right); }
    while(out.length && out.at(-1)===null)out.pop();return out;
  }
  if(kind==='graph') {
    const nn=nodes(v,'graph').sort((a,b)=>a.val-b.val);
    check(nn.every((n,i)=>n.val===i+1),'Graph labels must remain unique and contiguous.');
    return nn.map(n=>n.neighbors.map(c=>c.val).sort((a,b)=>a-b));
  }
  return v;
}
function execute(raw) {
  const args=raw.slice(0,KINDS.length).map((v,i)=>load(v,KINDS[i]));
  const original=args.flatMap((v,i)=>nodes(v,KINDS[i])),snapshot=new Map(original.map(n=>[n,n.val]));
  const originalLinks=new Map(original.map(n=>[n,n.neighbors?[...n.neighbors]:'left' in n?[n.left,n.right]:[n.next]]));
  const rows=MODE==='matrix_inplace'?[...args[0]]:[];
  const before=['tree_codec','graph_clone'].includes(MODE)?JSON.stringify(dump(args[0],KINDS[0])):null;
  let actual;
  if(MODE==='list_cycle') {
    const nn=listNodes(args[0]); if(raw[1]>=0)nn.at(-1).next=nn[raw[1]];const edges=nn.map(n=>n.next);
    actual=user[METHOD](...args);check(nn.every((n,i)=>n.next===edges[i]),'Cycle detection must preserve links.');
    check(nn.every(n=>n.val===snapshot.get(n)),'Cycle detection must preserve values.');
  } else if(MODE==='strings_codec') actual=new user.Codec().decode(new user.Codec().encode(args[0]));
  else if(MODE==='tree_codec') actual=new user.Codec().deserialize(new user.Codec().serialize(args[0]));
  else if(['trie','dictionary','median'].includes(MODE)) {
    const obj=new user[CLASS]();actual=[];
    args[0].forEach((op,i)=>{const value=op==='findMedian'?obj.findMedian():obj[op](args[1][i]);if(!['insert','addWord','addNum'].includes(op))actual.push(value);});
  } else { actual=user[METHOD](...args);if(['matrix_inplace','list_reorder'].includes(MODE))actual=args[0]; }
  if(MODE==='matrix_inplace')check(rows.length===args[0].length && rows.every((row,i)=>row===args[0][i]),'Preserve each row object.');
  if(['list_reuse','list_remove','list_reorder','tree_inplace','tree_node','tree_codec','graph_clone'].includes(MODE)) {
    const kind=MODE.startsWith('list_')?'list':MODE==='graph_clone'?'graph':'tree';
    const after=MODE==='tree_node'?(actual?[actual]:[]):nodes(actual,kind);
    const sameSet=expected=>after.length===expected.length && after.every(n=>expected.includes(n));
    if(MODE==='list_remove')check(sameSet(original.filter((_,i)=>i!==original.length-args[1])),'Remove exactly the requested original node.');
    else if(['list_reuse','list_reorder','tree_inplace'].includes(MODE))check(sameSet(original),'Reuse exactly the original nodes.');
    else if(MODE==='tree_node')check(snapshot.has(actual),'Return an original tree node.');
    else {
      check(after.every(n=>!snapshot.has(n)),'Copy shares original nodes.');check(JSON.stringify(dump(args[0],KINDS[0]))===before,'Preserve original structure.');
      for(const n of original){const links=n.neighbors?[...n.neighbors]:[n.left,n.right],old=originalLinks.get(n);check(links.length===old.length&&(kind==='graph'?old.every(x=>links.includes(x)):links.every((x,i)=>x===old[i])),'Preserve original node links.');}
    }
    check(original.every(n=>n.val===snapshot.get(n)),'Preserve original node values.');
    if(MODE==='tree_inplace')check(actual===args[0],'Return the original root.');
  }
  return dump(actual,OUTPUT);
}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(raw=>{
  const start=performance.now();let actual=null,error=null,validationFailed=false;const log=console.log;
  try {console.log=()=>{};actual=execute(raw);}catch(ex){if(ex instanceof ContractError)validationFailed=true;else error=String(ex);}finally{console.log=log;}
  return {actual,error,validationFailed,elapsedMs:performance.now()-start};
});
fs.writeFileSync('results.json',JSON.stringify(results));
