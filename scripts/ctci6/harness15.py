"""Small native-worker adapter for the three-call ordering exercise."""
import importlib,json
from core import ROOT
from models15 import header

def source(language,starters=False,only_ref=None):
 entry=next(e for e in json.loads((ROOT/'ctci6/staged15/catalog.json').read_text()) if e['ref']=='15.5')
 if only_ref not in (None,'15.5'):raise ValueError(only_ref)
 code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
 if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_15_5',1)
 prefix=header('15.5',language);module=importlib.import_module('harness_order15_'+language);value=prefix+code+'\n'+module.CORE
 if language=='python':return 'import json\n'+value+'''\nresults=[]
for row in json.load(open('cases.json')):
    try:results.append(execute(row))
    except BaseException as error:results.append(dict(error=str(error)))
json.dump(results,open('results.json','w'))
'''
 if language=='javascript':return "const fs=require('node:fs');\n"+value+'''\nif(!isMainThread&&workerData&&workerData.order15){orderWorker15();}else{
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{try{return execute(row);}catch(error){return {error:String(error)};}});
fs.writeFileSync('results.json',JSON.stringify(results));
}
'''
 if language=='csharp':return 'using System.IO;\nusing System.Text.Json;\n'+value+'\nclass Harness {\n'+module.INSIDE+'''\nstatic void Main(){using var doc=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in doc.RootElement.EnumerateArray()){try{results.Add(Execute(row));}catch(Exception error){results.Add(new {error=error.ToString()});}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}
}
'''
 if language=='java':return 'import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n'+value+'\npublic class Harness {\n'+module.INSIDE+'''\npublic static void main(String[] ignored)throws Exception{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){try{results.add(execute(row.asObject()));}catch(Throwable error){results.add(new JsonObject().add("error",error.toString()));}}Files.writeString(Path.of("results.json"),results.toString());}
}
'''
 return '#include <fstream>\n#include <memory>\n#include <mutex>\n#include <thread>\n#include <condition_variable>\n#include <chrono>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n'+value+'''\nint main(){std::ifstream input("cases.json");json rows;input>>rows;json results=json::array();for(const auto& row:rows){try{results.push_back(execute(row));}catch(const std::exception& error){results.push_back(json{{"error",error.what()}});}}std::ofstream("results.json")<<results;}
'''

_order_source=source
def source(language,starters=False,only_ref=None):
    # Preserve the exact existing per-reference adapter and its valid receipts.
    if only_ref=='15.5':return _order_source(language,starters,only_ref)
    from models08 import header as base_header
    from models15 import reference
    entries=json.loads((ROOT/'ctci6/staged15/catalog.json').read_text())
    selected=[e for e in entries if only_ref is None or e['ref']==only_ref]
    if not selected:raise ValueError(only_ref)
    declarations=[];cores=[];insides=[];branches=[];worker_branches=[]
    for entry in selected:
        ref=entry['ref'];tag='Order15' if ref=='15.5' else 'Fizz15';helper=importlib.import_module('harness_order15_'+language if ref=='15.5' else 'harness_fizz15_'+language)
        code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
        if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_'+ref.replace('.','_'),1)
        declarations.append(reference(ref,language)+code)
        core=helper.CORE
        if language=='python':core=core.replace('def execute(row):','def execute'+tag+'(row):',1);branches.append("    if row['ref']=="+repr(ref)+':return execute'+tag+'(row)')
        elif language=='javascript':
            core=core.replace("const {Worker,isMainThread,workerData,threadId}=require('node:worker_threads');",'').replace('function execute(row){','function execute'+tag+'(row){',1)
            branches.append('if(row.ref==='+json.dumps(ref)+')return execute'+tag+'(row);')
            worker_branches.append("if(!isMainThread&&workerData&&workerData."+('order15' if ref=='15.5' else 'fizz15')+"){\n"+('orderWorker15' if ref=='15.5' else 'fizzWorker15')+'();}')
        elif language=='csharp':insides.append(helper.INSIDE.replace('static object Execute(JsonElement row)','static object Execute'+tag+'(JsonElement row)',1));branches.append('if(row.GetProperty("ref").GetString()=='+json.dumps(ref)+')return Execute'+tag+'(row);')
        elif language=='java':insides.append(helper.INSIDE.replace('static JsonValue execute(JsonObject row)','static JsonValue execute'+tag+'(JsonObject row)',1));branches.append('if(row.get("ref").asString().equals('+json.dumps(ref)+'))return execute'+tag+'(row);')
        else:core=core.replace('json execute(const json& row)','json execute'+tag+'(const json& row)',1);branches.append('if(row["ref"]=='+json.dumps(ref)+')return execute'+tag+'(row);')
        cores.append(core)
    value=base_header('15.5',language)+'\n'.join(declarations+cores)
    if language=='python':return 'import json\n'+value+'\ndef execute(row):\n'+'\n'.join(branches)+'''\n    raise ValueError('Unknown worker reference')
results=[]
for row in json.load(open('cases.json')):
    try:results.append(execute(row))
    except BaseException as error:results.append(dict(error=str(error)))
json.dump(results,open('results.json','w'))
'''
    if language=='javascript':return "const fs=require('node:fs');\nconst {Worker,isMainThread,workerData,threadId}=require('node:worker_threads');\n"+value+'\nfunction execute(row){'+''.join(branches)+"throw new Error('Unknown worker reference');}\n"+'else '.join(worker_branches)+'''else{
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{try{return execute(row);}catch(error){return {error:String(error)};}});
fs.writeFileSync('results.json',JSON.stringify(results));
}
'''
    if language=='csharp':return 'using System.IO;\nusing System.Text.Json;\n'+value+'\nclass Harness {\n'+''.join(insides)+'\nstatic object Execute(JsonElement row){'+''.join(branches)+'throw new Exception("Unknown worker reference");}\n'+'''static void Main(){using var doc=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in doc.RootElement.EnumerateArray()){try{results.Add(Execute(row));}catch(Exception error){results.Add(new {error=error.ToString()});}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}
}
'''
    if language=='java':return 'import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n'+value+'\npublic class Harness {\n'+''.join(insides)+'\nstatic JsonValue execute(JsonObject row)throws Exception{'+''.join(branches)+'throw new IllegalArgumentException("Unknown worker reference");}\n'+'''public static void main(String[] ignored)throws Exception{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){try{results.add(execute(row.asObject()));}catch(Throwable error){results.add(new JsonObject().add("error",error.toString()));}}Files.writeString(Path.of("results.json"),results.toString());}
}
'''
    return '#include <fstream>\n#include <memory>\n#include <mutex>\n#include <thread>\n#include <condition_variable>\n#include <chrono>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n'+value+'\njson execute(const json& row){'+''.join(branches)+'throw std::runtime_error("Unknown worker reference");}\n'+'''int main(){std::ifstream input("cases.json");json rows;input>>rows;json results=json::array();for(const auto& row:rows){try{results.push_back(execute(row));}catch(const std::exception& error){results.push_back(json{{"error",error.what()}});}}std::ofstream("results.json")<<results;}
'''
