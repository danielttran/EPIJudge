"""Observe identities and mutations; keep algorithmic grading in corpus02.py."""

import json

from chapter02 import SPECS
from core import ROOT
from models02 import header


def source(language, starters=False, only_ref=None):
    specs = [s for s in SPECS if only_ref is None or s["ref"] == only_ref]
    catalog = json.loads((ROOT / "ctci6/staged02/catalog.json").read_text())
    catalog = [row for row in catalog if only_ref is None or row["ref"] == only_ref]
    pieces = [header(language)]
    for entry in catalog:
        code = entry["languages"][language][
            "starterCode" if starters else "solutionCode"
        ]
        if language not in ("python", "javascript"):
            code = code.replace(
                "class Solution", "class Solution_" + entry["ref"].replace(".", "_"), 1
            )
        pieces.append(code)
    if language == "python":
        pieces.append(
            PYTHON.replace(
                "METHODS_VALUE", repr({s["ref"]: s["method"] for s in specs})
            )
        )
    elif language == "javascript":
        pieces.append(
            JAVASCRIPT.replace(
                "FUNCTIONS_VALUE",
                "{"
                + ",".join(json.dumps(s["ref"]) + ":" + s["method"] for s in specs)
                + "}",
            )
        )
    elif language == "csharp":
        pieces.insert(
            0, "using System.IO;\nusing System.Reflection;\nusing System.Text.Json;\n"
        )
        pieces.append(
            CSHARP.replace(
                "METHODS_VALUE",
                "new Dictionary<string,string>{"
                + ",".join(
                    "{" + json.dumps(s["ref"]) + "," + json.dumps(s["method"]) + "}"
                    for s in specs
                )
                + "}",
            )
        )
    elif language == "java":
        pieces.insert(
            0, "import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n"
        )
        pieces.append(
            JAVA.replace(
                "METHODS_VALUE",
                "Map.of("
                + ",".join(
                    json.dumps(s["ref"]) + "," + json.dumps(s["method"]) for s in specs
                )
                + ")",
            )
        )
    else:
        pieces.insert(
            0,
            '#include <fstream>\n#include <memory>\n#include <unordered_map>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n',
        )
        dispatch = []
        for s in specs:
            arguments = {
                "2.1": "p.head",
                "2.2": "p.head, raw[1].get<int>()",
                "2.3": "p.target",
                "2.4": "p.head, raw[1].get<int>()",
                "2.5": "p.first, p.second, raw[2].get<bool>()",
                "2.6": "p.head",
                "2.7": "p.first, p.second",
                "2.8": "p.head",
            }[s["ref"]]
            call = (
                "Solution_"
                + s["ref"].replace(".", "_")
                + "()."
                + s["method"]
                + "("
                + arguments
                + ")"
            )
            dispatch.append(
                "if (ref == "
                + json.dumps(s["ref"])
                + ") { "
                + (
                    "returned = "
                    if s["result"] == "node"
                    else "boolean = "
                    if s["result"] == "b"
                    else ""
                )
                + call
                + "; }"
            )
        pieces.append(CPP.replace("DISPATCH_VALUE", "\n".join(dispatch)))
    return "\n".join(pieces)


PYTHON = """
import json
METHODS = METHODS_VALUE

def execute(row):
    ref, raw = row['ref'], row['arguments']
    originals = []
    def make(values):
        nodes = [LinkedListNode(v) for v in values]
        for a,b in zip(nodes,nodes[1:]): a.Next=b
        originals.extend(nodes)
        return nodes
    def head(nodes): return nodes[0] if nodes else None
    first = second = target = None
    if ref == '2.7':
        a,b,c = make(raw[0]),make(raw[1]),make(raw[2])
        if a: a[-1].Next=head(c)
        if b: b[-1].Next=head(c)
        first,second=head(a) if a else head(c),head(b) if b else head(c)
        h=first
    elif ref == '2.5':
        first,second=head(make(raw[0])),head(make(raw[1]))
        h=first
    else:
        a=make(raw[0]); h=head(a)
        if ref == '2.3': target=a[raw[1]] if raw[1]>=0 else None
        if ref == '2.8' and a and raw[1]>=0: a[-1].Next=a[raw[1]]
    ids={id(node):i for i,node in enumerate(originals)}
    def identify(node):
        if node is None: return None
        if not isinstance(node,LinkedListNode): raise TypeError('Return an actual node object')
        key=id(node)
        if key not in ids: ids[key]=len(ids)
        return ids[key]
    def snapshot(): return [[n.Value,identify(n.Next)] for n in originals]
    before=snapshot()
    args = [h]
    if ref in ('2.2','2.4'): args=[h,raw[1]]
    elif ref == '2.3': args=[target]
    elif ref == '2.5': args=[first,second,raw[2]]
    elif ref == '2.7': args=[first,second]
    value=globals()[METHODS[ref]](*args)
    returned=identify(value) if ref in ('2.2','2.4','2.5','2.7','2.8') else None
    boolean=value if ref in ('2.3','2.6') else None
    after=snapshot()
    current=h if ref in ('2.1','2.3') else value if ref in ('2.4','2.5') else None
    reachable,values,seen=[],[],set()
    while current is not None:
        key=identify(current)
        if key in seen: break
        seen.add(key);reachable.append(key);values.append(current.Value)
        if len(seen)>6002: raise ValueError('Output list exceeds its domain')
        current=current.Next
    return dict(before=before,after=after,returnedId=returned,returnedBool=boolean,
                reachableIds=reachable,reachableValues=values,cycle=current is not None)

results=[]
for row in json.load(open('cases.json',encoding='utf-8')):
    try: results.append(execute(row))
    except Exception as error: results.append(dict(error=repr(error)))
json.dump(results,open('results.json','w',encoding='utf-8'))
"""

JAVASCRIPT = """
const fs = require('node:fs');
const functions = FUNCTIONS_VALUE;
function execute(row) {
    const ref=row.ref,raw=row.arguments,originals=[];
    const make=values=>{const a=values.map(v=>new LinkedListNode(v));for(let i=1;i<a.length;i++)a[i-1].Next=a[i];originals.push(...a);return a;};
    const head=a=>a.length?a[0]:null;
    let h=null,first=null,second=null,target=null;
    if(ref==='2.7') {
        const a=make(raw[0]),b=make(raw[1]),c=make(raw[2]);
        if(a.length)a.at(-1).Next=head(c);if(b.length)b.at(-1).Next=head(c);
        first=a.length?head(a):head(c);second=b.length?head(b):head(c);h=first;
    } else if(ref==='2.5'){first=head(make(raw[0]));second=head(make(raw[1]));h=first;}
    else {const a=make(raw[0]);h=head(a);if(ref==='2.3')target=raw[1]>=0?a[raw[1]]:null;if(ref==='2.8'&&a.length&&raw[1]>=0)a.at(-1).Next=a[raw[1]];}
    const ids=new Map(originals.map((n,i)=>[n,i]));
    const identify=n=>{if(n===null)return null;if(!(n instanceof LinkedListNode))throw new Error('Return an actual node object');if(!ids.has(n))ids.set(n,ids.size);return ids.get(n);};
    const snapshot=()=>originals.map(n=>[n.Value,identify(n.Next)]);
    const before=snapshot();
    let args=[h];if(ref==='2.2'||ref==='2.4')args=[h,raw[1]];else if(ref==='2.3')args=[target];else if(ref==='2.5')args=[first,second,raw[2]];else if(ref==='2.7')args=[first,second];
    const value=functions[ref](...args);
    const returned=['2.2','2.4','2.5','2.7','2.8'].includes(ref)?identify(value):null;
    const boolean=['2.3','2.6'].includes(ref)?value:null,after=snapshot();
    let current=['2.1','2.3'].includes(ref)?h:['2.4','2.5'].includes(ref)?value:null;
    const reachable=[],values=[],seen=new Set();
    while(current!==null){const key=identify(current);if(seen.has(key))break;seen.add(key);reachable.push(key);values.push(current.Value);if(seen.size>6002)throw new Error('Output list exceeds domain');current=current.Next;}
    return {before,after,returnedId:returned,returnedBool:boolean,reachableIds:reachable,reachableValues:values,cycle:current!==null};
}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{try{return execute(row);}catch(error){return {error:String(error)};}});
fs.writeFileSync('results.json',JSON.stringify(results));
"""

CSHARP = """
class Harness {
static Dictionary<string,string> Methods = METHODS_VALUE;
static object Execute(JsonElement row) {
    string reference=row.GetProperty("ref").GetString()!;var raw=row.GetProperty("arguments");
    var originals=new List<LinkedListNode>();
    LinkedListNode[] Make(JsonElement values){var a=new LinkedListNode[values.GetArrayLength()];for(int i=0;i<a.Length;i++){a[i]=new LinkedListNode(values[i].GetInt32());if(i>0)a[i-1].Next=a[i];}originals.AddRange(a);return a;}
    LinkedListNode? Head(LinkedListNode[] a)=>a.Length==0?null:a[0];
    LinkedListNode? h=null,first=null,second=null,target=null;
    if(reference=="2.7"){var a=Make(raw[0]);var b=Make(raw[1]);var c=Make(raw[2]);if(a.Length>0)a[^1].Next=Head(c);if(b.Length>0)b[^1].Next=Head(c);first=a.Length>0?Head(a):Head(c);second=b.Length>0?Head(b):Head(c);h=first;}
    else if(reference=="2.5"){first=Head(Make(raw[0]));second=Head(Make(raw[1]));h=first;}
    else{var a=Make(raw[0]);h=Head(a);if(reference=="2.3")target=raw[1].GetInt32()<0?null:a[raw[1].GetInt32()];if(reference=="2.8"&&a.Length>0&&raw[1].GetInt32()>=0)a[^1].Next=a[raw[1].GetInt32()];}
    var ids=new Dictionary<LinkedListNode,int>(System.Collections.Generic.ReferenceEqualityComparer.Instance);for(int i=0;i<originals.Count;i++)ids[originals[i]]=i;
    int? Identify(LinkedListNode? n){if(n is null)return null;if(!ids.TryGetValue(n,out int index)){index=ids.Count;ids[n]=index;}return index;}
    int?[][] Snapshot()=>originals.Select(n=>new int?[]{n.Value,Identify(n.Next)}).ToArray();
    var before=Snapshot();
    object?[] arguments=reference switch{"2.2" or "2.4"=>[h,raw[1].GetInt32()],"2.3"=>[target],"2.5"=>[first,second,raw[2].GetBoolean()],"2.7"=>[first,second],_=>[h]};
    var type=typeof(Harness).Assembly.GetType("Solution_"+reference.Replace('.','_'))!;
    var value=type.GetMethod(Methods[reference])!.Invoke(Activator.CreateInstance(type),arguments);
    int? returned=reference is "2.2" or "2.4" or "2.5" or "2.7" or "2.8"?Identify((LinkedListNode?)value):null;
    bool? boolean=reference is "2.3" or "2.6"?(bool)value!:null;
    var after=Snapshot();
    var current=reference is "2.1" or "2.3"?h:reference is "2.4" or "2.5"?(LinkedListNode?)value:null;
    var reachable=new List<int>();var values=new List<int>();var seen=new HashSet<int>();
    while(current is not null){int id=Identify(current)!.Value;if(!seen.Add(id))break;reachable.Add(id);values.Add(current.Value);if(seen.Count>6002)throw new Exception("Output exceeds domain");current=current.Next;}
    return new{before,after,returnedId=returned,returnedBool=boolean,reachableIds=reachable,reachableValues=values,cycle=current is not null};
}
static void Main(){using var document=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in document.RootElement.EnumerateArray()){try{results.Add(Execute(row));}catch(Exception error){results.Add(new{error=error.ToString()});}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}
}
"""

JAVA = """
public class Harness {
static Map<String,String> METHODS=METHODS_VALUE;
static List<LinkedListNode> make(JsonValue values,List<LinkedListNode> pool){var a=new ArrayList<LinkedListNode>();for(JsonValue v:values.asArray()){var n=new LinkedListNode(v.asInt());if(!a.isEmpty())a.get(a.size()-1).Next=n;a.add(n);pool.add(n);}return a;}
static LinkedListNode head(List<LinkedListNode> a){return a.isEmpty()?null:a.get(0);}
static JsonValue identify(LinkedListNode n,IdentityHashMap<LinkedListNode,Integer> ids){if(n==null)return Json.NULL;Integer i=ids.get(n);if(i==null){i=ids.size();ids.put(n,i);}return Json.value(i);}
static JsonArray snapshot(List<LinkedListNode> pool,IdentityHashMap<LinkedListNode,Integer> ids){var out=new JsonArray();for(var n:pool)out.add(new JsonArray().add(n.Value).add(identify(n.Next,ids)));return out;}
static JsonValue execute(JsonObject row)throws Exception{
String ref=row.get("ref").asString();JsonArray raw=row.get("arguments").asArray();var pool=new ArrayList<LinkedListNode>();
LinkedListNode h=null,first=null,second=null,target=null;
if(ref.equals("2.7")){var a=make(raw.get(0),pool);var b=make(raw.get(1),pool);var c=make(raw.get(2),pool);if(!a.isEmpty())a.get(a.size()-1).Next=head(c);if(!b.isEmpty())b.get(b.size()-1).Next=head(c);first=a.isEmpty()?head(c):head(a);second=b.isEmpty()?head(c):head(b);h=first;}
else if(ref.equals("2.5")){first=head(make(raw.get(0),pool));second=head(make(raw.get(1),pool));h=first;}
else{var a=make(raw.get(0),pool);h=head(a);if(ref.equals("2.3"))target=raw.get(1).asInt()<0?null:a.get(raw.get(1).asInt());if(ref.equals("2.8")&&!a.isEmpty()&&raw.get(1).asInt()>=0)a.get(a.size()-1).Next=a.get(raw.get(1).asInt());}
var ids=new IdentityHashMap<LinkedListNode,Integer>();for(int i=0;i<pool.size();i++)ids.put(pool.get(i),i);
JsonArray before=snapshot(pool,ids);
Object[] args=switch(ref){case "2.2","2.4"->new Object[]{h,raw.get(1).asInt()};case "2.3"->new Object[]{target};case "2.5"->new Object[]{first,second,raw.get(2).asBoolean()};case "2.7"->new Object[]{first,second};default->new Object[]{h};};
Class<?> type=Class.forName("Solution_"+ref.replace('.','_'));var method=Arrays.stream(type.getMethods()).filter(m->m.getName().equals(METHODS.get(ref))).findFirst().orElseThrow();Object value=method.invoke(type.getDeclaredConstructor().newInstance(),args);
JsonValue returned=Set.of("2.2","2.4","2.5","2.7","2.8").contains(ref)?identify((LinkedListNode)value,ids):Json.NULL;
JsonValue bool=Set.of("2.3","2.6").contains(ref)?Json.value((boolean)value):Json.NULL;
JsonArray after=snapshot(pool,ids),reachable=new JsonArray(),values=new JsonArray();
LinkedListNode current=Set.of("2.1","2.3").contains(ref)?h:Set.of("2.4","2.5").contains(ref)?(LinkedListNode)value:null;
var seen=Collections.newSetFromMap(new IdentityHashMap<LinkedListNode,Boolean>());
while(current!=null){if(!seen.add(current))break;reachable.add(identify(current,ids));values.add(current.Value);if(seen.size()>6002)throw new IllegalArgumentException("Output exceeds domain");current=current.Next;}
return new JsonObject().add("before",before).add("after",after).add("returnedId",returned).add("returnedBool",bool).add("reachableIds",reachable).add("reachableValues",values).add("cycle",current!=null);
}
public static void main(String[] ignored)throws Exception{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){try{results.add(execute(row.asObject()));}catch(Throwable error){results.add(new JsonObject().add("error",error.toString()));}}Files.writeString(Path.of("results.json"),results.toString());}
}
"""

CPP = """
struct Prepared {
std::vector<std::unique_ptr<LinkedListNode>> owners;
std::vector<LinkedListNode*> originals;
LinkedListNode *head=nullptr,*first=nullptr,*second=nullptr,*target=nullptr;
std::vector<LinkedListNode*> make(const json& values){std::vector<LinkedListNode*> a;for(const auto& v:values){owners.push_back(std::make_unique<LinkedListNode>(v.get<int>()));auto n=owners.back().get();if(!a.empty())a.back()->Next=n;a.push_back(n);originals.push_back(n);}return a;}
static LinkedListNode* firstNode(const std::vector<LinkedListNode*>& a){return a.empty()?nullptr:a[0];}
};
json execute(const json& row){
std::string ref=row["ref"].get<std::string>();const auto& raw=row["arguments"];Prepared p;
if(ref=="2.7"){auto a=p.make(raw[0]),b=p.make(raw[1]),c=p.make(raw[2]);if(!a.empty())a.back()->Next=p.firstNode(c);if(!b.empty())b.back()->Next=p.firstNode(c);p.first=a.empty()?p.firstNode(c):p.firstNode(a);p.second=b.empty()?p.firstNode(c):p.firstNode(b);p.head=p.first;}
else if(ref=="2.5"){p.first=p.firstNode(p.make(raw[0]));p.second=p.firstNode(p.make(raw[1]));p.head=p.first;}
else{auto a=p.make(raw[0]);p.head=p.firstNode(a);if(ref=="2.3")p.target=raw[1].get<int>()<0?nullptr:a.at(raw[1].get<int>());if(ref=="2.8"&&!a.empty()&&raw[1].get<int>()>=0)a.back()->Next=a.at(raw[1].get<int>());}
std::unordered_map<LinkedListNode*,int> ids;for(size_t i=0;i<p.originals.size();i++)ids[p.originals[i]]=static_cast<int>(i);
auto identify=[&](LinkedListNode* n)->json{if(!n)return nullptr;auto found=ids.find(n);if(found!=ids.end())return found->second;int index=static_cast<int>(ids.size());ids[n]=index;return index;};
auto snapshot=[&](){json out=json::array();for(auto n:p.originals)out.push_back(json::array({n->Value,identify(n->Next)}));return out;};
json before=snapshot(),boolean=nullptr;LinkedListNode* returned=nullptr;
DISPATCH_VALUE
json returnedId=identify(returned),after=snapshot(),reachable=json::array(),values=json::array();
LinkedListNode* current=(ref=="2.1"||ref=="2.3")?p.head:(ref=="2.4"||ref=="2.5")?returned:nullptr;
std::unordered_set<LinkedListNode*> seen;
while(current){if(!seen.insert(current).second)break;reachable.push_back(identify(current));values.push_back(current->Value);if(seen.size()>6002)throw std::runtime_error("Output exceeds domain");current=current->Next;}
json output={{"before",before},{"after",after},{"returnedId",returnedId},{"returnedBool",boolean},{"reachableIds",reachable},{"reachableValues",values},{"cycle",current!=nullptr}};
for(const auto& item:ids)if(item.second>=static_cast<int>(p.originals.size()))delete item.first;
return output;
}
int main(){std::ifstream input("cases.json");json rows;input>>rows;json output=json::array();for(const auto& row:rows){try{output.push_back(execute(row));}catch(const std::exception& error){output.push_back(json{{"error",error.what()}});}}std::ofstream("results.json")<<output;}
"""
