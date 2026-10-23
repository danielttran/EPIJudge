"""Reuse the established bank random checker through a zero-based primitive bridge.

Only bank-owned checker functions are extracted. The original Interview Cake
runtimes are unchanged. CtCI permits alternative rejection schemes, so its
adapter removes the IC-specific two-draw rule and rejected-mass cutoff while
retaining probability intervals, seeded marginal/pair/triple checks and limits.
"""
import re
from textwrap import indent
from core import ROOT
from models08 import header as base_header
from models_rand16 import RAND5

RUNTIME=ROOT/'interviewcake/runtime'

def between(file,start,end):
    value=(RUNTIME/file).read_text();return value[value.index(start):value.index(end,value.index(start))]

def native_loop(value):
    expression=r'(for\s*\(int trial\s*=\s*0;\s*trial\s*<\s*samples;\s*(?:\+\+trial|trial\+\+)\s*\)\s*\{)'
    value,count=re.subn(expression,r'\1Capture=trial==0;',value)
    if count!=1:raise ValueError('Unknown randomized sample loop')
    return value

def relaxed(value,language):
    if language=='python':
        old='''        check(
            unresolved < 0.02,
            "Rejection probability exceeds bounded judge exploration.",
        )
'''
        if value.count(old)!=1:raise ValueError('Unknown Python rejection-mass gate')
        value=value.replace(old,'')
        value=value.replace('''                if Mode == "rand7":
                    check(draws % 2 == 0, "Rand7 must use two Rand5 draws per attempt.")
''','')
        value=value.replace('''            if Mode == "rand7":
                check(draws % 2 == 0, "Use two Rand5 draws per completed attempt.")
''','')
        # Check actual spelling rather than silently retaining a restrictive rule.
        value=re.sub(r'(?m)^\s*if Mode == "rand7":\n\s*check\(draws % 2 == 0, [^\n]+\)\n','',value)
        value=value.replace('    for trial in range(samples):','    for trial in range(samples):\n        context["capture"] = trial == 0',1)
    else:
        check='Check' if language=='csharp' else 'check'
        value,count=re.subn(check+r'\(unresolved\s*<\s*0\.02,[^;]+;','',value)
        if count!=1:raise ValueError('Unknown native rejection-mass gate '+language)
        if language=='csharp':value=re.sub(r'&&\s*\(Mode\s*!=\s*"rand7"\s*\|\|\s*draws\s*%\s*2\s*==\s*0\)', '', value)
        if language=='cpp':value=value.replace('(outcomes != 7 || draws % 2 == 0) &&','')
        if language=='javascript':
            value='\n'.join(line for line in value.split('\n') if 'draws % 2' not in line)
            value,count=re.subn(r'(for\s*\(let trial\s*=\s*0;\s*trial\s*<\s*samples;\s*(?:\+\+trial|trial\+\+)\s*\)\s*\{)',r'\1context.capture=trial===0;',value)
            if count!=1:raise ValueError('Unknown JS sample loop')
        else:
            if language=='java':value=re.sub(r'if\(Mode.equals\("rand7"\)\)check\(draws%2==0,[^;]+;','',value)
            value=native_loop(value)
    if 'draws % 2' in value or 'draws%2' in value:raise ValueError('A draw-pair restriction remains '+language)
    return value

def parts(language,code):
    if language=='python':
        checker=relaxed(between('harness.py','def random_check(raw):','\ndef execute(raw):'),'python')
        prelude='''def executeRand16(row):
    import math
    from types import SimpleNamespace
    context={'capture':False,'first':0}
    Mode='rand7'
    Method='Roll'
    class ContractError(Exception):pass
    class NeedChoice(Exception):
        def __init__(self,lower,upper):self.lower,self.upper=lower,upper
    def check(ok,message='Random contract failed'):
        if not ok:raise ContractError(message)
    class RandomSource:
        Draw=staticmethod(lambda lower,upper:0)
    class JudgeRand5(Rand5Source):
        def Next(self):return RandomSource.Draw(1,5)-1
    class Subject:
        def Roll(self):
            value=UniformSeven(JudgeRand5())
            check(type(value) is int and 0<=value<=6,'Return an integer in 0..6')
            if context['capture']:context['first']=value
            return value+1
    user=SimpleNamespace(RandomSource=RandomSource)
    def fresh():return Subject()
    def call(instance,method,*args):return getattr(instance,method)(*args)
    def typed_result(value,kind):check(value is None,'Return None for void')
'''
        return code+'\n'+prelude+indent(checker,'    ')+'''    random_check([[value+1 for value in row['arguments'][0]]])
    return dict(actual=context['first'],mutationOk=True,uniformOk=True)
''',''
    if language=='javascript':
        checker=relaxed(between('harness.js','function randomCheck(raw) {','\nfunction execute(raw) {'),'javascript')
        prelude='''function executeRand16(row){
const Mode='rand7',context={capture:false,first:0};
class ContractError extends Error{};
class NeedChoice extends Error{constructor(lower,upper){super('An injected choice is required');this.Lower=lower;this.Upper=upper;}}
function check(ok,message){if(!ok)throw new ContractError(message);}
const json=JSON.stringify;
class RandomSource{static Draw=(lower,upper)=>0;}
class JudgeRand5 extends Rand5Source{Next(){return RandomSource.Draw(1,5)-1;}}
class Subject{Roll(){const value=UniformSeven(new JudgeRand5());check(Number.isInteger(value)&&value>=0&&value<=6,'Return an integer in 0..6');if(context.capture)context.first=value;return value+1;}}
function fresh(){return new Subject();}
function call(instance,method,...args){return instance.Roll(...args);}
const Method='Roll';
'''
        return code+'\n'+prelude+checker+'''randomCheck([row.arguments[0].map(value=>value+1)]);return {actual:context.first,mutationOk:true,uniformOk:true};}
''',''
    if language=='csharp':
        checker=relaxed(between('Harness.cs','    static object RandomCheck(JsonElement raw)','    static object? Execute(JsonElement raw)'),'csharp')
        wrapper='''static class RandomAudit16 {
static readonly string Mode="rand7",Method="Roll";
static bool Capture;static int First;
sealed class ContractError(string message):Exception(message);
sealed class NeedChoice(int lower,int upper):Exception {public int Lower=lower,Upper=upper;}
static class RandomSource {public static Func<int,int,int> Draw=(lower,upper)=>0;}
sealed class JudgeRand5:Rand5Source {public override int Next()=>RandomSource.Draw(1,5)-1;}
sealed class Subject {private readonly Solution_16_23 subject=new();public int Roll(){int value=subject.UniformSeven(new JudgeRand5());Check(value>=0&&value<=6,"Return an integer in 0..6");if(Capture)First=value;return value+1;}}
static object Fresh()=>new Subject();
static object? Call(object instance,string method,params object?[] args)=>((Subject)instance).Roll();
static void Check(bool ok,string message){if(!ok)throw new ContractError(message);}
'''
        return code+'\n'+wrapper+checker+'''public static object Run(JsonElement row){Capture=false;First=0;var values=row.GetProperty("arguments")[0].EnumerateArray().Select(value=>value.GetInt32()+1).ToArray();RandomCheck(JsonSerializer.SerializeToElement(new[]{values}));return new {actual=First,mutationOk=true,uniformOk=true};}}
''','static object ExecuteRand16(JsonElement row)=>RandomAudit16.Run(row);\n'
    if language=='java':
        checker=relaxed(between('Harness.java','    static boolean sameMultiset(int[] first,int[] second)','    static Object execute(JsonArray raw)'),'java')
        wrapper='''class RandomAudit16 {
static final String Mode="rand7",Method="Roll";static boolean Capture;static int First;
static class ContractError extends RuntimeException {ContractError(String message){super(message);}}
static class NeedChoice extends RuntimeException {final int lower,upper;NeedChoice(int lower,int upper){this.lower=lower;this.upper=upper;}}
static class RandomSource {static java.util.function.IntBinaryOperator Draw=(lower,upper)->0;}
static class JudgeRand5 extends Rand5Source {public int Next(){return RandomSource.Draw.applyAsInt(1,5)-1;}}
static class Subject {private final Solution_16_23 subject=new Solution_16_23();public int Roll(){int value=subject.UniformSeven(new JudgeRand5());check(value>=0&&value<=6,"Return an integer in 0..6");if(Capture)First=value;return value+1;}}
static Object fresh(){return new Subject();}
static Object call(Object instance,String method,Object... args){return ((Subject)instance).Roll();}
static Object load(JsonValue value,String kind){var a=value.asArray();int[] result=new int[a.size()];for(int i=0;i<result.length;++i)result[i]=a.get(i).asInt();return result;}
static void check(boolean ok,String message){if(!ok)throw new ContractError(message);}
'''
        return code+'\n'+wrapper+checker+'''static JsonValue run(JsonObject row)throws Exception{Capture=false;First=0;var values=new JsonArray();for(var value:row.get("arguments").asArray().get(0).asArray())values.add(value.asInt()+1);randomCheck(new JsonArray().add(values));return new JsonObject().add("actual",First).add("mutationOk",true).add("uniformOk",true);}}
''','static JsonValue executeRand16(JsonObject row){try{return RandomAudit16.run(row);}catch(RuntimeException error){throw error;}catch(Exception error){throw new RuntimeException(error);}}\n'
    checker=relaxed(between('harness.cpp','template <typename Subject, typename Invoke>\njson randomCheck','\n// CONFIGURATION'),'cpp')
    wrapper='''#include <cmath>
#include <functional>
#include <map>
#include <cstdint>
namespace RandomAudit16 {
static bool Capture=false;static int First=0;
struct ContractError:std::runtime_error {using std::runtime_error::runtime_error;};
struct NeedChoice {int lower,upper;};
void check(bool ok,const std::string& message){if(!ok)throw ContractError(message);}
struct RandomSource {inline static std::function<int(int,int)> Draw=[](int,int){return 0;};};
struct JudgeRand5:Rand5Source {int Next() override{return RandomSource::Draw(1,5)-1;}};
struct Subject {Solution_16_23 subject;int Roll(){JudgeRand5 source;int value=subject.UniformSeven(source);check(value>=0&&value<=6,"Return an integer in 0..6");if(Capture)First=value;return value+1;}};
json dump(const std::vector<int>& array){return json(array);}
'''
    return code+'\n'+wrapper+checker+'''json run(const json& row){Capture=false;First=0;auto values=row["arguments"][0].get<std::vector<int>>();for(auto& value:values)++value;randomCheck<Subject>(json::array({values}),false,5,7,[](Subject& subject,std::vector<int>&){return json(subject.Roll());});return json{{"actual",First},{"mutationOk",true},{"uniformOk",true}};}}
json executeRand16(const json& row){return RandomAudit16::run(row);}
''',''

def attach(value,language,entry,starters):
    # The moderate C++ header also has unordered-map/set includes; the bank API
    # is inserted after the same common header as every other provided model.
    plain=base_header('16.23',language)
    if RAND5[language] not in value:value=value.replace(plain,plain+RAND5[language],1) if plain else RAND5[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_16_23',1)
    outside,inside=parts(language,code)
    if language=='python':return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='16.23': return executeRand16(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="16.23")return executeRand16(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="16.23")return ExecuteRand16(row);',1)
    if language=='java':return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("16.23"))return executeRand16(row);',1)
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="16.23")return executeRand16(row);',1)
