"""Independent authoring execution adapters, including identity observations.

These adapters test staged content, not the website submission integration. That
later acceptance stage must execute the exact published callable envelopes too.
"""

import json
from textwrap import indent

from chapter01 import SPECS
from core import HEADERS, ROOT, TYPES


def source(language, starters=False):
    sources = [HEADERS[language]]
    catalog = json.loads((ROOT / "ctci6/staged/catalog.json").read_text())
    for spec in SPECS:
        entry = next(row for row in catalog if row["ref"] == spec["ref"])
        code = entry["languages"][language][
            "starterCode" if starters else "solutionCode"
        ]
        if language not in ("python", "javascript"):
            # Rename only the known bank-owned outer class for batch execution.
            # Execute the staged algorithm's exact formatted body unchanged.
            if code.count("class Solution") != 1:
                raise ValueError("Unexpected staged class declaration")
            code = code.replace(
                "class Solution", "class Solution_" + spec["ref"].replace(".", "_"), 1
            )
        # The Java batch has several package-private classes in one file.
        sources.append(code)
    if language in ("python", "javascript"):
        modes = {
            s["ref"]: dict(method=s["method"], mutation=s["mutation"]) for s in SPECS
        }
        if language == "python":
            sources.append(
                """
import copy, json
MODES = MODES_VALUE
results = []
for row in json.load(open('cases.json', encoding='utf-8')):
    arguments = copy.deepcopy(row['arguments'])
    before = copy.deepcopy(arguments)
    mode = MODES[row['ref']]
    saved_rows = list(arguments[0]) if mode['mutation'] == 'matrix' else []
    try:
        result = globals()[mode['method']](*arguments)
        observed = arguments[0] if mode['mutation'] != 'preserve' else result
        valid = (arguments == before if mode['mutation'] == 'preserve' else
                 len(arguments[0]) == len(before[0]) and
                 all(a is b and len(a) == len(old) for a,b,old in zip(arguments[0],saved_rows,before[0]))
                 if mode['mutation'] == 'matrix' else len(arguments[0]) == len(before[0]))
        results.append(dict(ref=row['ref'], actual=observed, mutationOk=valid))
    except Exception as error:
        results.append(dict(ref=row['ref'], error=repr(error)))
json.dump(results, open('results.json', 'w', encoding='utf-8'))
""".replace("MODES_VALUE", repr(modes))
            )
        else:
            sources.append(
                """
const fs = require('node:fs');
const modes = MODES_VALUE;
const functions = FUNCTIONS_VALUE;
const results = JSON.parse(fs.readFileSync('cases.json', 'utf8')).map(row => {
    const args = structuredClone(row.arguments), before = structuredClone(args);
    const mode = modes[row.ref], savedRows = mode.mutation === 'matrix' ? [...args[0]] : [];
    try {
        const value = functions[row.ref](...args);
        const valid = mode.mutation === 'preserve' ? JSON.stringify(args) === JSON.stringify(before) :
          args[0].length === before[0].length && (mode.mutation !== 'matrix' ||
          args[0].every((r,i) => r === savedRows[i] && r.length === before[0][i].length));
        return {ref:row.ref, actual:mode.mutation === 'preserve' ? value : args[0], mutationOk:valid};
    } catch(error) { return {ref:row.ref, error:String(error)}; }
});
fs.writeFileSync('results.json', JSON.stringify(results));
""".replace("MODES_VALUE", json.dumps(modes)).replace(
                    "FUNCTIONS_VALUE",
                    "{"
                    + ",".join(json.dumps(s["ref"]) + ":" + s["method"] for s in SPECS)
                    + "}",
                )
            )
        return "\n".join(sources)
    dispatch = []
    for spec in SPECS:
        ref = spec["ref"]
        declarations = []
        for index, (_, kind) in enumerate(spec["params"]):
            t = TYPES[language][kind]
            expression = {
                "csharp": f"JsonSerializer.Deserialize<{t}>(args[{index}].GetRawText())!",
                "java": {
                    "s": f"args.get({index}).asString()",
                    "i": f"args.get({index}).asInt()",
                    "chars": f"chars(args.get({index}))",
                    "aai": f"matrix(args.get({index}))",
                }.get(kind),
                "cpp": f"chars(args[{index}])"
                if kind == "chars"
                else f"args[{index}].get<{t}>()",
            }[language]
            declarations.append(t + f" a{index} = " + expression + ";")
        args_list = ",".join("a" + str(i) for i in range(len(spec["params"])))
        call = (
            (
                "Solution_" + ref.replace(".", "_") + "()."
                if language == "cpp"
                else "new Solution_" + ref.replace(".", "_") + "()."
            )
            + spec["method"]
            + "("
            + args_list
            + ")"
        )
        is_void = spec["result"] == "void"
        if spec["mutation"] == "matrix":
            declarations.append(
                {
                    "csharp": "var saved = (int[][])a0.Clone();",
                    "java": "int[][] saved = a0.clone();",
                    "cpp": "std::vector<const int*> saved; for (const auto& r:a0) saved.push_back(r.data());",
                }[language]
            )
        if is_void:
            declarations.append(call + ";")
            result = "a0"
        else:
            declarations.append(
                ("auto" if language == "cpp" else TYPES[language][spec["result"]])
                + " value = "
                + call
                + ";"
            )
            result = "value"
        valid = "true"
        if spec["mutation"] == "matrix":
            declarations.append(
                {
                    "csharp": "bool valid = a0.Length == saved.Length; for(int i=0;i<saved.Length;i++) valid &= ReferenceEquals(a0[i],saved[i]);",
                    "java": "boolean valid = a0.length == saved.length; for(int i=0;i<saved.length;i++) valid &= a0[i] == saved[i];",
                    "cpp": "bool valid = a0.size() == saved.size(); for(size_t i=0;i<saved.size();i++) valid = valid && a0[i].data() == saved[i];",
                }[language]
            )
            valid = "valid"
        elif spec["mutation"] == "chars":
            valid = {
                "csharp": "a0.Length == args[0].GetArrayLength()",
                "java": "a0.length == args.get(0).asArray().size()",
                "cpp": "a0.size() == args[0].size()",
            }[language]
        if language == "csharp":
            if spec["mutation"] == "chars":
                result = "Array.ConvertAll(a0, c => c.ToString())"
            ending = (
                "return new { actual = " + result + ", mutationOk = " + valid + " };"
            )
        elif language == "java":
            ending = (
                'return new JsonObject().add("actual", dump('
                + result
                + ')).add("mutationOk", '
                + valid
                + ");"
            )
        else:
            if spec["mutation"] == "chars":
                result = "dumpChars(a0)"
            ending = (
                'return json{{"actual", '
                + result
                + '}, {"mutationOk", '
                + valid
                + "}};"
            )
        dispatch.append(
            "case "
            + json.dumps(ref)
            + ": {\n"
            + indent("\n".join(declarations) + "\n" + ending, "    ")
            + "\n}"
        )
    cases = "\n".join(dispatch)
    if language == "csharp":
        sources.insert(0, "using System.IO;\nusing System.Text.Json;\n")
        sources.append(
            """
class Harness {
static object Execute(string reference, JsonElement args) {
switch(reference) {
CASES
default: throw new Exception("Unknown exercise");
}}
static void Main() {
using var document = JsonDocument.Parse(File.ReadAllText("cases.json"));
var result = new List<object>();
foreach(var row in document.RootElement.EnumerateArray()) {
try { result.Add(Execute(row.GetProperty("ref").GetString()!,row.GetProperty("arguments"))); }
catch(Exception error) { result.Add(new { error = error.ToString() }); }
}
File.WriteAllText("results.json",JsonSerializer.Serialize(result));
}}
""".replace("CASES", cases)
        )
    elif language == "java":
        sources.insert(
            0, "import epi.test_framework.minimal_json.*;\nimport java.nio.file.*;\n"
        )
        sources.append(
            """
public class Harness {
static char[] chars(JsonValue value) { JsonArray a=value.asArray(); char[] out=new char[a.size()]; for(int i=0;i<out.length;i++) out[i]=a.get(i).asString().charAt(0); return out; }
static int[][] matrix(JsonValue value) { JsonArray a=value.asArray(); int[][] out=new int[a.size()][]; for(int r=0;r<out.length;r++){JsonArray row=a.get(r).asArray();out[r]=new int[row.size()];for(int c=0;c<row.size();c++)out[r][c]=row.get(c).asInt();}return out; }
static JsonValue dump(boolean value){return Json.value(value);}
static JsonValue dump(String value){return Json.value(value);}
static JsonValue dump(char[] value){JsonArray out=new JsonArray();for(char c:value)out.add(String.valueOf(c));return out;}
static JsonValue dump(int[][] value){JsonArray out=new JsonArray();for(int[] row:value){JsonArray a=new JsonArray();for(int x:row)a.add(x);out.add(a);}return out;}
static JsonValue execute(String reference, JsonArray args){switch(reference){
CASES
default:throw new RuntimeException("Unknown exercise");}}
public static void main(String[] ignored)throws Exception{
JsonArray results=new JsonArray();
for(JsonValue item:Json.parse(Files.readString(Path.of("cases.json"))).asArray()){
JsonObject row=item.asObject();
try{results.add(execute(row.get("ref").asString(),row.get("arguments").asArray()));}
catch(Throwable error){results.add(new JsonObject().add("error",error.toString()));}
}
Files.writeString(Path.of("results.json"),results.toString());
}}
""".replace("CASES", cases)
        )
    else:
        sources.insert(
            0,
            '#include <fstream>\n#include <stdexcept>\n#include "test_framework/json.h"\nusing json = nlohmann::json;\n',
        )
        # C++ cannot switch on a string.
        for spec in SPECS:
            cases = cases.replace(
                "case " + json.dumps(spec["ref"]) + ":",
                "if(reference == " + json.dumps(spec["ref"]) + ")",
            )
        sources.append(
            """
std::vector<char> chars(const json& value){std::vector<char> out;for(const auto& x:value)out.push_back(x.get<std::string>()[0]);return out;}
json dumpChars(const std::vector<char>& value){json out=json::array();for(char c:value)out.push_back(std::string(1,c));return out;}
json execute(const std::string& reference,const json& args){
CASES
throw std::runtime_error("Unknown exercise");}
int main(){std::ifstream input("cases.json");json rows;input>>rows;json out=json::array();for(const auto& row:rows){try{out.push_back(execute(row["ref"].get<std::string>(),row["arguments"]));}catch(const std::exception& error){out.push_back(json{{"error",error.what()}});}}std::ofstream("results.json")<<out;}
""".replace("CASES", cases)
        )
    return "\n".join(sources)
