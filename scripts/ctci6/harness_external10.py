"""Attach only the new external-file record/stream observer."""
import importlib
from models08 import header as base_header
from models_external10 import API

def attach(value,language,entry,starters):
    plain=base_header('10.6',language)
    value=value.replace(plain,plain+API[language],1) if plain else API[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_10_6',1)
    module=importlib.import_module('harness_external10_'+language)
    outside=code+'\n'+module.CORE;inside=getattr(module,'INSIDE','')
    if language=='python':return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='10.6':return executeExternal10(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="10.6")return executeExternal10(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="10.6")return ExecuteExternal10(row);',1)
    if language=='java':
        value='import java.io.*;\nimport java.nio.charset.StandardCharsets;\n'+value
        return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("10.6"))return executeExternal10(row);',1)
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="10.6")return executeExternal10(row);',1)
