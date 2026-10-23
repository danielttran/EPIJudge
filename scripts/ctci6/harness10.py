"""Existing value adapter plus opaque Listy and rank-transcript dispatch."""
import json
from core import ROOT
from models08 import header as base_header
from models10 import LISTY
from harness_file10 import attach as attach_file
from harness08_typed import source as typed_source

SPECIAL=('10.4','10.10')

def listy_parts(language,code,cls):
    if language=='python':
        return code+'''
class JudgeListy(Listy):
    def __init__(self, data):
        self.__data=data
        self.probes=0
        self.budget=4*(len(data)+1).bit_length()+8
    def ElementAt(self,index):
        self.probes+=1
        if self.probes>self.budget:raise RuntimeError('Listy query budget exceeded')
        return self.__data[index] if 0<=index<len(self.__data) else -1
def executeListy(row):
    data=row['arguments'][0];before=data.copy();provided=JudgeListy(data)
    actual=SearchWithoutSize(provided,row['arguments'][1])
    return dict(actual=actual,mutationOk=type(actual) is int and data==before and all(type(v) is int for v in data),probes=provided.probes)
''',''
    if language=='javascript':
        return code+'''
class JudgeListy extends Listy {#data;constructor(data){super();this.#data=data;this.probes=0;let power=1,steps=0;while(power<data.length+2){power*=2;++steps;}this.budget=4*steps+8;}ElementAt(index){++this.probes;if(this.probes>this.budget)throw new Error('Listy query budget exceeded');return index>=0&&index<this.#data.length?this.#data[index]:-1;}}
function executeListy(row){const data=row.arguments[0],before=data.slice(),provided=new JudgeListy(data),actual=SearchWithoutSize(provided,row.arguments[1]);return {actual,mutationOk:Number.isInteger(actual)&&data.length===before.length&&data.every((v,i)=>v===before[i]),probes:provided.probes};}
''',''
    if language=='csharp':
        outside=code+'''
sealed class JudgeListy:Listy {private readonly int[] data;private readonly int budget;public int Probes;public JudgeListy(int[] data){this.data=data;int power=1,steps=0;while(power<data.Length+2){power<<=1;++steps;}budget=4*steps+8;}public override int ElementAt(int index){++Probes;if(Probes>budget)throw new InvalidOperationException("Listy query budget exceeded");return index>=0&&index<data.Length?data[index]:-1;}}
'''
        inside='''static object ExecuteListy(JsonElement row){var args=row.GetProperty("arguments");int[] data=JsonSerializer.Deserialize<int[]>(args[0].GetRawText())!;var before=data.ToArray();var provided=new JudgeListy(data);int actual=new USER_CLASS().SearchWithoutSize(provided,args[1].GetInt32());return new {actual,mutationOk=data.SequenceEqual(before),probes=provided.Probes};}
'''
        return outside,inside.replace('USER_CLASS',cls)
    if language=='java':
        outside=code+'''
class JudgeListy extends Listy {private final int[] data;private final int budget;int probes;JudgeListy(int[] data){this.data=data;int power=1,steps=0;while(power<data.length+2){power<<=1;++steps;}budget=4*steps+8;}public int ElementAt(int index){++probes;if(probes>budget)throw new IllegalStateException("Listy query budget exceeded");return index>=0&&index<data.length?data[index]:-1;}}
'''
        inside='''static JsonValue executeListy(JsonObject row){var args=row.get("arguments").asArray();int[] data=integers(args.get(0).asArray()),before=data.clone();var provided=new JudgeListy(data);int actual=new USER_CLASS().SearchWithoutSize(provided,args.get(1).asInt());return new JsonObject().add("actual",actual).add("mutationOk",Arrays.equals(data,before)).add("probes",provided.probes);}
'''
        return outside,inside.replace('USER_CLASS',cls)
    outside=code+'''
class JudgeListy:public Listy {std::vector<int>& data;int budget;public:int probes=0;explicit JudgeListy(std::vector<int>& data):data(data){int power=1,steps=0;while(power<static_cast<int>(data.size())+2){power<<=1;++steps;}budget=4*steps+8;}int ElementAt(int index) override{++probes;if(probes>budget)throw std::runtime_error("Listy query budget exceeded");return index>=0&&index<static_cast<int>(data.size())?data[index]:-1;}};
json executeListy(const json& row){auto data=row["arguments"][0].get<std::vector<int>>(),before=data;JudgeListy provided(data);int actual=USER_CLASS().SearchWithoutSize(provided,row["arguments"][1].get<int>());return json{{"actual",actual},{"mutationOk",data==before},{"probes",provided.probes}};}
'''
    return outside.replace('USER_CLASS',cls),''

def rank_parts(language,code):
    if language=='python':return code+'''
def executeRank(row):
    operations,arguments=row['arguments'];instance=RankTracker();output=[None];valid=True
    for op,raw in zip(operations[1:],arguments[1:]):
        if op=='Track':
            value=instance.Track(raw[0]);valid=valid and value is None;output.append(value)
        elif op=='GetRank':
            value=instance.GetRank(raw[0]);valid=valid and type(value) is int and -2147483648<=value<=2147483647;output.append(value)
        else:raise ValueError('Unknown rank operation')
    return dict(actual=output,mutationOk=valid)
''',''
    if language=='javascript':return code+'''
function executeRank(row){const [operations,args]=row.arguments,instance=new RankTracker(),output=[null];let valid=true;for(let i=1;i<operations.length;++i){let value;if(operations[i]==='Track'){value=instance.Track(args[i][0]);valid=valid&&(value===undefined||value===null);output.push(value===undefined?null:value);}else if(operations[i]==='GetRank'){value=instance.GetRank(args[i][0]);valid=valid&&Number.isInteger(value)&&value>=-2147483648&&value<=2147483647;output.push(value);}else throw new Error('Unknown rank operation');}return {actual:output,mutationOk:valid};}
''',''
    if language=='csharp':return code,'''static object ExecuteRank(JsonElement row){var operations=row.GetProperty("arguments")[0];var args=row.GetProperty("arguments")[1];var instance=new RankTracker();Action<int> track=instance.Track;Func<int,int> getRank=instance.GetRank;var output=new List<object?>{null};for(int i=1;i<operations.GetArrayLength();++i){string op=operations[i].GetString()!;if(op=="Track"){track(args[i][0].GetInt32());output.Add(null);}else if(op=="GetRank")output.Add(getRank(args[i][0].GetInt32()));else throw new Exception("Unknown rank operation");}return new {actual=output,mutationOk=true};}
'''
    if language=='java':return code,'''static JsonValue executeRank(JsonObject row){var operations=row.get("arguments").asArray().get(0).asArray();var args=row.get("arguments").asArray().get(1).asArray();var instance=new RankTracker();try{if(RankTracker.class.getMethod("Track",int.class).getReturnType()!=void.class||RankTracker.class.getMethod("GetRank",int.class).getReturnType()!=int.class)throw new IllegalArgumentException("RankTracker method result types must match the API");}catch(NoSuchMethodException error){throw new IllegalArgumentException("RankTracker methods must match the API",error);}var output=new JsonArray().add(Json.NULL);for(int i=1;i<operations.size();++i){String op=operations.get(i).asString();if(op.equals("Track")){instance.Track(args.get(i).asArray().get(0).asInt());output.add(Json.NULL);}else if(op.equals("GetRank"))output.add(instance.GetRank(args.get(i).asArray().get(0).asInt()));else throw new RuntimeException("Unknown rank operation");}return new JsonObject().add("actual",output).add("mutationOk",true);}
'''
    return code+'''
#include <type_traits>
json executeRank(const json& row){const auto& operations=row["arguments"][0];const auto& args=row["arguments"][1];RankTracker instance;static_assert(std::is_same<decltype(instance.Track(0)),void>::value,"Track must return void");static_assert(std::is_same<decltype(instance.GetRank(0)),int>::value,"GetRank must return int");json output=json::array();output.push_back(nullptr);for(size_t i=1;i<operations.size();++i){auto op=operations[i].get<std::string>();if(op=="Track"){instance.Track(args[i][0].get<int>());output.push_back(nullptr);}else if(op=="GetRank")output.push_back(instance.GetRank(args[i][0].get<int>()));else throw std::runtime_error("Unknown rank operation");}return json{{"actual",output},{"mutationOk",true}};}
''',''

def source(language,starters=False,only_ref=None):
    entries=json.loads((ROOT/'ctci6/staged10/catalog.json').read_text())
    selected=[entry for entry in entries if only_ref is None or entry['ref']==only_ref]
    if not selected:raise ValueError('Unknown sorting reference')
    value=typed_source(language,starters,only_ref,staging_name='staged10',exclude_refs=SPECIAL+('10.6','10.7'),allow_empty=True)
    for entry in selected:
        if entry["ref"]=="10.6":
            from harness_external10 import attach as attach_external
            value=attach_external(value,language,entry,starters)
        if entry["ref"]=="10.7":value=attach_file(value,language,entry,starters)
    special=[entry for entry in selected if entry['ref'] in SPECIAL]
    if not special:return value
    if any(entry['ref']=='10.4' for entry in special):
        plain=base_header('10.4',language)
        value=value.replace(plain,plain+LISTY[language],1) if plain else LISTY[language]+value
    outside=[];inside=[];dispatch=[]
    for entry in special:
        code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
        cls='Solution_10_4'
        if entry['ref']=='10.4' and language not in ('python','javascript'):code=code.replace('class Solution','class '+cls,1)
        external,internal=listy_parts(language,code,cls) if entry['ref']=='10.4' else rank_parts(language,code)
        outside.append(external);inside.append(internal)
        handler='Listy' if entry['ref']=='10.4' else 'Rank'
        ref=entry['ref']
        dispatch.append(f"    if row['ref']=={ref!r}: return execute{handler}(row)\n" if language=='python' else f"if(row.ref==={json.dumps(ref)})return execute{handler}(row);" if language=='javascript' else f'if(row.GetProperty("ref").GetString()=="{ref}")return Execute{handler}(row);' if language=='csharp' else f'if(row.get("ref").asString().equals("{ref}"))return execute{handler}(row);' if language=='java' else f'if(row["ref"]=="{ref}")return execute{handler}(row);')
    external='\n'.join(outside);internal='\n'.join(inside);calls=''.join(dispatch)
    if language=='python':return value.replace('def execute(row):',external+'\ndef execute(row):\n'+calls,1)
    if language=='javascript':return value.replace('function execute(row){',external+'\nfunction execute(row){'+calls,1)
    if language=='csharp':return value.replace('class Harness {',external+'\nclass Harness {\n'+internal,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){'+calls,1)
    if language=='java':return value.replace('public class Harness {',external+'\npublic class Harness {\n'+internal,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){'+calls,1)
    return value.replace('json execute(const json& row){',external+'\njson execute(const json& row){'+calls,1)
