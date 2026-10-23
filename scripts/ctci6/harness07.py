"""Generic state adapters observe real methods/iterators, not reference answers."""
import importlib
import json
from core import ROOT
from models08 import header as base_header
from models07 import header
from harness08_typed import source as typed_source

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged07',exclude_refs=('7.9',),allow_empty=True)
    base=base_header('7.9',language);provided=header('7.9',language)
    value=value.replace(base,provided,1) if base else provided+value
    entry=next(e for e in json.loads((ROOT/'ctci6/staged07/catalog.json').read_text()) if e['ref']=='7.9')
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    helper=importlib.import_module('harness_circular07_'+language).CORE
    if language=='python':return value.replace('def execute(row):',code+helper+"\ndef execute(row):\n    if row['ref']=='7.9':return executeCircular7(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',code+helper+'\nfunction execute(row){if(row.ref==="7.9")return executeCircular7(row);',1)
    if language=='csharp':return value.replace('class Harness {',code+'\nclass Harness {\n'+helper,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="7.9")return ExecuteCircular7(row);',1)
    if language=='java':return value.replace('public class Harness {',code+'\npublic class Harness {\n'+helper,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("7.9"))return executeCircular7(row);',1)
    return value.replace('json execute(const json& row){',code+'\n'+helper+'\njson execute(const json& row){if(row["ref"]=="7.9")return executeCircular7(row);',1)

_circular_source=source
def source(language,starters=False,only_ref=None):
    entries=json.loads((ROOT/'ctci6/staged07/catalog.json').read_text())
    selected=[e for e in entries if only_ref is None or e['ref']==only_ref]
    if any(e['ref']=='7.9' for e in selected):value=_circular_source(language,starters,only_ref='7.9')
    else:
        value=typed_source(language,starters,only_ref,staging_name='staged07',exclude_refs=('7.9','7.12'),allow_empty=True)
        base=base_header('7.12',language);provided=header('7.12',language)
        value=value.replace(base,provided,1) if base else provided+value
    for entry in selected:
        if entry['ref']!='7.12':continue
        code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
        helper=importlib.import_module('harness_hash07_'+language).CORE
        if language=='python':value=value.replace('def execute(row):',code+helper+"\ndef execute(row):\n    if row['ref']=='7.12':return executeHash7(row)\n",1)
        elif language=='javascript':value=value.replace('function execute(row){',code+helper+'\nfunction execute(row){if(row.ref==="7.12")return executeHash7(row);',1)
        elif language=='csharp':value=value.replace('class Harness {',code+'\nclass Harness {\n'+helper,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="7.12")return ExecuteHash7(row);',1)
        elif language=='java':value=value.replace('public class Harness {',code+'\npublic class Harness {\n'+helper,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("7.12"))return executeHash7(row);',1)
        else:value=value.replace('json execute(const json& row){',code+'\n'+helper+'\njson execute(const json& row){if(row["ref"]=="7.12")return executeHash7(row);',1)
    return value
