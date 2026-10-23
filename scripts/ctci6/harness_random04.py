"""State/identity observers plus the established permutation checker for one node."""
import importlib
from models08 import header as base_header
from models_random04 import NODE,RANDOM
from harness_random17 import python_parts,javascript_parts,csharp_parts,java_parts,cpp_parts,add_serial

BUILDERS={'python':python_parts,'javascript':javascript_parts,'csharp':csharp_parts,'java':java_parts,'cpp':cpp_parts}

def wide_source(value,language):
    domains={
      'python':('0 <= lower <= upper < len(original)','0 <= lower <= upper <= 2147483647'),
      'javascript':('lower >= 0 && upper < original.length','lower >= 0 && upper <= 2147483647'),
      'csharp':('lower >= 0 && upper < original.Length','lower >= 0 && upper <= 2147483647'),
      'java':('lower>=0&&upper<length','lower>=0&&upper<=2147483647'),
      'cpp':('lower >= 0 && upper < static_cast<int>(original.size())','lower >= 0 && upper <= 2147483647')}
    old,new=domains[language]
    if old not in value:raise ValueError('Unknown generic source bounds '+language)
    value=value.replace(old,new)
    if language=='python':value=value.replace('if len(prefix) >= limit:','if len(prefix) >= limit or next_choice.upper-next_choice.lower+1>32:')
    elif language=='javascript':
        value=value.replace('if (item.prefix.length >= limit)', 'if (item.prefix.length >= limit || error.Upper-error.Lower+1>32)')
        value=value.replace('Math.floor(seed * (upper - lower + 1) / 4294967296)','Number((BigInt(seed)*BigInt(upper-lower+1))>>32n)')
    elif language=='csharp':
        value=value.replace('if (item.prefix.Length >= limit)', 'if (item.prefix.Length >= limit || (long)next.Upper-next.Lower+1>32)')
        value=value.replace('for (int choice = next.Lower; choice <= next.Upper; choice++) pending.Push((item.prefix.Append(choice)', 'for (long choice = next.Lower; choice <= next.Upper; choice++) pending.Push((item.prefix.Append((int)choice)')
        value=value.replace('(uint)(upper - lower + 1)','(uint)((long)upper-lower+1)')
    elif language=='java':
        value=value.replace('if(decision.prefix().length>=limit)', 'if(decision.prefix().length>=limit||(long)next.upper-next.lower+1>32)')
        value=value.replace('for(int choice=next.lower;choice<=next.upper;choice++) {','for(long rawChoice=next.lower;rawChoice<=next.upper;rawChoice++) {int choice=(int)rawChoice;')
    else:
        value=value.replace('if (branch.prefix.size() >= static_cast<size_t>(limit))','if (branch.prefix.size() >= static_cast<size_t>(limit) || static_cast<long long>(next.upper)-next.lower+1>32)')
        value=value.replace('for (int choice = next.lower; choice <= next.upper; ++choice) {','for (long long rawChoice = next.lower; rawChoice <= next.upper; ++rawChoice) {int choice=static_cast<int>(rawChoice);')
        value=value.replace('static_cast<std::uint32_t>(upper - lower + 1)','static_cast<std::uint32_t>(static_cast<std::uint64_t>(upper)-lower+1)')
    return value

def uniform_parts(language,code):
    outside,inside=BUILDERS[language](code,{'ref':'4.11'})
    if language=='python':
        old='returned = Shuffle(input_values)';assert outside.count(old)==1
        outside=outside.replace(old,"returned = context['subject'].Shuffle(input_values)")
        old='    class Subject:\n        def Shuffle(self,array):invoke(array)';assert outside.count(old)==1
        outside=outside.replace(old,"    class Subject:\n        def __init__(self):self.shim=NodeShuffle4()\n        def Shuffle(self,array):\n            context['subject']=self.shim\n            invoke(array)")
    if language=='javascript':
        old='const returned=Shuffle(input);';assert outside.count(old)==1
        outside=outside.replace(old,'const returned=context.subject.Shuffle(input);')
        old='class Subject{Shuffle(array){invoke(array);}}';assert outside.count(old)==1
        outside=outside.replace(old,'class Subject{constructor(){this.shim=new NodeShuffle4();}Shuffle(array){context.subject=this.shim;invoke(array);}}')
    return wide_source(add_serial(outside,language),language),inside

def attach(value,language,entry,starters):
    plain=base_header('4.11',language);provided=NODE[language]+RANDOM[language]
    if provided not in value:value=value.replace(plain,plain+provided,1) if plain else provided+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    module=importlib.import_module('harness_random04_'+language)
    outside,inside=module.parts(code)
    if language=='python':return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='4.11': return executeRandomBst4(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="4.11")return executeRandomBst4(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="4.11")return ExecuteRandomBst4(row);',1)
    if language=='java':return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("4.11"))return executeRandomBst4(row);',1)
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="4.11")return executeRandomBst4(row);',1)
