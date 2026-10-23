"""Actual native temporary-file observation; no expected answers in child code."""
from models08 import header as base_header
from tail12 import EXTRA

def attach(value,language,entry,starters):
    plain=base_header('12.1',language)
    value=value.replace(plain,plain+EXTRA[language],1) if plain else EXTRA[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_12_1',1)
    inside=''
    if language=='python':
        outside=code+'''
import tempfile
from pathlib import Path
def executeTail12(row):
    lines,k=row['arguments']
    content=''.join(line+'\\n' for line in lines)
    with tempfile.TemporaryDirectory(prefix='epijudge-tail-') as directory:
        path=Path(directory)/'input.txt'
        path.write_text(content,encoding='ascii')
        actual=LastKLines(str(path),k)
        preserved=path.is_file() and path.read_text(encoding='ascii')==content
        valid=type(actual) is list and all(type(line) is str for line in actual)
        return dict(actual=actual,mutationOk=preserved and valid)
'''
        return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='12.1':return executeTail12(row)\n",1)
    if language=='javascript':
        outside=code+'''
function executeTail12(row){
const nativeFs=require('node:fs'),os=require('node:os'),path=require('node:path');
const directory=nativeFs.mkdtempSync(path.join(os.tmpdir(),'epijudge-tail-')),file=path.join(directory,'input.txt');
const content=row.arguments[0].map(line=>line+'\\n').join('');
try{nativeFs.writeFileSync(file,content,'ascii');const actual=LastKLines(file,row.arguments[1]);
return {actual,mutationOk:nativeFs.existsSync(file)&&nativeFs.readFileSync(file,'ascii')===content&&Array.isArray(actual)&&actual.every(line=>typeof line==='string')};}
finally{nativeFs.rmSync(directory,{recursive:true,force:true});}}
'''
        return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="12.1")return executeTail12(row);',1)
    if language=='csharp':
        outside=code
        inside='''static object ExecuteTail12(JsonElement row){
var args=row.GetProperty("arguments");string content=string.Concat(args[0].EnumerateArray().Select(line=>line.GetString()+"\\n"));string path=System.IO.Path.GetTempFileName();
try{System.IO.File.WriteAllText(path,content,new System.Text.UTF8Encoding(false));var actual=new Solution_12_1().LastKLines(path,args[1].GetInt32());return new {actual,mutationOk=actual is not null&&actual.All(line=>line is not null)&&System.IO.File.Exists(path)&&System.IO.File.ReadAllText(path)==content};}
finally{System.IO.File.Delete(path);}}
'''
        return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="12.1")return ExecuteTail12(row);',1)
    if language=='java':
        outside=code
        inside='''static JsonValue executeTail12(JsonObject row){
var args=row.get("arguments").asArray();StringBuilder content=new StringBuilder();for(JsonValue line:args.get(0).asArray())content.append(line.asString()).append('\\n');
java.nio.file.Path path=null;
try{path=java.nio.file.Files.createTempFile("epijudge-tail-",".txt");java.nio.file.Files.writeString(path,content.toString(),java.nio.charset.StandardCharsets.US_ASCII);var actual=new Solution_12_1().LastKLines(path.toString(),args.get(1).asInt());boolean valid=actual!=null&&actual.stream().allMatch(java.util.Objects::nonNull)&&java.nio.file.Files.isRegularFile(path)&&java.nio.file.Files.readString(path).equals(content.toString());return new JsonObject().add("actual",encode(actual)).add("mutationOk",valid);}
catch(java.io.IOException error){throw new java.io.UncheckedIOException(error);}
finally{if(path!=null)try{java.nio.file.Files.deleteIfExists(path);}catch(java.io.IOException error){throw new java.io.UncheckedIOException(error);}}}
'''
        return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("12.1"))return executeTail12(row);',1)
    outside=code+'''
#include <atomic>
#include <chrono>
struct TailCleanup12 {std::filesystem::path directory;~TailCleanup12(){std::error_code ignored;std::filesystem::remove_all(directory,ignored);}};
json executeTail12(const json& row){
auto lines=row["arguments"][0].get<std::vector<std::string>>();std::string content;for(const auto& line:lines)content+=line+"\\n";
static std::atomic<unsigned long long> serial{0};std::filesystem::path directory;
for(int attempt=0;attempt<128;++attempt){auto stamp=std::chrono::steady_clock::now().time_since_epoch().count();auto candidate=std::filesystem::path("epijudge-tail-"+std::to_string(stamp)+"-"+std::to_string(serial.fetch_add(1)));std::error_code error;if(std::filesystem::create_directory(candidate,error)){directory=candidate;break;}if(error)throw std::runtime_error("temporary directory creation failed: "+error.message());}
if(directory.empty())throw std::runtime_error("temporary directory collision limit reached");TailCleanup12 cleanup{directory};auto filePath=(directory/"input.txt").string();
{std::ofstream file(filePath,std::ios::binary);file<<content;if(!file)throw std::runtime_error("temporary file write failed");}
auto actual=Solution_12_1().LastKLines(filePath,row["arguments"][1].get<int>());
std::ifstream file(filePath,std::ios::binary);std::string after((std::istreambuf_iterator<char>(file)),std::istreambuf_iterator<char>());bool preserved=std::filesystem::is_regular_file(filePath)&&after==content;
return json{{"actual",actual},{"mutationOk",preserved}};}
'''
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="12.1")return executeTail12(row);',1)
