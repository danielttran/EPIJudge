"""Typed JSON adapters; observation only, with no expected answers in children."""

import json
from core import ROOT
from models08 import header, TYPES


def source(language, starters=False, only_ref=None, staging_name='staged08'):
    entries = json.loads((ROOT / 'ctci6' / staging_name / 'catalog.json').read_text())
    if only_ref is not None:
        entries = [e for e in entries if e['ref'] == only_ref]
    if not entries:
        raise ValueError('Unknown recursion exercise')
    declarations, branches = [], []
    for entry in entries:
        code = entry['languages'][language]['starterCode' if starters else 'solutionCode']
        cls = 'Solution_' + entry['ref'].replace('.', '_')
        if language not in ('python', 'javascript'):
            code = code.replace('class Solution', 'class ' + cls, 1)
        declarations.append(code)
        if language == 'python':
            branches.append(f"    if ref == {entry['ref']!r}: return {entry['method']}(*args)")
            continue
        if language == 'javascript':
            branches.append(f"if(ref==={json.dumps(entry['ref'])})return {entry['method']}(...args);")
            continue
        decode, names, checks = [], [], []
        for i, (_, kind) in enumerate(entry['params']):
            name = 'p' + str(i)
            names.append(name)
            if language == 'csharp':
                value = f'JsonSerializer.Deserialize<{TYPES[language][kind]}>(args[{i}].GetRawText())!'
                decode.append(f'var {name}={value};')
                if kind in ('ai', 'aai'):
                    decode.append(f'var before{i}=JsonSerializer.Serialize({name});')
                    
                    if entry['mutation'] != 'screen':
                        checks.append(f'JsonSerializer.Serialize({name})==before{i}')
                    if kind == 'aai':
                        decode.append(f'var rows{i}={name}.ToArray();')
                        checks.append(f'{name}.Length==rows{i}.Length && {name}.Select((r,j)=>ReferenceEquals(r,rows{i}[j])).All(v=>v)')
            elif language == 'java':
                value = f'args.get({i}).' + {'i':'asInt()', 's':'asString()', 'b':'asBoolean()', 'ai':'asArray()', 'aai':'asArray()'}[kind]
                if kind == 'ai':
                    decode.append(f'int[] {name}=integers({value});')
                elif kind == 'aai':
                    decode.append(f'int[][] {name}=matrix({value});')
                else:
                    decode.append(f'var {name}={value};')
                if kind in ('ai','aai'):
                    decode.append(f'String before{i}=encode({name}).toString();')
                    
                    if entry['mutation'] != 'screen':
                        checks.append(f'encode({name}).toString().equals(before{i})')
                    if kind == 'aai':
                        decode.append(f'int[][] rows{i}={name}.clone();')
                        checks.append(f'sameRows({name},rows{i})')
            else:
                decode.append(f'auto {name}=args[{i}].get<{TYPES[language][kind]}>();')
                if kind in ('ai', 'aai'):
                    decode.append(f'auto before{i}={name};')
                    
                    if entry['mutation'] != 'screen':
                        checks.append(f'{name}==before{i}')
                    if kind == 'aai':
                        decode.append(f'std::vector<const int*> rows{i};for(const auto& row:{name})rows{i}.push_back(row.data());')
                        checks.append(f'sameRows({name},rows{i})')
        call = ('new ' + cls + '()' if language != 'cpp' else cls + '()') + '.' + entry['method'] + '(' + ','.join(names) + ')'
        if entry['mutation'] == 'screen':
            checks.append('JsonSerializer.Serialize(actual)==JsonSerializer.Serialize(p0)' if language == 'csharp' else 'encode(actual).toString().equals(encode(p0).toString())' if language == 'java' else 'actual==p0')
        check = ' && '.join('(' + v + ')' for v in checks) or 'true'
        emit = f'return new {{actual,mutationOk={check}}};' if language == 'csharp' else f'return new JsonObject().add("actual",encode(actual)).add("mutationOk",{check});' if language == 'java' else 'return json{{"actual",actual},{"mutationOk",' + check + '}};'
        condition = f'reference.equals("{entry["ref"]}")' if language == 'java' else f'reference=="{entry["ref"]}"'
        branches.append(f'if({condition}){{' + ''.join(decode) + f'var actual={call};' .replace('var ', 'auto ' if language == 'cpp' else 'var ', 1) + emit + '}')
    prefix = header('8.4' if only_ref is None else only_ref, language)
    code, dispatch = '\n'.join(declarations), '\n'.join(branches)
    kinds = {entry['ref']: entry['result'] for entry in entries}
    if language == 'python':
        return prefix + code + f'''
import json
KINDS={kinds!r}
def invoke(row):
    ref,args=row['ref'],row['arguments']
{dispatch}
    raise ValueError('Unknown reference')
def execute(row):
    args=row['arguments'];before=json.dumps(args);outer=[v for v in args if type(v) is list];rows=[(v,list(v)) for v in outer if v and type(v[0]) is list]
    actual=invoke(row);kind=KINDS[row['ref']]
    valid=(type(actual) is list and all(type(v) is str for v in actual)) if kind=='strings' else (type(actual) is list and all(type(r) is list and all(type(v) is int for v in r) for r in actual)) if kind in ('sets','arrangements','path','aai') else (type(actual) is list and all(type(v) is int for v in actual)) if kind=='ai' else type(actual) is int and -2147483648<=actual<=2147483647
    return dict(actual=actual,mutationOk=valid and (actual==args[0] if row['ref']=='8.10' else json.dumps(args)==before) and all(any(v is original for v in args) for original in outer) and all(len(v)==len(old) and all(a is b for a,b in zip(v,old)) for v,old in rows))
results=[]
for row in json.load(open('cases.json',encoding='utf-8')):
    try:results.append(execute(row))
    except Exception as error:results.append(dict(error=repr(error)))
json.dump(results,open('results.json','w',encoding='utf-8'))
'''
    if language == 'javascript':
        return prefix + code + f'''
const fs=require('node:fs'),kinds={json.dumps(kinds)};
function invoke(row){{const ref=row.ref,args=row.arguments;{dispatch}throw new Error('Unknown reference');}}
function execute(row){{const args=row.arguments,before=JSON.stringify(args),outer=args.filter(Array.isArray),rows=outer.filter(v=>v.length&&Array.isArray(v[0])).map(v=>[v,v.slice()]);const actual=invoke(row),kind=kinds[row.ref];const valid=kind==='strings'?Array.isArray(actual)&&actual.every(v=>typeof v==='string'):['sets','arrangements','path','aai'].includes(kind)?Array.isArray(actual)&&actual.every(r=>Array.isArray(r)&&r.every(Number.isInteger)):kind==='ai'?Array.isArray(actual)&&actual.every(v=>Number.isInteger(v)&&v>=-2147483648&&v<=2147483647):Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647;return {{actual,mutationOk:valid&&(row.ref==='8.10'?JSON.stringify(actual)===JSON.stringify(args[0]):JSON.stringify(args)===before)&&outer.every(v=>args.includes(v))&&rows.every(([v,old])=>v.length===old.length&&v.every((r,i)=>r===old[i]))}};}}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{{try{{return execute(row);}}catch(error){{return {{error:String(error)}};}}}});
fs.writeFileSync('results.json',JSON.stringify(results));
'''
    if language == 'csharp':
        return 'using System.IO;\nusing System.Text.Json;\n' + prefix + code + f'''
class Harness {{
static object Execute(JsonElement row){{string reference=row.GetProperty("ref").GetString()!;var args=row.GetProperty("arguments");{dispatch}throw new Exception("Unknown reference");}}
static void Main(){{using var document=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in document.RootElement.EnumerateArray()){{try{{results.Add(Execute(row));}}catch(Exception error){{results.Add(new {{error=error.ToString()}});}}}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}}
}}
'''
    if language == 'java':
        return 'import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n' + prefix + code + f'''
public class Harness {{
static int[] integers(JsonArray values){{int[] output=new int[values.size()];for(int i=0;i<output.length;++i)output[i]=values.get(i).asInt();return output;}}
static int[][] matrix(JsonArray values){{int[][] output=new int[values.size()][];for(int i=0;i<output.length;++i)output[i]=integers(values.get(i).asArray());return output;}}
static boolean sameRows(int[][] values,int[][] before){{if(values.length!=before.length)return false;for(int i=0;i<values.length;++i)if(values[i]!=before[i])return false;return true;}}
static JsonValue encode(Object value){{if(value==null)return Json.NULL;if(value instanceof Integer v)return Json.value(v);if(value instanceof String v)return Json.value(v);var result=new JsonArray();if(value instanceof int[] values){{for(int v:values)result.add(v);}}else if(value instanceof int[][] values){{for(int[] v:values)result.add(encode(v));}}else if(value instanceof Iterable<?> values){{for(Object v:values)result.add(encode(v));}}else throw new IllegalArgumentException("Invalid result");return result;}}
static JsonValue execute(JsonObject row){{String reference=row.get("ref").asString();var args=row.get("arguments").asArray();{dispatch}throw new RuntimeException("Unknown reference");}}
public static void main(String[] ignored)throws Exception{{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){{try{{results.add(execute(row.asObject()));}}catch(Throwable error){{results.add(new JsonObject().add("error",error.toString()));}}}}Files.writeString(Path.of("results.json"),results.toString());}}
}}
'''
    return '#include <fstream>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n' + prefix + code + f'''
bool sameRows(const std::vector<std::vector<int>>& values,const std::vector<const int*>& rows){{if(values.size()!=rows.size())return false;for(size_t i=0;i<rows.size();++i)if(values[i].data()!=rows[i])return false;return true;}}
json execute(const json& row){{std::string reference=row["ref"].get<std::string>();const auto& args=row["arguments"];{dispatch}throw std::runtime_error("Unknown reference");}}
int main(){{std::ifstream input("cases.json");json rows;input>>rows;json results=json::array();for(const auto& row:rows){{try{{results.push_back(execute(row));}}catch(const std::exception& error){{results.push_back(json{{{{"error",error.what()}}}});}}}}std::ofstream("results.json")<<results;}}
'''
