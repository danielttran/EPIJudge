"""Project newly returned trees/linked lists without computing any expected answer."""
import json
from models04 import TREE,DEPTH,header
from models08 import header as base_header
from harness_tree04 import common_support


def projectors(language,newtree,depths):
    outside=[];inside=[]
    if language=='python':
        if newtree:outside.append('''
def projectNewTree(root,limit):
    nodes=[];ids={};valid=True
    if root is not None:
        if isinstance(root,TreeNode):ids[id(root)]=0;nodes.append(root)
        else:valid=False
    index=0
    while index<len(nodes):
        node=nodes[index];index+=1
        if type(node.Data) is not int or not -2147483648<=node.Data<=2147483647:valid=False
        for child in (node.Left,node.Right):
            if child is None:continue
            if not isinstance(child,TreeNode):valid=False;continue
            if id(child) not in ids:
                if len(nodes)>=limit:valid=False;continue
                ids[id(child)]=len(nodes);nodes.append(child)
    rows=[[node.Data,nodeId(node.Left,ids),nodeId(node.Right,ids),nodeId(node.Parent,ids)] for node in nodes]
    return dict(root=nodeId(root,ids),nodes=rows),valid
''')
        if depths:outside.append('''
def projectDepths(heads,ids,limit):
    if type(heads) is not list:return [],False
    rows=[];seen=set();valid=True
    for head in heads:
        if len(rows)>=limit:valid=False;break
        row=[];link=head
        while link is not None:
            if not isinstance(link,DepthLink) or id(link) in seen or len(seen)>=limit:valid=False;break
            seen.add(id(link));row.append(nodeId(link.Value,ids));link=link.Next
        rows.append(row)
    return rows,valid
''')
    elif language=='javascript':
        if newtree:outside.append('''
function projectNewTree(root,limit){const nodes=[],ids=new Map();let valid=true;if(root!==null){if(root instanceof TreeNode){ids.set(root,0);nodes.push(root);}else valid=false;}for(let i=0;i<nodes.length;++i){const node=nodes[i];if(!Number.isInteger(node.Data)||node.Data< -2147483648||node.Data>2147483647)valid=false;for(const child of [node.Left,node.Right]){if(child===null)continue;if(!(child instanceof TreeNode)){valid=false;continue;}if(!ids.has(child)){if(nodes.length>=limit){valid=false;continue;}ids.set(child,nodes.length);nodes.push(child);}}}return {actual:{root:nodeId(root,ids),nodes:treeSnapshot(nodes,ids)},valid};}
''')
        if depths:outside.append('''
function projectDepths(heads,ids,limit){if(!Array.isArray(heads))return {actual:[],valid:false};const rows=[],seen=new Set();let valid=true;for(const head of heads){if(rows.length>=limit){valid=false;break;}const row=[];let link=head;while(link!==null){if(!(link instanceof DepthLink)||seen.has(link)||seen.size>=limit){valid=false;break;}seen.add(link);row.push(nodeId(link.Value,ids));link=link.Next;}rows.push(row);}return {actual:rows,valid};}
''')
    elif language=='csharp':
        if newtree:inside.append('''static (object Actual,bool Valid) ProjectNewTree(TreeNode? root,int limit){var nodes=new List<TreeNode>();var ids=new Dictionary<TreeNode,int>();bool valid=true;if(root!=null){ids[root]=0;nodes.Add(root);}for(int i=0;i<nodes.Count;++i)foreach(var child in new[]{nodes[i].Left,nodes[i].Right})if(child!=null&&!ids.ContainsKey(child)){if(nodes.Count>=limit){valid=false;continue;}ids[child]=nodes.Count;nodes.Add(child);}return(new {root=NodeId(root,ids),nodes=TreeSnapshot(nodes,ids)},valid);}
''')
        if depths:inside.append('''static (object Actual,bool Valid) ProjectDepths(List<DepthLink>? heads,Dictionary<TreeNode,int> ids,int limit){var rows=new List<List<int>>();if(heads==null)return(rows,false);var seen=new HashSet<DepthLink>();bool valid=true;foreach(var head in heads){if(rows.Count>=limit){valid=false;break;}var row=new List<int>();DepthLink? link=head;while(link!=null){if(seen.Count>=limit||!seen.Add(link)){valid=false;break;}row.Add(NodeId(link.Value,ids));link=link.Next;}rows.Add(row);}return(rows,valid);}
''')
    elif language=='java':
        if newtree or depths:inside.append('record Projection(JsonValue actual,boolean valid){}\n')
        if newtree:inside.append('''static Projection projectNewTree(TreeNode root,int limit){var nodes=new ArrayList<TreeNode>();var ids=new IdentityHashMap<TreeNode,Integer>();boolean valid=true;if(root!=null){ids.put(root,0);nodes.add(root);}for(int i=0;i<nodes.size();++i)for(var child:new TreeNode[]{nodes.get(i).Left,nodes.get(i).Right})if(child!=null&&!ids.containsKey(child)){if(nodes.size()>=limit){valid=false;continue;}ids.put(child,nodes.size());nodes.add(child);}return new Projection(new JsonObject().add("root",nodeId(root,ids)).add("nodes",treeSnapshot(nodes,ids)),valid);}
''')
        if depths:inside.append('''static Projection projectDepths(List<DepthLink> heads,IdentityHashMap<TreeNode,Integer> ids,int limit){var rows=new JsonArray();if(heads==null)return new Projection(rows,false);Set<DepthLink> seen=Collections.newSetFromMap(new IdentityHashMap<>());boolean valid=true;for(var head:heads){if(rows.size()>=limit){valid=false;break;}var row=new JsonArray();var link=head;while(link!=null){if(seen.size()>=limit||!seen.add(link)){valid=false;break;}row.add(nodeId(link.Value,ids));link=link.Next;}rows.add(row);}return new Projection(rows,valid);}
''')
    else:
        if newtree:outside.append('''std::pair<json,bool> projectNewTree(TreeNode* root,int limit){std::vector<TreeNode*> nodes;std::unordered_map<TreeNode*,int> ids;bool valid=true;if(root){ids[root]=0;nodes.push_back(root);}for(size_t i=0;i<nodes.size();++i)for(auto child:{nodes[i]->Left,nodes[i]->Right})if(child&&ids.find(child)==ids.end()){if(nodes.size()>=static_cast<size_t>(limit)){valid=false;continue;}ids[child]=static_cast<int>(nodes.size());nodes.push_back(child);}json rows=json::array();for(auto node:nodes)rows.push_back({node->Data,nodeId(node->Left,ids),nodeId(node->Right,ids),nodeId(node->Parent,ids)});json actual={{"root",nodeId(root,ids)},{"nodes",rows}};for(auto node:nodes)delete node;return {actual,valid};}
''')
        if depths:outside.append('''#include <unordered_set>
std::pair<json,bool> projectDepths(const std::vector<DepthLink*>& heads,const std::unordered_map<TreeNode*,int>& ids,int limit){json rows=json::array();std::unordered_set<DepthLink*> seen;bool valid=true;for(auto head:heads){if(rows.size()>=static_cast<size_t>(limit)){valid=false;break;}json row=json::array();auto link=head;while(link){if(seen.size()>=static_cast<size_t>(limit)||!seen.insert(link).second){valid=false;break;}row.push_back(nodeId(link->Value,ids));link=link->Next;}rows.push_back(row);}for(auto link:seen)delete link;return {rows,valid};}
''')
    return '\n'.join(outside),'\n'.join(inside)


def parts(language,entries,starters,needs_common):
    declarations=[]
    for entry in entries:
        code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
        if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_'+entry['ref'].replace('.','_'),1)
        declarations.append(code)
    refs={entry['ref'] for entry in entries}
    newtree='4.2' in refs;depths='4.3' in refs;sequences='4.9' in refs;rooted=depths or sequences
    shared_out,shared_in=common_support(language) if needs_common else ('','')
    projected_out,projected_in=projectors(language,newtree,depths)
    external='\n'.join(declarations)+'\n'+shared_out+'\n'+projected_out
    internal=shared_in+'\n'+projected_in
    if language=='python':
        handler="\ndef executeTreeOutput(row):\n    args=row['arguments'];ref=row['ref']\n"
        if newtree:handler+='''    if ref=='4.2':
        values=args[0];before=values.copy()
        actual,valid=projectNewTree(CreateMinimalBst(values),len(values)+1)
        return dict(actual=actual,mutationOk=valid and values==before and all(type(v) is int for v in values))
'''
        if rooted:
            handler+='''    nodes=[];root=readTree(args[0],nodes);ids={id(node):index for index,node in enumerate(nodes)};before=treeSnapshot(nodes,ids)
    valid=True
'''
            if depths:handler+="    if ref=='4.3':actual,valid=projectDepths(LinkedListsByDepth(root),ids,len(nodes)+1)\n"
            if sequences:handler+=("    elif" if depths else "    if")+" ref=='4.9':\n        actual=BstInsertionSequences(root)\n        valid=type(actual) is list and all(type(row) is list and all(type(v) is int and -2147483648<=v<=2147483647 for v in row) for row in actual)\n"
            handler+="    else:raise ValueError('Unknown tree output reference')\n    return dict(actual=actual,mutationOk=valid and all(type(node.Data) is int for node in nodes) and treeSnapshot(nodes,ids)==before)\n"
        else:handler+="    raise ValueError('Unknown tree output reference')\n"
        return external+handler,internal
    if language=='javascript':
        handler='\nfunction executeTreeOutput(row){const args=row.arguments,ref=row.ref;'
        if newtree:handler+="if(ref==='4.2'){const values=args[0],before=JSON.stringify(values),projected=projectNewTree(CreateMinimalBst(values),values.length+1);return {actual:projected.actual,mutationOk:projected.valid&&JSON.stringify(values)===before&&values.every(Number.isInteger)};}"
        if rooted:
            handler+='const nodes=[],root=readTree(args[0],nodes),ids=new Map(nodes.map((node,index)=>[node,index])),before=JSON.stringify(treeSnapshot(nodes,ids));let actual,valid=true;'
            if depths:handler+="if(ref==='4.3'){const projected=projectDepths(LinkedListsByDepth(root),ids,nodes.length+1);actual=projected.actual;valid=projected.valid;}"
            if sequences:handler+=('else ' if depths else '')+"if(ref==='4.9'){actual=BstInsertionSequences(root);valid=Array.isArray(actual)&&actual.every(row=>Array.isArray(row)&&row.every(v=>Number.isInteger(v)&&v>=-2147483648&&v<=2147483647));}"
            handler+="else throw new Error('Unknown tree output reference');return {actual,mutationOk:valid&&nodes.every(node=>Number.isInteger(node.Data)&&node.Data>=-2147483648&&node.Data<=2147483647)&&JSON.stringify(treeSnapshot(nodes,ids))===before};}"
        else:handler+="throw new Error('Unknown tree output reference');}"
        return external+handler,internal
    if language=='csharp':
        handler='static object ExecuteTreeOutput(JsonElement row){var args=row.GetProperty("arguments");string reference=row.GetProperty("ref").GetString()!;'
        if newtree:handler+='if(reference=="4.2"){var values=JsonSerializer.Deserialize<int[]>(args[0].GetRawText())!;var saved=values.ToArray();var projection=ProjectNewTree(new Solution_4_2().CreateMinimalBst(values),values.Length+1);return new {actual=projection.Actual,mutationOk=projection.Valid&&values.SequenceEqual(saved)};}'
        if rooted:
            handler+='var nodes=new List<TreeNode>();var root=ReadTree(args[0],nodes);var ids=new Dictionary<TreeNode,int>();for(int i=0;i<nodes.Count;++i)ids[nodes[i]]=i;string before=JsonSerializer.Serialize(TreeSnapshot(nodes,ids));object actual;bool valid=true;switch(reference){'
            if depths:handler+='case "4.3":var projection=ProjectDepths(new Solution_4_3().LinkedListsByDepth(root),ids,nodes.Count+1);actual=projection.Actual;valid=projection.Valid;break;'
            if sequences:handler+='case "4.9":actual=new Solution_4_9().BstInsertionSequences(root);break;'
            handler+='default:throw new Exception("Unknown tree output reference");}return new {actual,mutationOk=valid&&JsonSerializer.Serialize(TreeSnapshot(nodes,ids))==before};}'
        else:handler+='throw new Exception("Unknown tree output reference");}'
        return external,internal+handler
    if language=='java':
        handler='static JsonValue executeTreeOutput(JsonObject row){var args=row.get("arguments").asArray();String reference=row.get("ref").asString();'
        if newtree:handler+='if(reference.equals("4.2")){int[] values=integers(args.get(0).asArray()),saved=values.clone();var projection=projectNewTree(new Solution_4_2().CreateMinimalBst(values),values.length+1);return new JsonObject().add("actual",projection.actual()).add("mutationOk",projection.valid()&&Arrays.equals(values,saved));}'
        if rooted:
            handler+='var nodes=new ArrayList<TreeNode>();var root=readTree(args.get(0).asObject(),nodes);var ids=new IdentityHashMap<TreeNode,Integer>();for(int i=0;i<nodes.size();++i)ids.put(nodes.get(i),i);String before=treeSnapshot(nodes,ids).toString();JsonValue actual;boolean valid=true;switch(reference){'
            if depths:handler+='case "4.3":var projection=projectDepths(new Solution_4_3().LinkedListsByDepth(root),ids,nodes.size()+1);actual=projection.actual();valid=projection.valid();break;'
            if sequences:handler+='case "4.9":actual=encode(new Solution_4_9().BstInsertionSequences(root));break;'
            handler+='default:throw new RuntimeException("Unknown tree output reference");}return new JsonObject().add("actual",actual).add("mutationOk",valid&&treeSnapshot(nodes,ids).toString().equals(before));}'
        else:handler+='throw new RuntimeException("Unknown tree output reference");}'
        return external,internal+handler
    handler='\njson executeTreeOutput(const json& row){const auto& args=row["arguments"];std::string ref=row["ref"].get<std::string>();'
    if newtree:handler+='if(ref=="4.2"){auto values=args[0].get<std::vector<int>>(),saved=values;auto projection=projectNewTree(Solution_4_2().CreateMinimalBst(values),static_cast<int>(values.size())+1);return json{{"actual",projection.first},{"mutationOk",projection.second&&values==saved}};}'
    if rooted:
        handler+='std::vector<std::unique_ptr<TreeNode>> nodes;auto root=readTree(args[0],nodes);std::unordered_map<TreeNode*,int> ids;for(size_t i=0;i<nodes.size();++i)ids[nodes[i].get()]=static_cast<int>(i);json before=treeSnapshot(nodes,ids),actual;bool valid=true;'
        if depths:handler+='if(ref=="4.3"){auto projection=projectDepths(Solution_4_3().LinkedListsByDepth(root),ids,static_cast<int>(nodes.size())+1);actual=projection.first;valid=projection.second;}'
        if sequences:handler+=('else ' if depths else '')+'if(ref=="4.9")actual=Solution_4_9().BstInsertionSequences(root);'
        handler+='else throw std::runtime_error("Unknown tree output reference");return json{{"actual",actual},{"mutationOk",valid&&treeSnapshot(nodes,ids)==before}};}'
    else:handler+='throw std::runtime_error("Unknown tree output reference");}'
    return external+handler,internal


def attach(value,language,entries,starters,needs_common):
    external,internal=parts(language,entries,starters,needs_common)
    # Keep the full owned header contiguous for separate-module extraction.
    if TREE[language] not in value:
        representative='4.3' if any(e['ref']=='4.3' for e in entries) else entries[0]['ref']
        plain=base_header(representative,language);owned=header(representative,language)
        value=value.replace(plain,owned,1) if plain else owned+value
    elif any(e['ref']=='4.3' for e in entries) and DEPTH[language] not in value:
        value=value.replace(TREE[language],TREE[language]+DEPTH[language],1)
    refs=[e['ref'] for e in entries]
    if language=='python':return value.replace('def execute(row):',external+"\ndef execute(row):\n    if row['ref'] in "+repr(refs)+": return executeTreeOutput(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',external+'\nfunction execute(row){if('+json.dumps(refs)+'.includes(row.ref))return executeTreeOutput(row);',1)
    if language=='csharp':return value.replace('class Harness {',external+'\nclass Harness {\n'+internal,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if('+ '||'.join('row.GetProperty("ref").GetString()=="'+ref+'"' for ref in refs)+')return ExecuteTreeOutput(row);',1)
    if language=='java':return value.replace('public class Harness {',external+'\npublic class Harness {\n'+internal,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if('+ '||'.join('row.get("ref").asString().equals("'+ref+'")' for ref in refs)+')return executeTreeOutput(row);',1)
    return value.replace('json execute(const json& row){',external+'\njson execute(const json& row){if('+ '||'.join('row["ref"]=="'+ref+'"' for ref in refs)+')return executeTreeOutput(row);',1)
