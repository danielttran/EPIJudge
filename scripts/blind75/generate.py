"""Generate the isolated catalog and language scaffolds; run from the repository root."""
import json, re
from pathlib import Path
from specs import SPECS
from oracle import solve, equivalent
from corpus import extend
from explanations import explain

ROOT=Path(__file__).resolve().parents[2]
LANGS=['csharp','javascript','python','cpp','java']
TYPES={
 'csharp':dict(i='int',l='long',b='bool',s='string',ai='int[]',aai='int[][]',aas='string[][]',ab='bool[]',ad='double[]',**{'as':'string[]','list':'ListNode?','lists':'ListNode?[]','tree':'TreeNode?','tree_node':'TreeNode?','graph':'Node?','void':'void'}),
 'cpp':dict(i='int',l='long long',b='bool',s='std::string',ai='std::vector<int>',aai='std::vector<std::vector<int>>',aas='std::vector<std::vector<std::string>>',ab='std::vector<bool>',ad='std::vector<double>',**{'as':'std::vector<std::string>','list':'ListNode*','lists':'std::vector<ListNode*>','tree':'TreeNode*','tree_node':'TreeNode*','graph':'Node*','void':'void'}),
 'java':dict(i='int',l='long',b='boolean',s='String',ai='int[]',aai='int[][]',aas='String[][]',ab='boolean[]',ad='double[]',**{'as':'String[]','list':'ListNode','lists':'ListNode[]','tree':'TreeNode','tree_node':'TreeNode','graph':'Node','void':'void'}),
 'python':dict(i='int',l='int',b='bool',s='str',ai='list[int]',aai='list[list[int]]',aas='list[list[str]]',ab='list[bool]',ad='list[float]',**{'as':'list[str]','list':'ListNode | None','lists':'list[ListNode | None]','tree':'TreeNode | None','tree_node':'TreeNode | None','graph':'Node | None','void':'None'})}
HEADERS={
'csharp':'''using System;
using System.Collections.Generic;
using System.Linq;
public class ListNode { public int val; public ListNode? next; public ListNode(int val=0,ListNode? next=null){this.val=val;this.next=next;} }
public class TreeNode { public int val; public TreeNode? left,right; public TreeNode(int val=0,TreeNode? left=null,TreeNode? right=null){this.val=val;this.left=left;this.right=right;} }
public class Node { public int val; public List<Node> neighbors=new(); public Node(int val=0){this.val=val;} }
''',
'java':'''import java.util.*;
class ListNode { public int val; public ListNode next; public ListNode(int val,ListNode next){this.val=val;this.next=next;} public ListNode(int val){this(val,null);} }
class TreeNode { public int val; public TreeNode left,right; public TreeNode(int val){this.val=val;} }
class Node { public int val; public List<Node> neighbors=new ArrayList<>(); public Node(int val){this.val=val;} }
''',
'cpp':'''#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
struct ListNode { int val; ListNode* next; ListNode(int val=0,ListNode* next=nullptr):val(val),next(next){} };
struct TreeNode { int val; TreeNode *left=nullptr,*right=nullptr; explicit TreeNode(int val=0):val(val){} };
struct Node { int val; std::vector<Node*> neighbors; explicit Node(int val=0):val(val){} };
''',
'javascript':'''class ListNode { constructor(val=0,next=null){this.val=val;this.next=next;} }
class TreeNode { constructor(val=0,left=null,right=null){this.val=val;this.left=left;this.right=right;} }
class Node { constructor(val=0){this.val=val;this.neighbors=[];} }
''',
'python':'''from __future__ import annotations
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
class Node:
    def __init__(self, val=0): self.val, self.neighbors = val, []
'''}

def name(method,lang):
    if lang=='python': return re.sub(r'(?<!^)(?=[A-Z])','_',method).lower().replace('b_s_t','bst').replace('l_i_s','lis')
    return method[:1].lower()+method[1:] if lang in ('javascript','java') else method

def neutral(t,lang):
    if t=='void': return ''
    if t in ('i','l'): return '0'
    if t=='b': return 'False' if lang=='python' else 'false'
    if t=='s': return "''" if lang in ('python','javascript') else '""'
    if t in ('list','tree','tree_node','graph'): return {'python':'None','cpp':'nullptr'}.get(lang,'null')
    if lang=='java': return 'new '+TYPES[lang][t].replace('[]','[0]',1)
    return '{}' if lang=='cpp' else '[]'

STATE={
 'strings_codec':('Codec',[('Encode',[('strings','as')],'s'),('Decode',[('encoded','s')],'as')]),
 'tree_codec':('Codec',[('Serialize',[('root','tree')],'s'),('Deserialize',[('encoded','s')],'tree')]),
 'trie':('Trie',[('Insert',[('word','s')],'void'),('Search',[('word','s')],'b'),('StartsWith',[('prefix','s')],'b')]),
 'dictionary':('WordDictionary',[('AddWord',[('word','s')],'void'),('Search',[('pattern','s')],'b')]),
 'median':('MedianFinder',[('AddNum',[('value','i')],'void'),('FindMedian',[],'double')])}
for l in TYPES: TYPES[l]['double']={'python':'float','cpp':'double','java':'double','csharp':'double'}[l]

def starter(s,lang,bodies=None):
    state=STATE.get(s['mode']); cls, methods=state if state else ('Solution',[(s['method'],[(p['name'],p['type']) for p in s['params']],s['result'])])
    pieces=[];signatures=[]
    for method,params,result in methods:
        method_name=name(method,lang)
        body=bodies.get(method) if bodies else None
        default=neutral(result if result!='double' else 'i',lang)
        if lang=='python':
            signature=f"def {method_name}({', '.join(n+': '+TYPES[lang][t] for n,t in params)}) -> {TYPES[lang][result]}"
            args=', '.join(['self']+[n+': '+TYPES[lang][t] for n,t in params]) if state else ', '.join(n+': '+TYPES[lang][t] for n,t in params)
            code=f"def {method_name}({args}) -> {TYPES[lang][result]}:\n"+'\n'.join('    '+line for line in (body or ('# Write your solution here.\n'+('return '+default if result!='void' else 'pass'))).splitlines())+'\n'
        elif lang=='javascript':
            signature=f"{method_name}({', '.join(n for n,_ in params)})"
            code=('' if state else 'function ')+signature+' {\n'+(body or '    // Write your solution here.\n'+('    return '+default+';' if result!='void' else ''))+'\n}\n'
        else:
            typed=', '.join(TYPES[lang][t]+((' &' if t.startswith('a') else ' ') if lang=='cpp' else ' ')+n for n,t in params)
            signature=f"{TYPES[lang][result]} {method_name}({typed})"
            code=('public ' if lang in ('java','csharp') else '')+signature+' {\n'+(body or '    // Write your solution here.\n'+('    return '+default+';' if result!='void' else ''))+'\n}\n'
        signatures.append(signature); pieces.append(code)
    if lang=='python': source=HEADERS[lang]+('class '+cls+':\n'+''.join('    '+line+'\n' for line in '\n'.join(pieces).splitlines()) if state else '\n'.join(pieces))
    elif lang=='javascript': source=HEADERS[lang]+(('class '+cls+' {\n'+''.join(pieces)+'}\n') if state else ''.join(pieces))+'\nmodule.exports = { ListNode, TreeNode, Node, '+(cls if state else name(s['method'],lang))+' };\n'
    else: source=HEADERS[lang]+('public class ' if lang in ('java','csharp') else 'class ')+cls+' {\n'+('public:\n' if lang=='cpp' else '')+''.join(pieces)+('};\n' if lang=='cpp' else '}\n')
    return dict(signature='; '.join(signatures),starterCode=source,filename={'csharp':'Solution.cs','java':cls+'.java','cpp':'solution.cpp','python':'solution.py','javascript':'solution.js'}[lang],runtime={'csharp':'C# .NET 10','java':'Java 21','cpp':'C++17','python':'Python 3.14','javascript':'JavaScript Node.js 24'}[lang])

def cpp_body(s):
    lines=['json execute(const json& raw){']
    for i,p in enumerate(s['params']):
        k=p['type']; value=f'raw[{i}]'
        value={'list':f'readList({value})','lists':f'readLists({value})','tree':f'readTree({value})','graph':f'readGraph({value})'}.get(k, f'{value}.get<{TYPES["cpp"][k]}>()')
        lines.append(f'auto a{i}={value};')
    mode=s['mode'];args=','.join('a'+str(i) for i in range(len(s['params'])))
    node_type='ListNode' if mode.startswith('list_') else 'Node' if mode=='graph_clone' else 'TreeNode'
    node_fn='listNodes' if mode.startswith('list_') else 'graphNodes' if mode=='graph_clone' else 'treeNodes'
    structural=mode in ('list_reuse','list_remove','list_reorder','tree_inplace','tree_node','tree_codec','graph_clone')
    if structural:
        lines.append(f'std::vector<{node_type}*> original;')
        for i,p in enumerate(s['params']):
            if p['type']=='lists': lines.append(f'for(auto head:a{i}){{auto nn=listNodes(head);original.insert(original.end(),nn.begin(),nn.end());}}')
            elif p['type'] in ('list','tree','graph'): lines.append(f'{{auto nn={node_fn}(a{i});original.insert(original.end(),nn.begin(),nn.end());}}')
        lines.append(f'std::unordered_map<{node_type}*,int> snapshot;for(auto n:original)snapshot[n]=n->val;')
    if mode in ('tree_codec','graph_clone'):
        lines.append('auto before=dump(a0);')
        lines.append('std::unordered_map<Node*,std::vector<Node*>> originalLinks;for(auto n:original)originalLinks[n]=n->neighbors;' if mode=='graph_clone' else 'std::unordered_map<TreeNode*,std::pair<TreeNode*,TreeNode*>> originalLinks;for(auto n:original)originalLinks[n]={n->left,n->right};')
    if mode=='matrix_inplace': lines.append('std::vector<const void*> rows;for(auto& row:a0)rows.push_back(&row);')
    if mode=='list_cycle':
        lines.extend(['auto nn=listNodes(a0);int pos=raw[1].get<int>();if(pos>=0)nn.back()->next=nn.at(pos);std::vector<ListNode*> edges;std::vector<int> values;for(auto n:nn){edges.push_back(n->next);values.push_back(n->val);}',f'auto actual=Solution().{s["method"]}({args});','for(size_t i=0;i<nn.size();i++){check(nn[i]->next==edges[i],"Cycle detection must preserve links.");check(nn[i]->val==values[i],"Cycle detection must preserve values.");}'])
    elif mode=='strings_codec': lines.append('auto actual=Codec().Decode(Codec().Encode(a0));')
    elif mode=='tree_codec': lines.append('auto actual=Codec().Deserialize(Codec().Serialize(a0));')
    elif mode in ('trie','dictionary','median'):
        cls=STATE[mode][0];lines.append(f'{cls} obj;json actual=json::array();')
        ops={'trie':[('insert','Insert',False),('search','Search',True),('startsWith','StartsWith',True)],'dictionary':[('addWord','AddWord',False),('search','Search',True)],'median':[('addNum','AddNum',False),('findMedian','FindMedian',True)]}[mode]
        lines.append('for(size_t i=0;i<a0.size();i++){')
        for op,fn,query in ops:
            call=f'obj.{fn}('+('' if op=='findMedian' else 'a1[i]')+')'
            lines.append(f'if(a0[i]=="{op}")'+('actual.push_back('+call+');' if query else call+';'))
        lines.append('}')
    elif mode in ('matrix_inplace','list_reorder'): lines.extend([f'Solution().{s["method"]}({args});','auto actual=a0;'])
    else: lines.append(f'auto actual=Solution().{s["method"]}({args});')
    if mode=='matrix_inplace': lines.append('check(rows.size()==a0.size());for(size_t i=0;i<rows.size();i++)check(rows[i]==&a0[i],"Preserve each row object.");')
    if structural:
        lines.append(f'auto after={node_fn}(actual);' if mode!='tree_node' else 'std::vector<TreeNode*> after;if(actual)after.push_back(actual);')
        if mode in ('list_reuse','list_remove','list_reorder','tree_inplace'):
            lines.append(f'std::unordered_set<{node_type}*> expected(original.begin(),original.end());')
            if mode=='list_remove':lines.append('expected.erase(original.at(original.size()-a1));')
            lines.append('check(expected.size()==after.size(),"Reuse exactly the requested original nodes.");for(auto n:after)check(expected.count(n)!=0,"Return original nodes.");')
        elif mode=='tree_node': lines.append('check(actual && snapshot.count(actual),"Return an original tree node.");')
        else:
            lines.append('for(auto n:after)check(!snapshot.count(n),"Copy shares original nodes.");check(dump(a0)==before,"Preserve original structure.");')
            lines.append('for(auto n:original)check(n->neighbors.size()==originalLinks.at(n).size()&&std::unordered_set<Node*>(n->neighbors.begin(),n->neighbors.end())==std::unordered_set<Node*>(originalLinks.at(n).begin(),originalLinks.at(n).end()),"Preserve original links.");' if mode=='graph_clone' else 'for(auto n:original)check(std::make_pair(n->left,n->right)==originalLinks.at(n),"Preserve original links.");')
        lines.append('for(auto n:original)check(n->val==snapshot.at(n),"Preserve original values.");')
        if mode=='tree_inplace':lines.append('check(actual==a0,"Return the original root.");')
    lines.append('return actual?json(actual->val):json(nullptr);' if mode=='tree_node' else 'return dump(actual);')
    return '\n'.join(lines)+'\n}'

def configs(s):
    kinds=[p['type'] for p in s['params']];out='aai' if s['mode']=='matrix_inplace' else 'list' if s['mode']=='list_reorder' else s['result']
    cls=STATE.get(s['mode'],('Solution',[]))[0]
    basic=dict(KINDS=kinds,MODE=s['mode'],METHOD=name(s['method'],'javascript'),OUTPUT=out,CLASS=cls)
    js='\n'.join(f'const {k}={json.dumps(v)};' for k,v in basic.items())+'\n'
    py='\n'.join(f'{k}={v!r}' for k,v in basic.items() if k!='METHOD')+'\nMETHOD='+repr(name(s['method'],'python'))+'\nOP_NAMES='+repr({o:name(o[0].upper()+o[1:],'python') for o in ['insert','search','startsWith','addWord','addNum']})+'\n'
    cs='\n'.join(['static readonly string[] Kinds=['+','.join(json.dumps(k) for k in kinds)+'];']+[f'static readonly string {k}={json.dumps(v)};' for k,v in [('Mode',s['mode']),('Method',s['method']),('Output',out),('Class',cls)]])
    java='\n'.join(['static final String[] KINDS={'+','.join(json.dumps(k) for k in kinds)+'};']+[f'static final String {k}={json.dumps(v)};' for k,v in [('MODE',s['mode']),('METHOD',name(s['method'],'java')),('OUTPUT',out),('CLASS',cls)]])
    return dict(csharp=cs,javascript=js,python=py,java=java,cpp=cpp_body(s))

def generate():
    catalog=[]
    order_path=ROOT/'blind75/source-order.txt'
    if order_path.exists():assert [s['title'] for s in SPECS]==order_path.read_text().splitlines(), 'Crackr order changed'
    diagram_path=ROOT/'blind75/diagrams.json'
    diagrams={d['id']:d for d in json.loads(diagram_path.read_text())} if diagram_path.exists() else {}
    for source in SPECS:
        s=dict(source, cases=extend(source))
        for case in s['cases']:
            assert equivalent(s,solve(s,case['arguments']),case['expected'],case['arguments']), (s['id'],case)
        item={k:v for k,v in s.items() if k!='cases'}
        item['starters']={lang:starter(s,lang) for lang in LANGS};item['harnessConfigs']=configs(s)
        item['testCount']=len(s['cases'])
        if s['id'] in diagrams:item.update(diagram=diagrams[s['id']]['path'],diagramAlt=diagrams[s['id']]['alt'])
        item['examples']=[dict(input=', '.join((s['params'][i]['name'] if i<len(s['params']) else 'pos')+' = '+json.dumps(v,ensure_ascii=True) for i,v in enumerate(c['arguments'])),output=json.dumps(c['expected'],ensure_ascii=True),explanation=explain(s,c)) for c in s['cases'][:3]]
        catalog.append(item)
        path=ROOT/'blind75'/'cases'/f'{s["id"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(s['cases'],indent=2)+'\n')
    (ROOT/'blind75/catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
    print(f'Generated {len(catalog)} isolated problems and {len(catalog)*5} typed starters.')

if __name__=='__main__': generate()
