"""Primitive int APIs: no reference algorithm or expected answers in the child."""

import json
from core import HEADERS, ROOT


def primitive_source(language, starters=False, only_ref=None):
    entries = json.loads((ROOT / "ctci6/staged08/catalog.json").read_text())
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
    from models08 import header

    if only_ref in ("8.1", "8.5", "8.11"):
        return primitive_source(language, starters, only_ref)
    entries = json.loads((ROOT / "ctci6/staged08/catalog.json").read_text())
    if only_ref is not None:
        entries = [e for e in entries if e["ref"] == only_ref]
        if len(entries) != 1:
            raise ValueError("Unknown recursion/DP reference")
    prefix = header("8.4", language)
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
        ref = entry["ref"]
        method = entry["method"]
        if language == "python":
            branches.append(f"    if ref == {ref!r}: return {method}(*args)")
            continue
        if language == "javascript":
            branches.append(f"if(ref==={json.dumps(ref)})return {method}(...args);")
            continue
        if ref == "8.4":
            continue
        arguments = []
        for i, (_, kind) in enumerate(entry["params"]):
            arguments.append(
                f"args[{i}]." + ("GetString()!" if kind == "s" else "GetInt32()")
                if language == "csharp"
                else f"args.get({i})." + ("asString()" if kind == "s" else "asInt()")
                if language == "java"
                else f"args[{i}].get<"
                + ("std::string" if kind == "s" else "int")
                + ">()"
            )
        call = (
            ("new " + cls + "()" if language != "cpp" else cls + "()")
            + "."
            + method
            + "("
            + ",".join(arguments)
            + ")"
        )
        if language == "java":
            emit = (
                f"var actual={call};var output=new JsonArray();for(String value:actual)output.add(value);return output;"
                if entry["result"] == "strings"
                else f"return Json.value({call});"
            )
            branches.append(f'if(reference.equals("{ref}")){{{emit}}}')
        else:
            branches.append(f'if(reference=="{ref}")return {call};')
    code = "\n".join(declarations)
    dispatch = "\n".join(branches)
    has_sets = any(e["ref"] == "8.4" for e in entries)
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
    if row['ref']=='8.4':
        values=row['arguments'][0].copy();before=values.copy()
        actual=invoke(dict(ref=row['ref'],arguments=[values]))
        return dict(actual=actual,mutationOk=len(values)==len(before) and all(type(v) is int and v==before[i] for i,v in enumerate(values)))
    actual=invoke(row);kind=KINDS[row['ref']]
    valid=type(actual) is list and all(type(v) is str for v in actual) if kind=='strings' else type(actual) is int and -2147483648<=actual<=2147483647
    return dict(actual=actual,mutationOk=valid)
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
const fs=require('node:fs'),kinds={json.dumps({e["ref"]: e["result"] for e in entries})};
function invoke(row){{const ref=row.ref,args=row.arguments;{dispatch}throw new Error('Unknown reference');}}
function execute(row){{if(row.ref==='8.4'){{const values=row.arguments[0].slice(),before=values.slice(),actual=invoke({{ref:row.ref,arguments:[values]}});return {{actual,mutationOk:values.length===before.length&&values.every((v,i)=>v===before[i])}};}}
const actual=invoke(row);return {{actual,mutationOk:kinds[row.ref]==='strings'?Array.isArray(actual)&&actual.every(v=>typeof v==='string'):Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647}};}}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{{try{{return execute(row);}}catch(error){{return {{error:String(error)}};}}}});
fs.writeFileSync('results.json',JSON.stringify(results));
"""
        )
    if language == "csharp":
        sets = (
            """if(row.GetProperty("ref").GetString()=="8.4"){var values=row.GetProperty("arguments")[0].EnumerateArray().Select(v=>v.GetInt32()).ToArray();var before=values.ToArray();var actual=new Solution_8_4().PowerSet(values);return new {actual,mutationOk=values.SequenceEqual(before)};}"""
            if has_sets
            else ""
        )
        return (
            "using System.IO;\nusing System.Text.Json;\n"
            + prefix
            + code
            + f"""
class Harness {{
static object Invoke(JsonElement row){{string reference=row.GetProperty("ref").GetString()!;var args=row.GetProperty("arguments");{dispatch}throw new Exception("Unknown reference");}}
static object Execute(JsonElement row){{{sets}return new {{actual=Invoke(row),mutationOk=true}};}}
static void Main(){{using var document=JsonDocument.Parse(File.ReadAllText("cases.json"));var results=new List<object>();foreach(var row in document.RootElement.EnumerateArray()){{try{{results.Add(Execute(row));}}catch(Exception error){{results.Add(new {{error=error.ToString()}});}}}}File.WriteAllText("results.json",JsonSerializer.Serialize(results));}}
}}
"""
        )
    if language == "java":
        sets = (
            """if(row.get("ref").asString().equals("8.4")){var raw=row.get("arguments").asArray().get(0).asArray();int[] values=new int[raw.size()];for(int i=0;i<values.length;++i)values[i]=raw.get(i).asInt();int[] before=values.clone();var actual=new Solution_8_4().PowerSet(values);var output=new JsonArray();for(var subset:actual){var entry=new JsonArray();for(int value:subset)entry.add(value);output.add(entry);}return new JsonObject().add("actual",output).add("mutationOk",Arrays.equals(values,before));}"""
            if has_sets
            else ""
        )
        return (
            "import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n"
            + prefix
            + code
            + f"""
public class Harness {{
static JsonValue invoke(JsonObject row){{String reference=row.get("ref").asString();var args=row.get("arguments").asArray();{dispatch}throw new RuntimeException("Unknown reference");}}
static JsonValue execute(JsonObject row){{{sets}return new JsonObject().add("actual",invoke(row)).add("mutationOk",true);}}
public static void main(String[] ignored)throws Exception{{var results=new JsonArray();for(var row:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){{try{{results.add(execute(row.asObject()));}}catch(Throwable error){{results.add(new JsonObject().add("error",error.toString()));}}}}Files.writeString(Path.of("results.json"),results.toString());}}
}}
"""
        )
    sets = (
        """if(row["ref"]=="8.4"){auto values=row["arguments"][0].get<std::vector<int>>();auto before=values;auto actual=Solution_8_4().PowerSet(values);return json{{"actual",actual},{"mutationOk",values==before}};}"""
        if has_sets
        else ""
    )
    return (
        '#include <fstream>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n'
        + prefix
        + code
        + f"""
json invoke(const json& row){{std::string reference=row["ref"].get<std::string>();const auto& args=row["arguments"];{dispatch}throw std::runtime_error("Unknown reference");}}
json execute(const json& row){{{sets}return json{{{{"actual",invoke(row)}},{{"mutationOk",true}}}};}}
int main(){{std::ifstream input("cases.json");json rows;input>>rows;json results=json::array();for(const auto& row:rows){{try{{results.push_back(execute(row));}}catch(const std::exception& error){{results.push_back(json{{{{"error",error.what()}}}});}}}}std::ofstream("results.json")<<results;}}
"""
    )
