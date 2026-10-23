"""Fixed-width bit, binary64 and packed-byte API adapters without expected answers."""

import json
from core import HEADERS, ROOT


def primitive_source(language, starters=False, only_ref=None):
    entries = json.loads((ROOT / "ctci6/staged05/catalog.json").read_text())
    if only_ref is not None:
        entries = [e for e in entries if e["ref"] == only_ref]
        if len(entries) != 1:
            raise ValueError("Unknown bit exercise")
    prefix = HEADERS[language] + ("#include <cstdint>\n" if language == "cpp" else "")
    declarations = []
    branches = []
    for entry in entries:
        code = entry["languages"][language][
            "starterCode" if starters else "solutionCode"
        ]
        cls = "Solution_" + entry["ref"].replace(".", "_")
        if language not in ("python", "javascript"):
            code = code.replace("class Solution", "class " + cls, 1)
        declarations.append(code)
        count = len(entry["params"])
        method = entry["method"]
        ref = entry["ref"]
        if language == "python":
            branches.append(f"    if ref == {ref!r}: return {method}(*args)")
        elif language == "javascript":
            branches.append(f"if(ref==={json.dumps(ref)})return {method}(...args);")
        else:
            args = ",".join(
                f"args[{i}].GetInt32()"
                if language == "csharp"
                else f"args.get({i}).asInt()"
                if language == "java"
                else f"args[{i}].get<int>()"
                for i in range(count)
            )
            call = (
                ("new " + cls + "()" if language != "cpp" else cls + "()")
                + "."
                + method
                + "("
                + args
                + ")"
            )
            branches.append(
                f'if (reference == "{ref}") return {call};'
                if language != "java"
                else f'if (reference.equals("{ref}")) return Json.value({call});'
            )
    code = "\n".join(declarations)
    dispatch = "\n".join(branches)
    if language == "python":
        return (
            prefix
            + code
            + f"""
import json
def invoke(row):
    ref,args=row['ref'],row['arguments']
{dispatch}
    raise ValueError('Unknown reference')
def execute(row):
    value=invoke(row)
    return dict(actual=value,mutationOk=type(value) is int and -2147483648<=value<=2147483647)
results=[]
for row in json.load(open('cases.json',encoding='utf-8')):
    try:results.append(execute(row))
    except Exception as error:results.append(dict(error=repr(error)))
json.dump(results,open('results.json','w',encoding='utf-8'))
"""
        )
    if language == "javascript":
        return (
            prefix
            + code
            + f"""
const fs=require('node:fs');
function invoke(row){{const ref=row.ref,args=row.arguments;{dispatch}throw new Error('Unknown reference');}}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{{try{{const actual=invoke(row);return {{actual,mutationOk:Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647}};}}catch(error){{return {{error:String(error)}};}}}});
fs.writeFileSync('results.json',JSON.stringify(results));
"""
        )
    if language == "csharp":
        return (
            "using System.IO;\nusing System.Text.Json;\n"
            + prefix
            + code
            + f"""
class Harness {{
static int Invoke(JsonElement row){{string reference=row.GetProperty("ref").GetString()!;var args=row.GetProperty("arguments");{dispatch}throw new Exception("Unknown reference");}}
static object Execute(JsonElement row){{return new {{actual=Invoke(row),mutationOk=true}};}}
static void Main(){{using var document=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in document.RootElement.EnumerateArray()){{try{{results.Add(Execute(row));}}catch(Exception error){{results.Add(new {{error=error.ToString()}});}}}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}}
}}
"""
        )
    if language == "java":
        return (
            "import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n"
            + prefix
            + code
            + f"""
public class Harness {{
static JsonValue invoke(JsonObject row){{String reference=row.get("ref").asString();var args=row.get("arguments").asArray();{dispatch}throw new RuntimeException("Unknown reference");}}
static JsonValue execute(JsonObject row){{return new JsonObject().add("actual",invoke(row)).add("mutationOk",true);}}
public static void main(String[] ignored)throws Exception{{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){{try{{results.add(execute(row.asObject()));}}catch(Throwable error){{results.add(new JsonObject().add("error",error.toString()));}}}}Files.writeString(Path.of("results.json"),results.toString());}}
}}
"""
        )
    return (
        '#include <fstream>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n'
        + prefix
        + code
        + f"""
int invoke(const json& row){{std::string reference=row["ref"].get<std::string>();const auto& args=row["arguments"];{dispatch}throw std::runtime_error("Unknown reference");}}
json execute(const json& row){{return json{{{{"actual",invoke(row)}},{{"mutationOk",true}}}};}}
int main(){{std::ifstream input("cases.json");json rows;input>>rows;json results=json::array();for(const auto& row:rows){{try{{results.push_back(execute(row));}}catch(const std::exception& error){{results.push_back(json{{{{"error",error.what()}}}});}}}}std::ofstream("results.json")<<results;}}
"""
    )


def source(language, starters=False, only_ref=None):
    # Keep exact existing single-question adapters for unchanged int exercises.
    if only_ref in ("5.1", "5.6", "5.7"):
        return primitive_source(language, starters, only_ref)
    entries = json.loads((ROOT / "ctci6/staged05/catalog.json").read_text())
    if only_ref is not None:
        entries = [e for e in entries if e["ref"] == only_ref]
        if len(entries) != 1:
            raise ValueError("Unknown bit exercise")
    prefix = HEADERS[language] + ("#include <cstdint>\n" if language == "cpp" else "")
    declarations = []
    branches = []
    for entry in entries:
        code = entry["languages"][language][
            "starterCode" if starters else "solutionCode"
        ]
        cls = "Solution_" + entry["ref"].replace(".", "_")
        if language not in ("python", "javascript"):
            code = code.replace("class Solution", "class " + cls, 1)
        declarations.append(code)
        method, ref = entry["method"], entry["ref"]
        if language == "python":
            branches.append(f"    if ref == {ref!r}: return {method}(*args)")
            continue
        if language == "javascript":
            branches.append(f"if(ref==={json.dumps(ref)})return {method}(...args);")
            continue
        if ref == "5.8":
            continue
        args = []
        for i, (_, kind) in enumerate(entry["params"]):
            args.append(
                f"args[{i}]." + ("GetDouble()" if kind == "d" else "GetInt32()")
                if language == "csharp"
                else f"args.get({i})." + ("asDouble()" if kind == "d" else "asInt()")
                if language == "java"
                else f"args[{i}].get<" + ("double" if kind == "d" else "int") + ">()"
            )
        call = (
            ("new " + cls + "()" if language != "cpp" else cls + "()")
            + "."
            + method
            + "("
            + ",".join(args)
            + ")"
        )
        if language == "java":
            emit = (
                f"var actual={call};var output=new JsonArray();for(int value:actual)output.add(value);return output;"
                if entry["result"] == "ai"
                else f"return Json.value({call});"
            )
            branches.append(f'if(reference.equals("{ref}")){{{emit}}}')
        else:
            branches.append(f'if(reference=="{ref}")return {call};')
    code = "\n".join(declarations)
    dispatch = "\n".join(branches)
    has_bytes = any(e["ref"] == "5.8" for e in entries)
    if language == "python":
        return (
            prefix
            + code
            + f"""
import json
KINDS={repr({e["ref"]: e["result"] for e in entries})}
def invoke(row):
    ref,args=row['ref'],row['arguments']
{dispatch}
    raise ValueError('Unknown reference')
def execute(row):
    if row['ref']=='5.8':
        screen=bytearray(row['arguments'][0]);length=len(screen)
        returned=invoke(dict(ref=row['ref'],arguments=[screen,*row['arguments'][1:]]))
        return dict(actual=list(screen),mutationOk=returned is None and len(screen)==length)
    actual=invoke(row);kind=KINDS[row['ref']]
    valid=(type(actual) is str if kind=='s' else type(actual) is list and len(actual)==2 and all(type(v) is int and -2147483648<=v<=2147483647 for v in actual) if kind=='ai' else type(actual) is int and -2147483648<=actual<=2147483647)
    return dict(actual=actual,mutationOk=valid)
results=[]
for row in json.load(open('cases.json',encoding='utf-8')):
    try:results.append(execute(row))
    except Exception as error:results.append(dict(error=repr(error)))
json.dump(results,open('results.json','w',encoding='utf-8'))
"""
        )
    if language == "javascript":
        kinds = json.dumps({e["ref"]: e["result"] for e in entries})
        return (
            prefix
            + code
            + f"""
const fs=require('node:fs'),kinds={kinds};
function invoke(row){{const ref=row.ref,args=row.arguments;{dispatch}throw new Error('Unknown reference');}}
function execute(row){{if(row.ref==='5.8'){{const screen=new Uint8Array(row.arguments[0]),length=screen.length,returned=invoke({{ref:row.ref,arguments:[screen,...row.arguments.slice(1)]}});return {{actual:Array.from(screen),mutationOk:returned===undefined&&screen.length===length}};}}
const actual=invoke(row),kind=kinds[row.ref],integer=v=>Number.isInteger(v)&&v>=-2147483648&&v<=2147483647;return {{actual,mutationOk:kind==='s'?typeof actual==='string':kind==='ai'?Array.isArray(actual)&&actual.length===2&&actual.every(integer):integer(actual)}};}}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{{try{{return execute(row);}}catch(error){{return {{error:String(error)}};}}}});
fs.writeFileSync('results.json',JSON.stringify(results));
"""
        )
    if language == "csharp":
        byte_branch = (
            """if(row.GetProperty("ref").GetString()=="5.8") {var args=row.GetProperty("arguments");var screen=args[0].EnumerateArray().Select(v=>v.GetByte()).ToArray();int length=screen.Length;new Solution_5_8().DrawHorizontalLine(screen,args[1].GetInt32(),args[2].GetInt32(),args[3].GetInt32(),args[4].GetInt32());return new {actual=screen.Select(v=>(int)v).ToArray(),mutationOk=screen.Length==length};}"""
            if has_bytes
            else ""
        )
        return (
            "using System.IO;\nusing System.Text.Json;\n"
            + prefix
            + code
            + f"""
class Harness {{
static object Invoke(JsonElement row){{string reference=row.GetProperty("ref").GetString()!;var args=row.GetProperty("arguments");{dispatch}throw new Exception("Unknown reference");}}
static object Execute(JsonElement row){{{byte_branch}return new {{actual=Invoke(row),mutationOk=true}};}}
static void Main(){{using var document=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in document.RootElement.EnumerateArray()){{try{{results.Add(Execute(row));}}catch(Exception error){{results.Add(new {{error=error.ToString()}});}}}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}}
}}
"""
        )
    if language == "java":
        byte_branch = (
            """if(row.get("ref").asString().equals("5.8")){var args=row.get("arguments").asArray();var raw=args.get(0).asArray();byte[] screen=new byte[raw.size()];for(int i=0;i<screen.length;i++)screen[i]=(byte)raw.get(i).asInt();new Solution_5_8().DrawHorizontalLine(screen,args.get(1).asInt(),args.get(2).asInt(),args.get(3).asInt(),args.get(4).asInt());var output=new JsonArray();for(byte value:screen)output.add(value & 255);return new JsonObject().add("actual",output).add("mutationOk",screen.length==raw.size());}"""
            if has_bytes
            else ""
        )
        return (
            "import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n"
            + prefix
            + code
            + f"""
public class Harness {{
static JsonValue invoke(JsonObject row){{String reference=row.get("ref").asString();var args=row.get("arguments").asArray();{dispatch}throw new RuntimeException("Unknown reference");}}
static JsonValue execute(JsonObject row){{{byte_branch}return new JsonObject().add("actual",invoke(row)).add("mutationOk",true);}}
public static void main(String[] ignored)throws Exception{{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){{try{{results.add(execute(row.asObject()));}}catch(Throwable error){{results.add(new JsonObject().add("error",error.toString()));}}}}Files.writeString(Path.of("results.json"),results.toString());}}
}}
"""
        )
    byte_branch = (
        """if(row["ref"]=="5.8"){const auto& args=row["arguments"];auto screen=args[0].get<std::vector<std::uint8_t>>();auto pointer=screen.data();auto length=screen.size();Solution_5_8().DrawHorizontalLine(screen,args[1].get<int>(),args[2].get<int>(),args[3].get<int>(),args[4].get<int>());return json{{"actual",screen},{"mutationOk",screen.size()==length && screen.data()==pointer}};}"""
        if has_bytes
        else ""
    )
    return (
        '#include <fstream>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n'
        + prefix
        + code
        + f"""
json invoke(const json& row){{std::string reference=row["ref"].get<std::string>();const auto& args=row["arguments"];{dispatch}throw std::runtime_error("Unknown reference");}}
json execute(const json& row){{{byte_branch}return json{{{{"actual",invoke(row)}},{{"mutationOk",true}}}};}}
int main(){{std::ifstream input("cases.json");json rows;input>>rows;json results=json::array();for(const auto& row:rows){{try{{results.push_back(execute(row));}}catch(const std::exception& error){{results.push_back(json{{{{"error",error.what()}}}});}}}}std::ofstream("results.json")<<results;}}
"""
    )
