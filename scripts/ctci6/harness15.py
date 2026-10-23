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
