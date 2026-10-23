"""Decode shared node identities and observe results/readonly links; no answer logic."""
from core import ROOT
import json
from models04 import TREE_REFS,TREE,header
from models08 import header as base_header


def expression(entry,language):
    ref=entry['ref'];method=entry['method'];cls='Solution_'+ref.replace('.','_')
    args='first,second' if ref in ('4.8','4.10') else 'first,args[1].GetInt32()' if language=='csharp' and ref=='4.12' else 'first,args.get(1).asInt()' if language=='java' and ref=='4.12' else 'first,args[1].get<int>()' if language=='cpp' and ref=='4.12' else "first,args[1]" if ref=='4.12' else 'first'
    call=method+'('+args+')' if language in ('python','javascript') else ('new '+cls+'().' if language in ('csharp','java') else cls+'().')+method+'('+args+')'
    if entry['result']=='tree':call=('nodeId' if language in ('python','javascript') else 'NodeId' if language=='csharp' else 'nodeId')+'('+call+(', ids)' if language!='python' else ', ids)')
    return call


def pieces(language,entries,starters):
    declarations=[];branches=[]
    for entry in entries:
        code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
        if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_'+entry['ref'].replace('.','_'),1)
        declarations.append(code);ref=entry['ref'];call=expression(entry,language)
        branches.append(f"    if ref=={ref!r}: actual={call}\n" if language=='python' else f"if(ref==={json.dumps(ref)})actual={call};" if language=='javascript' else f'case "{ref}":actual={call};break;' if language in ('csharp','java') else f'if(ref=="{ref}")actual={call};')
    code='\n'.join(declarations)
    if language=='python':
        dispatch=''.join(branches).replace('    if ref==','    elif ref==')
        dispatch=dispatch.replace('    elif ref==','    if ref==',1)
        return code+'''
def nodeId(node,ids):
    return -1 if node is None else ids.get(id(node),-2)
def readTree(view,nodes):
    offset=len(nodes);rows=view['nodes']
    nodes.extend(TreeNode(row[0]) for row in rows)
    for index,(_,left,right) in enumerate(rows):
        node=nodes[offset+index]
        if left!=-1:node.Left=nodes[offset+left];node.Left.Parent=node
        if right!=-1:node.Right=nodes[offset+right];node.Right.Parent=node
    return None if view['selected']==-1 else nodes[offset+view['selected']]
def treeSnapshot(nodes,ids):
    return [(node.Data,nodeId(node.Left,ids),nodeId(node.Right,ids),nodeId(node.Parent,ids)) for node in nodes]
def executeTree(row):
    args=row['arguments'];ref=row['ref'];nodes=[]
    first=readTree(args[0],nodes);second=None
    if ref=='4.10':second=readTree(args[1],nodes)
    elif ref=='4.8':second=None if args[1]==-1 else nodes[args[1]]
    ids={id(node):index for index,node in enumerate(nodes)};before=treeSnapshot(nodes,ids)
'''+dispatch+'''    else:raise ValueError('Unknown tree reference')
    valid=type(actual) is bool if ref in ('4.4','4.5','4.10') else type(actual) is int and -2147483648<=actual<=2147483647
    return dict(actual=actual,mutationOk=valid and all(type(node.Data) is int for node in nodes) and treeSnapshot(nodes,ids)==before)
''',''
    if language=='javascript':
        dispatch='else '.join(branches)
        return code+'''
function nodeId(node,ids){return node===null?-1:ids.has(node)?ids.get(node):-2;}
function readTree(view,nodes){const offset=nodes.length;for(const row of view.nodes)nodes.push(new TreeNode(row[0]));for(let i=0;i<view.nodes.length;++i){const node=nodes[offset+i],[,left,right]=view.nodes[i];if(left!==-1){node.Left=nodes[offset+left];node.Left.Parent=node;}if(right!==-1){node.Right=nodes[offset+right];node.Right.Parent=node;}}return view.selected===-1?null:nodes[offset+view.selected];}
function treeSnapshot(nodes,ids){return nodes.map(node=>[node.Data,nodeId(node.Left,ids),nodeId(node.Right,ids),nodeId(node.Parent,ids)]);}
function executeTree(row){const args=row.arguments,ref=row.ref,nodes=[],first=readTree(args[0],nodes);let second=null;if(ref==='4.10')second=readTree(args[1],nodes);else if(ref==='4.8')second=args[1]===-1?null:nodes[args[1]];const ids=new Map(nodes.map((node,index)=>[node,index])),before=JSON.stringify(treeSnapshot(nodes,ids));let actual;
'''+dispatch+'''else throw new Error('Unknown tree reference');const valid=['4.4','4.5','4.10'].includes(ref)?typeof actual==='boolean':Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647;return {actual,mutationOk:valid&&nodes.every(node=>Number.isInteger(node.Data)&&node.Data>=-2147483648&&node.Data<=2147483647)&&JSON.stringify(treeSnapshot(nodes,ids))===before};}
''',''
    if language=='csharp':return code,'''static TreeNode? ReadTree(JsonElement view,List<TreeNode> nodes){int offset=nodes.Count;var rows=view.GetProperty("nodes");foreach(var value in rows.EnumerateArray())nodes.Add(new TreeNode(value[0].GetInt32()));for(int i=0;i<rows.GetArrayLength();++i){var node=nodes[offset+i];int left=rows[i][1].GetInt32(),right=rows[i][2].GetInt32();if(left!=-1){node.Left=nodes[offset+left];node.Left.Parent=node;}if(right!=-1){node.Right=nodes[offset+right];node.Right.Parent=node;}}int selected=view.GetProperty("selected").GetInt32();return selected==-1?null:nodes[offset+selected];}
static int NodeId(TreeNode? node,Dictionary<TreeNode,int> ids)=>node==null?-1:ids.TryGetValue(node,out int index)?index:-2;
static int[][] TreeSnapshot(List<TreeNode> nodes,Dictionary<TreeNode,int> ids)=>nodes.Select(node=>new[]{node.Data,NodeId(node.Left,ids),NodeId(node.Right,ids),NodeId(node.Parent,ids)}).ToArray();
static object ExecuteTree(JsonElement row){var args=row.GetProperty("arguments");string reference=row.GetProperty("ref").GetString()!;var nodes=new List<TreeNode>();var first=ReadTree(args[0],nodes);TreeNode? second=null;if(reference=="4.10")second=ReadTree(args[1],nodes);else if(reference=="4.8")second=args[1].GetInt32()==-1?null:nodes[args[1].GetInt32()];var ids=new Dictionary<TreeNode,int>();for(int i=0;i<nodes.Count;++i)ids[nodes[i]]=i;string before=JsonSerializer.Serialize(TreeSnapshot(nodes,ids));object actual;switch(reference){'''+''.join(branches)+'''default:throw new Exception("Unknown tree reference");}return new {actual,mutationOk=JsonSerializer.Serialize(TreeSnapshot(nodes,ids))==before};}
'''
    if language=='java':return code,'''static TreeNode readTree(JsonObject view,List<TreeNode> nodes){int offset=nodes.size();var rows=view.get("nodes").asArray();for(var value:rows)nodes.add(new TreeNode(value.asArray().get(0).asInt()));for(int i=0;i<rows.size();++i){var node=nodes.get(offset+i);var value=rows.get(i).asArray();int left=value.get(1).asInt(),right=value.get(2).asInt();if(left!=-1){node.Left=nodes.get(offset+left);node.Left.Parent=node;}if(right!=-1){node.Right=nodes.get(offset+right);node.Right.Parent=node;}}int selected=view.get("selected").asInt();return selected==-1?null:nodes.get(offset+selected);}
static int nodeId(TreeNode node,IdentityHashMap<TreeNode,Integer> ids){return node==null?-1:ids.getOrDefault(node,-2);}
static JsonArray treeSnapshot(List<TreeNode> nodes,IdentityHashMap<TreeNode,Integer> ids){var result=new JsonArray();for(var node:nodes)result.add(new JsonArray().add(node.Data).add(nodeId(node.Left,ids)).add(nodeId(node.Right,ids)).add(nodeId(node.Parent,ids)));return result;}
static JsonValue executeTree(JsonObject row){var args=row.get("arguments").asArray();String reference=row.get("ref").asString();var nodes=new ArrayList<TreeNode>();var first=readTree(args.get(0).asObject(),nodes);TreeNode second=null;if(reference.equals("4.10"))second=readTree(args.get(1).asObject(),nodes);else if(reference.equals("4.8"))second=args.get(1).asInt()==-1?null:nodes.get(args.get(1).asInt());var ids=new IdentityHashMap<TreeNode,Integer>();for(int i=0;i<nodes.size();++i)ids.put(nodes.get(i),i);String before=treeSnapshot(nodes,ids).toString();Object actual;switch(reference){'''+''.join(branches)+'''default:throw new RuntimeException("Unknown tree reference");}return new JsonObject().add("actual",encode(actual)).add("mutationOk",treeSnapshot(nodes,ids).toString().equals(before));}
'''
    dispatch='else '.join(branches)
    return code+'''
#include <memory>
TreeNode* readTree(const json& view,std::vector<std::unique_ptr<TreeNode>>& nodes){size_t offset=nodes.size();const auto& rows=view["nodes"];for(const auto& row:rows)nodes.push_back(std::make_unique<TreeNode>(row[0].get<int>()));for(size_t i=0;i<rows.size();++i){auto node=nodes[offset+i].get();int left=rows[i][1].get<int>(),right=rows[i][2].get<int>();if(left!=-1){node->Left=nodes[offset+left].get();node->Left->Parent=node;}if(right!=-1){node->Right=nodes[offset+right].get();node->Right->Parent=node;}}int selected=view["selected"].get<int>();return selected==-1?nullptr:nodes[offset+selected].get();}
int nodeId(TreeNode* node,const std::unordered_map<TreeNode*,int>& ids){if(!node)return -1;auto found=ids.find(node);return found==ids.end()?-2:found->second;}
json treeSnapshot(const std::vector<std::unique_ptr<TreeNode>>& nodes,const std::unordered_map<TreeNode*,int>& ids){json result=json::array();for(const auto& item:nodes){auto node=item.get();result.push_back({node->Data,nodeId(node->Left,ids),nodeId(node->Right,ids),nodeId(node->Parent,ids)});}return result;}
json executeTree(const json& row){const auto& args=row["arguments"];std::string ref=row["ref"].get<std::string>();std::vector<std::unique_ptr<TreeNode>> nodes;TreeNode* first=readTree(args[0],nodes);TreeNode* second=nullptr;if(ref=="4.10")second=readTree(args[1],nodes);else if(ref=="4.8"){int index=args[1].get<int>();second=index==-1?nullptr:nodes[index].get();}std::unordered_map<TreeNode*,int> ids;for(size_t i=0;i<nodes.size();++i)ids[nodes[i].get()]=static_cast<int>(i);json before=treeSnapshot(nodes,ids),actual;
'''+dispatch+'''else throw std::runtime_error("Unknown tree reference");return json{{"actual",actual},{"mutationOk",treeSnapshot(nodes,ids)==before}};}
''',''


def attach(value,language,entries,starters):
    external,internal=pieces(language,entries,starters)
    selected_refs=[entry["ref"] for entry in entries]
    plain=base_header(entries[0]['ref'],language)
    owned=header(entries[0]['ref'],language)
    value=value.replace(plain,owned,1) if plain else TREE[language]+value
    if language=='python':return value.replace('def execute(row):',external+"\ndef execute(row):\n    if row['ref'] in "+repr(selected_refs)+": return executeTree(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',external+'\nfunction execute(row){if('+json.dumps(selected_refs)+'.includes(row.ref))return executeTree(row);',1)
    if language=='csharp':return value.replace('class Harness {',external+'\nclass Harness {\n'+internal,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if('+ '||'.join('row.GetProperty("ref").GetString()=="'+ref+'"' for ref in selected_refs)+')return ExecuteTree(row);',1)
    if language=='java':return value.replace('public class Harness {',external+'\npublic class Harness {\n'+internal,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if('+ '||'.join('row.get("ref").asString().equals("'+ref+'")' for ref in selected_refs)+')return executeTree(row);',1)
    return value.replace('json execute(const json& row){',external+'\njson execute(const json& row){if('+ '||'.join('row["ref"]=="'+ref+'"' for ref in selected_refs)+')return executeTree(row);',1)

def common_support(language):
    # Extract only this bank-owned, expected-answer-free decoder/snapshot template.
    external,internal=pieces(language,[],False)
    markers={'python':('\ndef nodeId(', '\ndef executeTree('),'javascript':('\nfunction nodeId(', '\nfunction executeTree('),'cpp':('#include <memory>', '\njson executeTree(')}
    if language in markers:
        start,end=markers[language]
        return external[external.index(start):external.index(end)],''
    marker='static object ExecuteTree(' if language=='csharp' else 'static JsonValue executeTree('
    return '',internal[:internal.index(marker)]
