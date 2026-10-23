"""Invoke actual state APIs and retain admitted-animal object identity."""

import json

from chapter03 import APIS
from core import EXT, ROOT
from models03 import ANIMAL, header


def source(language, starters=False, only_ref=None):
    entries = json.loads((ROOT / "ctci6/staged03/catalog.json").read_text())
    if only_ref is not None:
        entries = [e for e in entries if e["ref"] == only_ref]
        if len(entries) != 1:
            raise ValueError("Unknown state reference: " + only_ref)
    apis = {
        ref: api for ref, api in APIS.items() if only_ref is None or ref == only_ref
    }
    pieces = [header("3.5", language) + ANIMAL[language]]
    pieces.extend(
        e["languages"][language]["starterCode" if starters else "solutionCode"]
        for e in entries
    )
    config = {
        ref: dict(cls=cls, methods={name: result for name, _, result in methods})
        for ref, (cls, _, methods) in apis.items()
    }
    if language == "python":
        pieces.append(PYTHON.replace("CONFIG_VALUE", repr(config)))
    elif language == "javascript":
        pieces.append(
            JAVASCRIPT.replace("CONFIG_VALUE", json.dumps(config)).replace(
                "CLASSES_VALUE",
                "{"
                + ",".join(json.dumps(c) + ":" + c for c, _, _ in apis.values())
                + "}",
            )
        )
    else:
        template = (
            ROOT / "scripts/ctci6/templates03" / ("Harness." + EXT[language])
        ).read_text()
        start = template.index("SORT_BRANCH_START\n")
        end = template.index("SORT_BRANCH_END\n", start) + len("SORT_BRANCH_END\n")
        branch = (
            template[start:end]
            .replace("SORT_BRANCH_START\n", "")
            .replace("SORT_BRANCH_END\n", "")
        )
        template = (
            template[:start]
            + (branch if only_ref in (None, "3.5") else "")
            + template[end:]
        )
        if language == "csharp":
            pieces.insert(
                0,
                "using System.IO;\nusing System.Reflection;\nusing System.Text.Json;\n",
            )
            pieces.append(
                template.replace("CONFIG_VALUE", json.dumps(config).replace('"', '""'))
            )
        elif language == "java":
            pieces.insert(
                0,
                "import java.nio.file.*;\nimport epi.test_framework.minimal_json.*;\n",
            )
            pieces.append(
                template.replace("CONFIG_VALUE", json.dumps(json.dumps(config)))
            )
        else:
            pieces.insert(
                0,
                '#include <fstream>\n#include <unordered_set>\n#include "test_framework/json.h"\nusing json=nlohmann::json;\n',
            )
            branches = []
            for ref, (cls, constructor, methods) in apis.items():
                calls = []
                for name, params, result in methods:
                    arguments = [
                        "animal" if kind == "animal" else f"raw[{i}].get<int>()"
                        for i, (_, kind) in enumerate(params)
                    ]
                    expression = "instance." + name + "(" + ",".join(arguments) + ")"
                    prepare = (
                        ""
                        if name != "Enqueue"
                        else "owners.push_back(std::make_unique<Animal>(raw[0].get<int>(),raw[1].get<std::string>()));auto animal=owners.back().get();originals.insert(animal);"
                    )
                    emit = (
                        expression + ";output.push_back(nullptr);"
                        if result == "void"
                        else "output.push_back(" + expression + ");"
                    )
                    if result == "animal":
                        emit = (
                            "auto value="
                            + expression
                            + ';if(value && !originals.count(value)){valid=false;output.push_back(json{{"invalidIdentity",true}});}else output.push_back(value?json(value->Id):json(nullptr));'
                        )
                    calls.append(
                        ("if" if not calls else "else if")
                        + '(op=="'
                        + name
                        + '") {'
                        + prepare
                        + emit
                        + "}"
                    )
                ctor = "(arguments[0][0].get<int>())" if constructor else ""
                loop = (
                    "output.push_back(nullptr);for(size_t i=1;i<operations.size();++i){std::string op=operations[i].get<std::string>();const auto& raw=arguments[i];try{"
                    + "\n".join(calls)
                    + 'else throw std::runtime_error("Unknown operation");}catch(const BankError& error){output.push_back(json{{"error",error.Code}});}}'
                )
                branches.append(
                    'if(ref=="'
                    + ref
                    + '") { try { '
                    + cls
                    + " instance"
                    + ctor
                    + "; "
                    + loop
                    + ' } catch(const BankError& error) { output.push_back(json{{"error",error.Code}}); } }'
                )
            pieces.append(template.replace("STATE_BRANCHES", "\n".join(branches)))
    return "\n".join(pieces)


PYTHON = """
import json
CONFIG=CONFIG_VALUE
def execute(row):
    ref,args=row['ref'],row['arguments']
    if ref=='3.5':
        stack=IntStack()
        for value in args[0]:stack.Push(value)
        SortStack(stack)
        output=[]
        while not stack.IsEmpty():
            output.append(stack.Pop())
            if len(output)>len(args[0]):return dict(actual=output,mutationOk=False)
        return dict(actual=output,mutationOk=True)
    config=CONFIG[ref]
    operations,arguments=args
    output=[];instance=None;valid=True;animals=[]
    for index,(op,parameters) in enumerate(zip(operations,arguments)):
        try:
            if index==0:
                instance=globals()[config['cls']](*parameters)
                output.append(None)
                continue
            if op=='Enqueue':
                animal=Animal(*parameters)
                animals.append((animal,animal.Id,animal.Species))
                parameters=[animal]
            value=getattr(instance,op)(*parameters)
            kind=config['methods'][op]
            if kind=='animal':
                if value is not None:
                    if not any(value is original for original,_,_ in animals):valid=False;value={'invalidIdentity':True}
                    else:value=value.Id
            elif kind=='void':
                if value is not None:valid=False
                value=None
            elif kind=='i' and type(value) is not int:valid=False;value={'invalidReturn':'integer'}
            elif kind=='b' and type(value) is not bool:valid=False;value={'invalidReturn':'boolean'}
            output.append(value)
        except BankError as error:output.append(dict(error=error.Code))
    valid=valid and all(a.Id==id and a.Species==species for a,id,species in animals)
    return dict(actual=output,mutationOk=valid)
results=[]
for row in json.load(open('cases.json',encoding='utf-8')):
    try:results.append(execute(row))
    except Exception as error:results.append(dict(error=repr(error)))
json.dump(results,open('results.json','w',encoding='utf-8'))
"""

JAVASCRIPT = """
const fs=require('node:fs');
const config=CONFIG_VALUE,classes=CLASSES_VALUE;
function execute(row){
const ref=row.ref,args=row.arguments;
if(ref==='3.5'){const stack=new IntStack();for(const value of args[0])stack.Push(value);SortStack(stack);const output=[];while(!stack.IsEmpty()){output.push(stack.Pop());if(output.length>args[0].length)return {actual:output,mutationOk:false};}return {actual:output,mutationOk:true};}
const [operations,argumentsList]=args,output=[],animals=[];
let instance=null,valid=true;
for(let i=0;i<operations.length;++i){const op=operations[i];let parameters=argumentsList[i];try{
if(i===0){instance=new classes[config[ref].cls](...parameters);output.push(null);continue;}
if(op==='Enqueue'){const animal=new Animal(...parameters);animals.push([animal,animal.Id,animal.Species]);parameters=[animal];}
let value=instance[op](...parameters);const kind=config[ref].methods[op];
if(kind==='animal'&&value!==null){if(!animals.some(a=>a[0]===value)){valid=false;value={invalidIdentity:true};}else value=value.Id;}
else if(kind==='void'){if(value!==undefined&&value!==null)valid=false;value=null;}
else if(kind==='i'&&!Number.isInteger(value)){valid=false;value={invalidReturn:'integer'};}
else if(kind==='b'&&typeof value!=='boolean'){valid=false;value={invalidReturn:'boolean'};}
output.push(value);
}catch(error){if(!(error instanceof BankError))throw error;output.push({error:error.Code});}}
valid=valid&&animals.every(([a,id,species])=>a.Id===id&&a.Species===species);
return {actual:output,mutationOk:valid};}
const results=JSON.parse(fs.readFileSync('cases.json','utf8')).map(row=>{try{return execute(row);}catch(error){return {error:String(error)};}});
fs.writeFileSync('results.json',JSON.stringify(results));
"""
