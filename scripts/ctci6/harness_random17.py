"""Property-check shuffles and subset distributions via original occurrence IDs.

A subset result is lifted uniformly to compatible occurrence IDs, then its
selected/complement groups are independently shuffled. The resulting full
permutation is uniform iff the observable subset law is the desired uniform
occurrence-subset law. This reuses the established permutation checker without
forcing uniform result order or treating duplicate values as distinct values.
"""
from textwrap import indent
from models08 import header as base_header
from models_random17 import RANDOM
from random_checker17 import checker

def python_parts(code,entry):
    subset=entry['ref']=='17.3';suffix=entry['ref'].replace('.','_');name='executeRandom'+suffix
    call='result = RandomSubset(input_values,count)\n        check(input_values==original,"Preserve input values and order")' if subset else 'returned = Shuffle(input_values)\n        check(returned is None,"Shuffle must return None")\n        result = input_values'
    prelude=f'''def {name}(row):
    import math
    from types import SimpleNamespace
    original=row['arguments'][0].copy()
    count=row['arguments'][1] if {subset!r} else len(original)
    context={{'capture':False,'sampling':False,'first':[]}}
    track=5<len(original)<=64
    positions=[[0]*len(original) for _ in original] if track else []
    draw_limit=64*len(original)+128
    Mode='shuffle'
    Method='Shuffle'
    class ContractError(Exception):pass
    class NeedChoice(Exception):
        def __init__(self,lower,upper):self.lower,self.upper=lower,upper
    def check(ok,message='Random contract failed'):
        if not ok:raise ContractError(message)
    def invoke(array):
        input_values=original.copy()
        {call}
        check(type(input_values) is list and all(type(v) is int for v in input_values),'Preserve integer input members')
        check(type(result) is list and len(result)==count and all(type(v) is int for v in result),'Return the required number of integer members')
        if context['capture']:context['first']=result.copy()
        pools={{}}
        for index,value in enumerate(original):pools.setdefault(value,[]).append(index)
        labels=[]
        for value in result:
            check(value in pools and len(pools[value])>0,'Respect original occurrence multiplicities')
            pool=pools[value];slot=RandomSource.GetRandom(0,len(pool)-1) if len(pool)>1 else 0
            labels.append(pool[slot]);pool[slot]=pool[-1];pool.pop()
        if {subset!r}:
            selected=set(labels);remaining=[i for i in range(len(original)) if i not in selected]
            for group in (labels,remaining):
                for index in range(len(group)-1,0,-1):
                    other=RandomSource.GetRandom(0,index);group[index],group[other]=group[other],group[index]
            labels.extend(remaining)
        array[:]=labels
        if context['sampling'] and track:
            for position,index in enumerate(labels):positions[position][index]+=1
    class Subject:
        def Shuffle(self,array):invoke(array)
    user=SimpleNamespace(RandomSource=RandomSource)
    def fresh():return Subject()
    def call(instance,method,*args):return instance.Shuffle(*args)
    def typed_result(value,kind):check(value is None,'Return None')
'''
    engine=checker('python')
    ending='''    random_check([list(range(len(original)))])
    if track:
        expected=4096/len(original)
        for frequencies in positions:
            statistic=sum((value-expected)**2/expected for value in frequencies)
            check(statistic<4*(len(original)-1)+80,'Biased position marginals')
    return dict(actual=context['first'],mutationOk=True,uniformOk=True)
'''
    return code+'\n'+prelude+indent(engine,'    ')+ending,''

def javascript_parts(code,entry):
    subset=entry['ref']=='17.3';suffix=entry['ref'].replace('.','_');name='executeRandom'+suffix
    call="const result=RandomSubset(input,count);check(input.every((value,i)=>value===original[i])&&input.length===original.length,'Preserve input values and order');" if subset else "const returned=Shuffle(input);check(returned===undefined,'Shuffle must return undefined');const result=input;"
    prelude=f'''function {name}(row){{
const original=row.arguments[0].slice(),count={"row.arguments[1]" if subset else "original.length"},context={{capture:false,sampling:false,first:[],drawLimit:64*original.length+128}},track=original.length>5&&original.length<=64,positions=track?Array.from({{length:original.length}},()=>Array(original.length).fill(0)):[];
const Mode='shuffle',Method='Shuffle',json=JSON.stringify;
class ContractError extends Error{{}};
class NeedChoice extends Error{{constructor(lower,upper){{super('An injected choice is required');this.Lower=lower;this.Upper=upper;}}}}
function check(ok,message){{if(!ok)throw new ContractError(message);}}
function invoke(array){{const input=original.slice();{call}
check(Array.isArray(input)&&input.every(Number.isInteger),'Preserve integer input members');check(Array.isArray(result)&&result.length===count&&result.every(Number.isInteger),'Return the required number of integer members');if(context.capture)context.first=result.slice();
const pools=new Map();original.forEach((value,i)=>{{if(!pools.has(value))pools.set(value,[]);pools.get(value).push(i);}});const labels=[];
for(const value of result){{check(pools.has(value)&&pools.get(value).length>0,'Respect original occurrence multiplicities');const pool=pools.get(value),slot=pool.length>1?RandomSource.GetRandom(0,pool.length-1):0;labels.push(pool[slot]);pool[slot]=pool[pool.length-1];pool.pop();}}
if({str(subset).lower()}){{const selected=new Set(labels),remaining=Array.from({{length:original.length}},(_,i)=>i).filter(i=>!selected.has(i));for(const group of [labels,remaining])for(let i=group.length-1;i>0;--i){{const other=RandomSource.GetRandom(0,i);[group[i],group[other]]=[group[other],group[i]];}}labels.push(...remaining);}}
array.splice(0,array.length,...labels);if(context.sampling&&track)labels.forEach((index,position)=>++positions[position][index]);}}
class Subject{{Shuffle(array){{invoke(array);}}}}
function fresh(){{return new Subject();}}function call(instance,method,...args){{return instance.Shuffle(...args);}}
'''
    ending='''randomCheck([original.map((_,i)=>i)]);if(track){const expected=4096/original.length;for(const frequencies of positions){const statistic=frequencies.reduce((sum,value)=>sum+(value-expected)**2/expected,0);check(statistic<4*(original.length-1)+80,'Biased position marginals');}}return {actual:context.first,mutationOk:true,uniformOk:true};}
'''
    return code+'\n'+prelude+checker('javascript')+ending,''

def csharp_parts(code,entry):
    subset=entry['ref']=='17.3';suffix=entry['ref'].replace('.','_');audit='RandomAudit'+suffix;root='Solution_'+suffix
    call='int[] result=subject.RandomSubset(input,Count);Check(input.SequenceEqual(Original),"Preserve input values and order");' if subset else 'subject.Shuffle(input);int[] result=input;'
    wrapper=f'''static class {audit} {{
static readonly string Mode="shuffle",Method="Shuffle";static bool Capture,Sampling,Track;static int DrawLimit,Count;static int[] Original=[],First=[];static int[][] Positions=[];
sealed class ContractError(string message):Exception(message);
sealed class NeedChoice(int lower,int upper):Exception {{public int Lower=lower,Upper=upper;}}
static void Check(bool ok,string message){{if(!ok)throw new ContractError(message);}}
sealed class Subject {{private readonly {root} subject=new();public void Shuffle(int[] array){{var input=(int[])Original.Clone();{call}
Check(result is not null&&result.Length==Count,"Return the required number of integers");if(Capture)First=(int[])result.Clone();var pools=new Dictionary<int,List<int>>();for(int i=0;i<Original.Length;++i){{if(!pools.TryGetValue(Original[i],out var pool)){{pool=new();pools[Original[i]]=pool;}}pool.Add(i);}}var labels=new List<int>();foreach(int value in result){{Check(pools.TryGetValue(value,out var pool)&&pool.Count>0,"Respect original occurrence multiplicities");int slot=pool!.Count>1?RandomSource.GetRandom(0,pool.Count-1):0;labels.Add(pool[slot]);pool[slot]=pool[^1];pool.RemoveAt(pool.Count-1);}}
if({str(subset).lower()}){{var selected=labels.ToHashSet();var remaining=Enumerable.Range(0,Original.Length).Where(i=>!selected.Contains(i)).ToList();foreach(var group in new[]{{labels,remaining}})for(int i=group.Count-1;i>0;--i){{int other=RandomSource.GetRandom(0,i);(group[i],group[other])=(group[other],group[i]);}}labels.AddRange(remaining);}}labels.CopyTo(array);if(Sampling&&Track)for(int i=0;i<array.Length;++i)Positions[i][array[i]]++;}}}}
static object Fresh()=>new Subject();static object? Call(object instance,string method,params object?[] args){{((Subject)instance).Shuffle((int[])args[0]!);return null;}}
'''
    ending=f'''public static object Run(JsonElement row){{Original=JsonSerializer.Deserialize<int[]>(row.GetProperty("arguments")[0].GetRawText())!;Count={"row.GetProperty(\"arguments\")[1].GetInt32()" if subset else "Original.Length"};First=[];Capture=false;Sampling=false;Track=Original.Length>5&&Original.Length<=64;DrawLimit=64*Original.Length+128;Positions=Track?Enumerable.Range(0,Original.Length).Select(_=>new int[Original.Length]).ToArray():[];RandomCheck(JsonSerializer.SerializeToElement(new[]{{Enumerable.Range(0,Original.Length).ToArray()}}));if(Track){{double expected=4096.0/Original.Length;foreach(var frequencies in Positions)Check(frequencies.Sum(value=>(value-expected)*(value-expected)/expected)<4*(Original.Length-1)+80,"Biased position marginals");}}return new {{actual=First,mutationOk=true,uniformOk=true}};}}}}
'''
    return code+'\n'+wrapper+checker('csharp')+ending,f'static object ExecuteRandom{suffix}(JsonElement row)=>{audit}.Run(row);\n'

def java_parts(code,entry):
    subset=entry['ref']=='17.3';suffix=entry['ref'].replace('.','_');audit='RandomAudit'+suffix;root='Solution_'+suffix
    call='int[] result=subject.RandomSubset(input,Count);check(Arrays.equals(input,Original),"Preserve input values and order");' if subset else 'subject.Shuffle(input);int[] result=input;'
    wrapper=f'''class {audit} {{
static final String Mode="shuffle",Method="Shuffle";static boolean Capture,Sampling,Track;static int DrawLimit,Count;static int[] Original,First;static int[][] Positions;
static class ContractError extends RuntimeException {{ContractError(String message){{super(message);}}}}
static class NeedChoice extends RuntimeException {{final int lower,upper;NeedChoice(int lower,int upper){{this.lower=lower;this.upper=upper;}}}}
static void check(boolean ok,String message){{if(!ok)throw new ContractError(message);}}
static class Subject {{private final {root} subject=new {root}();public void Shuffle(int[] array){{int[] input=Original.clone();{call}
check(result!=null&&result.length==Count,"Return the required number of integers");if(Capture)First=result.clone();var pools=new HashMap<Integer,ArrayList<Integer>>();for(int i=0;i<Original.length;++i)pools.computeIfAbsent(Original[i],unused->new ArrayList<>()).add(i);var labels=new ArrayList<Integer>();for(int value:result){{var pool=pools.get(value);check(pool!=null&&!pool.isEmpty(),"Respect original occurrence multiplicities");int slot=pool.size()>1?RandomSource.GetRandom(0,pool.size()-1):0;labels.add(pool.get(slot));pool.set(slot,pool.get(pool.size()-1));pool.remove(pool.size()-1);}}
if({str(subset).lower()}){{var selected=new HashSet<Integer>(labels);var remaining=new ArrayList<Integer>();for(int i=0;i<Original.length;++i)if(!selected.contains(i))remaining.add(i);for(var group:List.of(labels,remaining))for(int i=group.size()-1;i>0;--i)Collections.swap(group,i,RandomSource.GetRandom(0,i));labels.addAll(remaining);}}for(int i=0;i<array.length;++i)array[i]=labels.get(i);if(Sampling&&Track)for(int i=0;i<array.length;++i)Positions[i][array[i]]++;}}}}
static Object fresh(){{return new Subject();}}static Object call(Object instance,String method,Object... args){{((Subject)instance).Shuffle((int[])args[0]);return null;}}
static Object load(JsonValue value,String kind){{var a=value.asArray();int[] result=new int[a.size()];for(int i=0;i<result.length;++i)result[i]=a.get(i).asInt();return result;}}
'''
    count='row.get("arguments").asArray().get(1).asInt()' if subset else 'Original.length'
    ending=f'''static JsonValue run(JsonObject row)throws Exception{{var values=row.get("arguments").asArray().get(0).asArray();Original=(int[])load(values,"ai");Count={count};First=new int[0];Capture=false;Sampling=false;Track=Original.length>5&&Original.length<=64;DrawLimit=64*Original.length+128;Positions=Track?new int[Original.length][Original.length]:new int[0][];var labels=new JsonArray();for(int i=0;i<Original.length;++i)labels.add(i);randomCheck(new JsonArray().add(labels));if(Track){{double expected=4096.0/Original.length;for(int[] frequencies:Positions){{double statistic=0;for(int value:frequencies)statistic+=(value-expected)*(value-expected)/expected;check(statistic<4*(Original.length-1)+80,"Biased position marginals");}}}}var actual=new JsonArray();for(int value:First)actual.add(value);return new JsonObject().add("actual",actual).add("mutationOk",true).add("uniformOk",true);}}}}
'''
    return code+'\n'+wrapper+checker('java')+ending,f'static JsonValue executeRandom{suffix}(JsonObject row){{try{{return {audit}.run(row);}}catch(RuntimeException error){{throw error;}}catch(Exception error){{throw new RuntimeException(error);}}}}\n'

def cpp_parts(code,entry):
    subset=entry['ref']=='17.3';suffix=entry['ref'].replace('.','_');audit='RandomAudit'+suffix;root='Solution_'+suffix
    call='auto result=subject.RandomSubset(input,Count);check(input==Original,"Preserve input values and order");' if subset else 'subject.Shuffle(input);auto result=input;'
    wrapper=f'''#include <cmath>
#include <functional>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <cstdint>
namespace {audit} {{
static bool Capture=false,Sampling=false,Track=false;static int DrawLimit=128,Count=0;static std::vector<int> Original,First;static std::vector<std::vector<int>> Positions;
struct ContractError:std::runtime_error {{using std::runtime_error::runtime_error;}};
struct NeedChoice {{int lower,upper;}};
void check(bool ok,const std::string& message){{if(!ok)throw ContractError(message);}}
struct Subject {{{root} subject;void Shuffle(std::vector<int>& array){{auto input=Original;{call}
check(result.size()==static_cast<size_t>(Count),"Return the required number of integers");if(Capture)First=result;std::unordered_map<int,std::vector<int>> pools;for(size_t i=0;i<Original.size();++i)pools[Original[i]].push_back(static_cast<int>(i));std::vector<int> labels;for(int value:result){{auto found=pools.find(value);check(found!=pools.end()&&!found->second.empty(),"Respect original occurrence multiplicities");auto& pool=found->second;int slot=pool.size()>1?RandomSource::GetRandom(0,static_cast<int>(pool.size())-1):0;labels.push_back(pool[slot]);pool[slot]=pool.back();pool.pop_back();}}
if({str(subset).lower()}){{std::unordered_set<int> selected(labels.begin(),labels.end());std::vector<int> remaining;for(size_t i=0;i<Original.size();++i)if(selected.find(static_cast<int>(i))==selected.end())remaining.push_back(static_cast<int>(i));auto shuffle=[](std::vector<int>& group){{for(int i=static_cast<int>(group.size())-1;i>0;--i)std::swap(group[i],group[RandomSource::GetRandom(0,i)]);}};shuffle(labels);shuffle(remaining);labels.insert(labels.end(),remaining.begin(),remaining.end());}}array=std::move(labels);if(Sampling&&Track)for(size_t i=0;i<array.size();++i)++Positions[i][array[i]];}}}};
json dump(const std::vector<int>& array){{return json(array);}}
'''
    count='row["arguments"][1].get<int>()' if subset else 'static_cast<int>(Original.size())'
    ending=f'''json run(const json& row){{Original=row["arguments"][0].get<std::vector<int>>();Count={count};First.clear();Capture=false;Sampling=false;Track=Original.size()>5&&Original.size()<=64;DrawLimit=64*static_cast<int>(Original.size())+128;Positions=Track?std::vector<std::vector<int>>(Original.size(),std::vector<int>(Original.size())):std::vector<std::vector<int>>{{}};std::vector<int> labels(Original.size());for(size_t i=0;i<labels.size();++i)labels[i]=static_cast<int>(i);randomCheck<Subject>(json::array({{labels}}),true,5,7,[](Subject& subject,std::vector<int>& array){{subject.Shuffle(array);return json(nullptr);}});if(Track){{double expected=4096.0/Original.size();for(const auto& frequencies:Positions){{double statistic=0;for(int value:frequencies)statistic+=(value-expected)*(value-expected)/expected;check(statistic<4*(Original.size()-1)+80,"Biased position marginals");}}}}return json{{{{"actual",First}},{{"mutationOk",true}},{{"uniformOk",true}}}};}}}}
json executeRandom{suffix}(const json& row){{return {audit}::run(row);}}
'''
    return code+'\n'+wrapper+checker('cpp')+ending,''

def add_serial(value,language):
    if language=='python':
        code='''    serial={'last':None,'pairs':[[0]*len(original) for _ in original] if track else []}
    def record_serial(array):
        if not track:return
        if serial['last'] is not None:serial['pairs'][serial['last']][array[0]]+=1
        serial['last']=array[0]
    def check_serial():
        if not track:return
        expected=4095/(len(original)**2)
        statistic=sum((value-expected)**2/expected for row in serial['pairs'] for value in row)
        check(statistic<4*(len(original)**2-1)+80,'Correlated successive positions')
'''
        marker='    draw_limit='
        index=value.index(marker);value=value[:index]+code+value[index:]
        return value.replace("    return dict(actual=context['first'],mutationOk=True,uniformOk=True)","    check_serial()\n    return dict(actual=context['first'],mutationOk=True,uniformOk=True)")
    if language=='javascript':
        code='''const serial={last:-1,pairs:track?Array.from({length:original.length},()=>Array(original.length).fill(0)):[]};
function recordSerial(array){if(!track)return;if(serial.last>=0)++serial.pairs[serial.last][array[0]];serial.last=array[0];}
function checkSerial(){if(!track)return;const expected=4095/(original.length*original.length),statistic=serial.pairs.flat().reduce((sum,value)=>sum+(value-expected)**2/expected,0);check(statistic<4*(original.length*original.length-1)+80,'Correlated successive positions');}
'''
        marker="const Mode='shuffle'";index=value.index(marker);value=value[:index]+code+value[index:]
        return value.replace('return {actual:context.first,mutationOk:true,uniformOk:true};','checkSerial();return {actual:context.first,mutationOk:true,uniformOk:true};')
    if language=='csharp':
        code='''static int SerialLast=-1;static int[,] SerialPairs=new int[0,0];
static void ResetSerial(){SerialLast=-1;SerialPairs=Track?new int[Original.Length,Original.Length]:new int[0,0];}
static void RecordSerial(int[] array){if(!Track)return;if(SerialLast>=0)SerialPairs[SerialLast,array[0]]++;SerialLast=array[0];}
static void CheckSerial(){if(!Track)return;double expected=4095.0/(Original.Length*Original.Length),statistic=0;foreach(int value in SerialPairs)statistic+=(value-expected)*(value-expected)/expected;Check(statistic<4*(Original.Length*Original.Length-1)+80,"Correlated successive positions");}
'''
        marker='    static object RandomCheck';index=value.index(marker);value=value[:index]+code+value[index:]
        value=value.replace('RandomCheck(JsonSerializer.SerializeToElement','ResetSerial();RandomCheck(JsonSerializer.SerializeToElement')
        return value.replace('return new {actual=First,mutationOk=true,uniformOk=true};','CheckSerial();return new {actual=First,mutationOk=true,uniformOk=true};')
    if language=='java':
        code='''static int SerialLast=-1;static int[][] SerialPairs;
static void resetSerial(){SerialLast=-1;SerialPairs=Track?new int[Original.length][Original.length]:new int[0][];}
static void recordSerial(int[] array){if(!Track)return;if(SerialLast>=0)SerialPairs[SerialLast][array[0]]++;SerialLast=array[0];}
static void checkSerial(){if(!Track)return;double expected=4095.0/(Original.length*Original.length),statistic=0;for(int[] row:SerialPairs)for(int value:row)statistic+=(value-expected)*(value-expected)/expected;check(statistic<4*(Original.length*Original.length-1)+80,"Correlated successive positions");}
'''
        marker='    static boolean sameMultiset';index=value.index(marker);value=value[:index]+code+value[index:]
        value=value.replace('randomCheck(new JsonArray().add(labels));','resetSerial();randomCheck(new JsonArray().add(labels));')
        return value.replace('var actual=new JsonArray();','checkSerial();var actual=new JsonArray();')
    code='''static int SerialLast=-1;static std::vector<std::vector<int>> SerialPairs;
void resetSerial(){SerialLast=-1;SerialPairs=Track?std::vector<std::vector<int>>(Original.size(),std::vector<int>(Original.size())):std::vector<std::vector<int>>{};}
void recordSerial(const std::vector<int>& array){if(!Track)return;if(SerialLast>=0)++SerialPairs[SerialLast][array[0]];SerialLast=array[0];}
void checkSerial(){if(!Track)return;double expected=4095.0/(Original.size()*Original.size()),statistic=0;for(const auto& row:SerialPairs)for(int value:row)statistic+=(value-expected)*(value-expected)/expected;check(statistic<4*(Original.size()*Original.size()-1)+80,"Correlated successive positions");}
'''
    marker='template <typename Subject, typename Invoke>';index=value.index(marker);value=value[:index]+code+value[index:]
    value=value.replace('randomCheck<Subject>(json::array','resetSerial();randomCheck<Subject>(json::array')
    return value.replace('return json{{"actual",First},{"mutationOk",true},{"uniformOk",true}};','checkSerial();return json{{"actual",First},{"mutationOk",true},{"uniformOk",true}};')

def attach(value,language,entry,starters):
    plain=base_header(entry['ref'],language)
    if RANDOM[language] not in value:value=value.replace(plain,plain+RANDOM[language],1) if plain else RANDOM[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    suffix=entry['ref'].replace('.','_')
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_'+suffix,1)
    builder={'python':python_parts,'javascript':javascript_parts,'csharp':csharp_parts,'java':java_parts,'cpp':cpp_parts}[language]
    outside,inside=builder(code,entry)
    outside=add_serial(outside,language)
    ref=entry['ref']
    if language=='python':return value.replace('def execute(row):',outside+f"\ndef execute(row):\n    if row['ref']=='{ref}': return executeRandom{suffix}(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+f'\nfunction execute(row){{if(row.ref==="{ref}")return executeRandom{suffix}(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){',f'static object Execute(JsonElement row){{if(row.GetProperty("ref").GetString()=="{ref}")return ExecuteRandom{suffix}(row);',1)
    if language=='java':return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){',f'static JsonValue execute(JsonObject row){{if(row.get("ref").asString().equals("{ref}"))return executeRandom{suffix}(row);',1)
    return value.replace('json execute(const json& row){',outside+f'\njson execute(const json& row){{if(row["ref"]=="{ref}")return executeRandom{suffix}(row);',1)
