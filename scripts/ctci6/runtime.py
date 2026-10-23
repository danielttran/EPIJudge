"""Build separate-module adapters from exact bank-owned authoring templates.

Only known checked-in declarations are removed from judge templates. User code,
drafts and imported answers never pass through this transformation. The resulting
judge contains structural decoding/observation, not a hidden reference solution.
"""

import json
import re

import harness01
import harness02
import harness03
import harness05
import harness08
import harness16
import harness17
import models08
import models03
from core import HEADERS, LANGUAGES, ROOT
from models02 import MODELS, header


def timed(source, language, batch):
    if language == "python":
        source = "import time\n" + source
        source, count = re.subn(
            r"(^for row in json\.load\([^\n]+\):\n)",
            r"\1    clock = time.perf_counter()\n",
            source,
            count=1,
            flags=re.M,
        )
        if count != 1:
            raise ValueError("Unknown Python judge loop")
        index = source.index("json.dump(results")
        return (
            source[:index]
            + "    results[-1] = dict(observation=results[-1], elapsedMs=(time.perf_counter()-clock)*1000)\n"
            + source[index:]
        )
    if language == "javascript":
        source, count = re.subn(
            r"\.map\((row\s*=>\s*\{)", r".map(timed(\1", source, count=1
        )
        if count != 1:
            raise ValueError("Unknown JavaScript judge loop")
        index = source.index("\nfs.writeFileSync")
        before = source[:index].rstrip()
        if not before.endswith(");"):
            raise ValueError("Unknown JavaScript loop terminator")
        source = before[:-2] + "));" + source[index:]
        return (
            source
            + "\nfunction timed(fn) { return row => { const start=performance.now(); let observation; try { observation=fn(row); } catch(error) { observation={error:String(error)}; } return {observation,elapsedMs:performance.now()-start}; }; }\n"
        )
    if language == "csharp":
        parameters = (
            "string reference, JsonElement args" if batch == 1 else "JsonElement row"
        )
        arguments = "reference,args" if batch == 1 else "row"
        helper = f"""static object TimedExecute({parameters}) {{
var clock=System.Diagnostics.Stopwatch.StartNew();object observed;
try {{ observed=Execute({arguments}); }} catch(Exception error) {{ observed=new {{error=error.ToString()}}; }}
return new {{observation=observed,elapsedMs=clock.Elapsed.TotalMilliseconds}};
}}
"""
        if source.count(".Add(Execute(") != 1:
            raise ValueError("Unknown C# judge invocation")
        return source.replace(".Add(Execute(", ".Add(TimedExecute(", 1).replace(
            "static void Main()", helper + "static void Main()", 1
        )
    if language == "java":
        parameters = (
            "String reference,JsonArray args" if batch == 1 else "JsonObject row"
        )
        arguments = "reference,args" if batch == 1 else "row"
        helper = f"""static JsonValue timedExecute({parameters}) {{
long start=System.nanoTime();JsonValue observed;
try {{ observed=execute({arguments}); }} catch(Throwable error) {{ observed=new JsonObject().add("error",error.toString()); }}
return new JsonObject().add("observation",observed).add("elapsedMs",(System.nanoTime()-start)/1000000.0);
}}
"""
        if source.count(".add(execute(") != 1:
            raise ValueError("Unknown Java judge invocation")
        return source.replace(".add(execute(", ".add(timedExecute(", 1).replace(
            "public static void main", helper + "public static void main", 1
        )
    parameters = (
        "const std::string& reference,const json& args"
        if batch == 1
        else "const json& row"
    )
    arguments = "reference,args" if batch == 1 else "row"
    helper = f"""json timedExecute({parameters}) {{
auto start=std::chrono::steady_clock::now();json observed;
try {{ observed=execute({arguments}); }} catch(const std::exception& error) {{ observed=json{{{{"error",error.what()}}}}; }}
double elapsed=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-start).count();
return json{{{{"observation",observed}},{{"elapsedMs",elapsed}}}};
}}
"""
    if source.count(".push_back(execute(") != 1:
        raise ValueError("Unknown C++ judge invocation")
    return "#include <chrono>\n" + source.replace(
        ".push_back(execute(", ".push_back(timedExecute(", 1
    ).replace("int main()", helper + "int main()", 1)


def submission_prefix(batch, language, reference=None):
    if batch in (8, 16, 17):
        return models08.header(reference, language)
    if batch in (1, 5):
        return HEADERS[language] + (
            "#include <cstdint>\n" if batch == 5 and language == "cpp" else ""
        )
    if batch == 2:
        return header(language)
    if batch == 3:
        return models03.header("3.5", language) + models03.ANIMAL[language]
    raise ValueError("Unsupported submission batch")


def adapter(entry, language, batch):
    module = {1: harness01, 2: harness02, 3: harness03, 5: harness05, 8: harness08, 16: harness16, 17: harness17}[
        batch
    ]
    bank = module.source(language, only_ref=entry["ref"])
    code = entry["languages"][language]["solutionCode"]
    name = "Solution_" + entry["ref"].replace(".", "_")
    declaration = (
        code.replace("class Solution", "class " + name, 1)
        if batch != 3 and language not in ("python", "javascript")
        else code
    )
    if bank.count(declaration) != 1:
        raise ValueError("Judge source does not contain the exact owned declaration")
    bank = bank.replace(declaration, "", 1).replace(name, "Solution")
    owned_header = submission_prefix(batch, language, entry["ref"])
    if owned_header:
        if bank.count(owned_header) != 1:
            raise ValueError("Judge header does not match its recorded owned header")
        bank = bank.replace(owned_header, "", 1)
    if language == "python":
        imports = (
            "import solution as user\n"
            + entry["method"]
            + " = user."
            + entry["method"]
            + "\n"
        )
        if batch == 2:
            imports += "LinkedListNode = user.LinkedListNode\n"
        elif batch == 3:
            imports += "BankError = user.BankError\nIntStack = user.IntStack\nAnimal = user.Animal\n"
    elif language == "javascript":
        imports = (
            "const user = require('./solution.js');\nconst "
            + entry["method"]
            + " = user."
            + entry["method"]
            + ";\n"
        )
        if batch == 2:
            imports += "const LinkedListNode = user.LinkedListNode;\n"
        elif batch == 3:
            imports += "const {BankError, IntStack, Animal} = user;\n"
    else:
        imports = HEADERS[language]
        if language == "cpp":
            imports += '#include "solution.cpp"\n'
    if batch == 2 and language == "csharp":
        bank = bank.replace("\"Solution_\"+reference.Replace('.','_')", '"Solution"')
    if batch == 2 and language == "java":
        bank = bank.replace("\"Solution_\"+ref.replace('.','_')", '"Solution"')
    if "Solution_" in bank:
        raise ValueError("A batch class name remains in the separate-module judge")
    return timed(imports + bank, language, batch)


def generate_runtime():
    rows = []
    for batch, folder in (
        (1, "staged"),
        (2, "staged02"),
        (3, "staged03"),
        (5, "staged05"),
        (8, "staged08"),
        (16, "staged16"),
        (17, "staged17"),
    ):
        for entry in json.loads((ROOT / "ctci6" / folder / "catalog.json").read_text()):
            item = {
                k: entry[k]
                for k in (
                    "id",
                    "ref",
                    "title",
                    "description",
                    "constraints",
                    "method",
                    "params",
                    "result",
                    "mutation",
                    "testCount",
                )
            }
            item.update(
                batch=batch,
                stagingDirectory=folder,
                example=entry["example"],
                languages={},
            )
            for language in LANGUAGES:
                code = entry["languages"][language]
                prefix = submission_prefix(batch, language, entry["ref"])
                exports = (
                    ["LinkedListNode"]
                    if batch == 2
                    else ["BankError", "IntStack", "Animal"]
                    if batch == 3
                    else []
                ) + [entry["method"]]
                suffix = (
                    "\nmodule.exports = {" + ",".join(exports) + "};\n"
                    if language == "javascript"
                    else ""
                )
                item["languages"][language] = dict(
                    code,
                    prefix=prefix,
                    suffix=suffix,
                    harness=adapter(entry, language, batch),
                    reference=MODELS[language]
                    if batch == 2
                    else (
                        models03.header(entry["ref"], language).removeprefix(
                            HEADERS[language]
                        )
                        if batch == 3
                        else ""
                    ),
                )
            rows.append(item)
    directory = ROOT / "ctci6/runtime"
    directory.mkdir(exist_ok=True)
    (directory / "catalog.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(
        f"Prepared {len(rows) * len(LANGUAGES)} separate-module staged submission adapters; no live catalog registration."
    )


if __name__ == "__main__":
    generate_runtime()
