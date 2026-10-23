"""Decode original mutable BiNodes and observe real previous/next identities."""
from models08 import header as base_header
from models_binode17 import BINODE

def parts(language,code):
    if language=='python':return code+'''
def executeBiNode(row):
    wire=row['arguments'][0];rows=wire['nodes'];pool=[BiNode(v[0]) for v in rows]
    for node,raw in zip(pool,rows):
        node.Node1=None if raw[1]<0 else pool[raw[1]]
        node.Node2=None if raw[2]<0 else pool[raw[2]]
    identities={id(node):i for i,node in enumerate(pool)}
    def identity(node):return -1 if node is None else identities.get(id(node),-2)
    head=ConvertBiNode(None if wire['selected']<0 else pool[wire['selected']]);node=head
    order=[];values=[];previous=[];nexts=[];seen=set();cycle=False
    while node is not None:
        index=identity(node)
        if index<0:break
        if index in seen:cycle=True;break
        seen.add(index);order.append(index);values.append(node.Data);previous.append(identity(node.Node1));nexts.append(identity(node.Node2));node=node.Node2
    actual=dict(head=identity(head),order=order,values=values,previous=previous,next=nexts,cycle=cycle)
    return dict(actual=actual,mutationOk=all(type(node.Data) is int and node.Data==raw[0] for node,raw in zip(pool,rows)))
''',''
    if language=='javascript':return code+'''
function executeBiNode(row){const wire=row.arguments[0],rows=wire.nodes,pool=rows.map(raw=>new BiNode(raw[0]));for(let i=0;i<pool.length;++i){pool[i].Node1=rows[i][1]<0?null:pool[rows[i][1]];pool[i].Node2=rows[i][2]<0?null:pool[rows[i][2]];}const identities=new Map(pool.map((node,i)=>[node,i])),identity=node=>node===null?-1:identities.has(node)?identities.get(node):-2,head=ConvertBiNode(wire.selected<0?null:pool[wire.selected]),order=[],values=[],previous=[],next=[],seen=new Set();let node=head,cycle=false;while(node!==null){const index=identity(node);if(index<0)break;if(seen.has(index)){cycle=true;break;}seen.add(index);order.push(index);values.push(node.Data);previous.push(identity(node.Node1));next.push(identity(node.Node2));node=node.Node2;}return {actual:{head:identity(head),order,values,previous,next,cycle},mutationOk:pool.every((node,i)=>Number.isInteger(node.Data)&&node.Data===rows[i][0])};}
''',''
    if language=='csharp':return code,'''static object ExecuteBiNode(JsonElement row){var wire=row.GetProperty("arguments")[0];var rows=wire.GetProperty("nodes").EnumerateArray().Select(v=>JsonSerializer.Deserialize<int[]>(v.GetRawText())!).ToArray();var pool=rows.Select(v=>new BiNode(v[0])).ToArray();for(int i=0;i<pool.Length;++i){pool[i].Node1=rows[i][1]<0?null:pool[rows[i][1]];pool[i].Node2=rows[i][2]<0?null:pool[rows[i][2]];}var identities=new Dictionary<BiNode,int>(ReferenceEqualityComparer.Instance);for(int i=0;i<pool.Length;++i)identities[pool[i]]=i;int Identity(BiNode? node)=>node is null?-1:identities.GetValueOrDefault(node,-2);int root=wire.GetProperty("selected").GetInt32();var head=new Solution_17_12().ConvertBiNode(root<0?null:pool[root]);var node=head;var order=new List<int>();var values=new List<int>();var previous=new List<int>();var next=new List<int>();var seen=new HashSet<int>();bool cycle=false;while(node is not null){int index=Identity(node);if(index<0)break;if(!seen.Add(index)){cycle=true;break;}order.Add(index);values.Add(node.Data);previous.Add(Identity(node.Node1));next.Add(Identity(node.Node2));node=node.Node2;}return new {actual=new {head=Identity(head),order,values,previous,next,cycle},mutationOk=pool.Select((value,i)=>value.Data==rows[i][0]).All(v=>v)};}
'''
    if language=='java':return code,'''static JsonValue executeBiNode(JsonObject row){var wire=row.get("arguments").asArray().get(0).asObject();var raw=wire.get("nodes").asArray();int[][] rows=new int[raw.size()][];BiNode[] pool=new BiNode[raw.size()];for(int i=0;i<pool.length;++i){rows[i]=integers(raw.get(i).asArray());pool[i]=new BiNode(rows[i][0]);}for(int i=0;i<pool.length;++i){pool[i].Node1=rows[i][1]<0?null:pool[rows[i][1]];pool[i].Node2=rows[i][2]<0?null:pool[rows[i][2]];}var identities=new IdentityHashMap<BiNode,Integer>();for(int i=0;i<pool.length;++i)identities.put(pool[i],i);java.util.function.ToIntFunction<BiNode> identity=node->node==null?-1:identities.getOrDefault(node,-2);int root=wire.get("selected").asInt();BiNode head=new Solution_17_12().ConvertBiNode(root<0?null:pool[root]),node=head;var order=new JsonArray();var values=new JsonArray();var previous=new JsonArray();var next=new JsonArray();var seen=new HashSet<Integer>();boolean cycle=false;while(node!=null){int index=identity.applyAsInt(node);if(index<0)break;if(!seen.add(index)){cycle=true;break;}order.add(index);values.add(node.Data);previous.add(identity.applyAsInt(node.Node1));next.add(identity.applyAsInt(node.Node2));node=node.Node2;}boolean mutationOk=true;for(int i=0;i<pool.length;++i)mutationOk&=pool[i].Data==rows[i][0];return new JsonObject().add("actual",new JsonObject().add("head",identity.applyAsInt(head)).add("order",order).add("values",values).add("previous",previous).add("next",next).add("cycle",cycle)).add("mutationOk",mutationOk);}
'''
    return '#include <memory>\n#include <unordered_map>\n#include <unordered_set>\n'+code+'''
json executeBiNode(const json& row){const auto& wire=row["arguments"][0];auto rows=wire["nodes"].get<std::vector<std::vector<int>>>();std::vector<std::unique_ptr<BiNode>> pool;for(const auto& raw:rows)pool.emplace_back(std::make_unique<BiNode>(raw[0]));for(size_t i=0;i<pool.size();++i){pool[i]->Node1=rows[i][1]<0?nullptr:pool[rows[i][1]].get();pool[i]->Node2=rows[i][2]<0?nullptr:pool[rows[i][2]].get();}std::unordered_map<BiNode*,int> identities;for(size_t i=0;i<pool.size();++i)identities[pool[i].get()]=static_cast<int>(i);auto identity=[&](BiNode* node){if(node==nullptr)return -1;auto found=identities.find(node);return found==identities.end()?-2:found->second;};int root=wire["selected"].get<int>();BiNode* head=Solution_17_12().ConvertBiNode(root<0?nullptr:pool[root].get());BiNode* node=head;std::vector<int> order,values,previous,next;std::unordered_set<int> seen;bool cycle=false;while(node!=nullptr){int index=identity(node);if(index<0)break;if(!seen.insert(index).second){cycle=true;break;}order.push_back(index);values.push_back(node->Data);previous.push_back(identity(node->Node1));next.push_back(identity(node->Node2));node=node->Node2;}bool mutationOk=true;for(size_t i=0;i<pool.size();++i)mutationOk=mutationOk&&pool[i]->Data==rows[i][0];return json{{"actual",json{{"head",identity(head)},{"order",order},{"values",values},{"previous",previous},{"next",next},{"cycle",cycle}}},{"mutationOk",mutationOk}};}
''',''

def attach(value,language,entry,starters):
    plain=base_header('17.12',language)
    value=value.replace(plain,plain+BINODE[language],1) if plain else BINODE[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_17_12',1)
    outside,inside=parts(language,code)
    if language=='python':return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='17.12': return executeBiNode(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="17.12")return executeBiNode(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="17.12")return ExecuteBiNode(row);',1)
    if language=='java':return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("17.12"))return executeBiNode(row);',1)
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="17.12")return executeBiNode(row);',1)
