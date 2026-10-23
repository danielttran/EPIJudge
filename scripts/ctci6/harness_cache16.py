"""Expected-answer-free observation for the string-valued cache state API."""

def parts(language,code):
    if language=='python':return code+'''
def executeCache(row):
    import json
    args=row['arguments'];before=json.dumps(args)
    capacity,operations,keys,values=args
    instance=LRUCache(capacity);output=[None];valid=True
    for op,key,value in zip(operations[1:],keys[1:],values[1:]):
        if op=='Set':
            actual=instance.Set(key,value);valid=valid and actual is None
        elif op=='Get':
            actual=instance.Get(key);valid=valid and (actual is None or type(actual) is str)
        else:raise ValueError('Unknown cache operation')
        output.append(actual)
    return dict(actual=output,mutationOk=valid and json.dumps(args)==before)
''',''
    if language=='javascript':return code+'''
function executeCache(row){const args=row.arguments,before=JSON.stringify(args),[capacity,operations,keys,values]=args,instance=new LRUCache(capacity),output=[null];let valid=true;for(let i=1;i<operations.length;++i){let actual;if(operations[i]==='Set'){actual=instance.Set(keys[i],values[i]);valid=valid&&(actual===undefined||actual===null);if(actual===undefined)actual=null;}else if(operations[i]==='Get'){actual=instance.Get(keys[i]);valid=valid&&(actual===null||typeof actual==='string');}else throw new Error('Unknown cache operation');output.push(actual);}return {actual:output,mutationOk:valid&&JSON.stringify(args)===before};}
''',''
    if language=='csharp':return code,'''static object ExecuteCache(JsonElement row){var args=row.GetProperty("arguments");var operations=args[1];var keys=args[2];var values=args[3];var instance=new LRUCache(args[0].GetInt32());Func<int,string?> get=instance.Get;Action<int,string> set=instance.Set;var output=new List<object?>{null};for(int i=1;i<operations.GetArrayLength();++i){string op=operations[i].GetString()!;if(op=="Set"){set(keys[i].GetInt32(),values[i].GetString()!);output.Add(null);}else if(op=="Get")output.Add(get(keys[i].GetInt32()));else throw new Exception("Unknown cache operation");}return new {actual=output,mutationOk=true};}
'''
    if language=='java':return code,'''static JsonValue executeCache(JsonObject row){var args=row.get("arguments").asArray();var operations=args.get(1).asArray();var keys=args.get(2).asArray();var values=args.get(3).asArray();var instance=new LRUCache(args.get(0).asInt());try{if(LRUCache.class.getMethod("Get",int.class).getReturnType()!=String.class||LRUCache.class.getMethod("Set",int.class,String.class).getReturnType()!=void.class)throw new IllegalArgumentException("LRUCache result types must match the API");}catch(NoSuchMethodException error){throw new IllegalArgumentException("LRUCache methods must match the API",error);}var output=new JsonArray().add(Json.NULL);for(int i=1;i<operations.size();++i){String op=operations.get(i).asString();if(op.equals("Set")){instance.Set(keys.get(i).asInt(),values.get(i).asString());output.add(Json.NULL);}else if(op.equals("Get")){String value=instance.Get(keys.get(i).asInt());output.add(value==null?Json.NULL:Json.value(value));}else throw new RuntimeException("Unknown cache operation");}return new JsonObject().add("actual",output).add("mutationOk",true);}
'''
    return code+'''
#include <type_traits>
json executeCache(const json& row){const auto& args=row["arguments"];const auto& operations=args[1];const auto& keys=args[2];const auto& values=args[3];LRUCache instance(args[0].get<int>());static_assert(std::is_same<decltype(instance.Get(0)),std::optional<std::string>>::value,"Get must return optional<string>");static_assert(std::is_same<decltype(instance.Set(0,std::string{})),void>::value,"Set must return void");json output=json::array();output.push_back(nullptr);for(size_t i=1;i<operations.size();++i){auto op=operations[i].get<std::string>();if(op=="Set"){instance.Set(keys[i].get<int>(),values[i].get<std::string>());output.push_back(nullptr);}else if(op=="Get"){auto value=instance.Get(keys[i].get<int>());if(value)output.push_back(*value);else output.push_back(nullptr);}else throw std::runtime_error("Unknown cache operation");}return json{{"actual",output},{"mutationOk",true}};}
''',''


def attach(source,language,code):
    external,internal=parts(language,code)
    if language=='python':return source.replace('def execute(row):',external+"\ndef execute(row):\n    if row['ref']=='16.25': return executeCache(row)\n",1)
    if language=='javascript':return source.replace('function execute(row){',external+"\nfunction execute(row){if(row.ref==='16.25')return executeCache(row);",1)
    if language=='csharp':return source.replace('class Harness {',external+'\nclass Harness {\n'+internal,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="16.25")return ExecuteCache(row);',1)
    if language=='java':return source.replace('public class Harness {',external+'\npublic class Harness {\n'+internal,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("16.25"))return executeCache(row);',1)
    return source.replace('json execute(const json& row){',external+'\njson execute(const json& row){if(row["ref"]=="16.25")return executeCache(row);',1)
