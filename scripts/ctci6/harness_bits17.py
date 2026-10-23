"""Opaque readonly bit-query decoding; observer contains no expected answers."""
from models08 import header as base_header
from models_bits17 import BITS

def parts(language,code):
    if language=='python':return code+'''
class JudgeBits(BitArray):
    def __init__(self,data):
        self.__data=tuple(data)
        self.probes=0
    def Size(self):return len(self.__data)
    def FetchBit(self,index,column):
        if type(index) is not int or type(column) is not int or not 0<=index<len(self.__data) or not 0<=column<32:raise RuntimeError('Invalid bit query')
        self.probes+=1
        if self.probes>4*len(self.__data)+32:raise RuntimeError('Bit query budget exceeded')
        return self.__data[index]>>column&1
def executeBits(row):
    provided=JudgeBits(row['arguments'][0]);actual=MissingNumberBits(provided)
    return dict(actual=actual,mutationOk=type(actual) is int and 0<=actual<=provided.Size(),probes=provided.probes)
''',''
    if language=='javascript':return code+'''
class JudgeBits extends BitArray {#data;constructor(data){super();this.#data=data.slice();this.probes=0;}Size(){return this.#data.length;}FetchBit(index,column){if(!Number.isInteger(index)||!Number.isInteger(column)||index<0||index>=this.#data.length||column<0||column>=32)throw new Error('Invalid bit query');if(++this.probes>4*this.#data.length+32)throw new Error('Bit query budget exceeded');return this.#data[index]>>>column&1;}}
function executeBits(row){const provided=new JudgeBits(row.arguments[0]),actual=MissingNumberBits(provided);return {actual,mutationOk:Number.isInteger(actual)&&actual>=0&&actual<=provided.Size(),probes:provided.probes};}
''',''
    if language=='csharp':return code+'''
sealed class JudgeBits:BitArray {private readonly int[] data;public int Probes;public JudgeBits(int[] values){data=(int[])values.Clone();}public override int Size()=>data.Length;public override int FetchBit(int index,int column){if(index<0||index>=data.Length||column<0||column>=32)throw new ArgumentException("Invalid bit query");if(++Probes>4*data.Length+32)throw new InvalidOperationException("Bit query budget exceeded");return data[index]>>column&1;}}
''','''static object ExecuteBits(JsonElement row){var provided=new JudgeBits(JsonSerializer.Deserialize<int[]>(row.GetProperty("arguments")[0].GetRawText())!);int actual=new Solution_17_4().MissingNumberBits(provided);return new {actual,mutationOk=actual>=0&&actual<=provided.Size(),probes=provided.Probes};}
'''
    if language=='java':return code+'''
class JudgeBits extends BitArray {private final int[] data;int probes;JudgeBits(int[] values){data=values.clone();}public int Size(){return data.length;}public int FetchBit(int index,int column){if(index<0||index>=data.length||column<0||column>=32)throw new IllegalArgumentException("Invalid bit query");if(++probes>4*data.length+32)throw new IllegalStateException("Bit query budget exceeded");return data[index]>>>column&1;}}
''','''static JsonValue executeBits(JsonObject row){var provided=new JudgeBits(integers(row.get("arguments").asArray().get(0).asArray()));int actual=new Solution_17_4().MissingNumberBits(provided);return new JsonObject().add("actual",actual).add("mutationOk",actual>=0&&actual<=provided.Size()).add("probes",provided.probes);}
'''
    return code+'''
class JudgeBits:public BitArray {const std::vector<int> data;public:int probes=0;explicit JudgeBits(const std::vector<int>& values):data(values){}int Size() override{return static_cast<int>(data.size());}int FetchBit(int index,int column) override{if(index<0||static_cast<size_t>(index)>=data.size()||column<0||column>=32)throw std::invalid_argument("Invalid bit query");if(++probes>4*Size()+32)throw std::runtime_error("Bit query budget exceeded");return data[index]>>column&1;}};
json executeBits(const json& row){JudgeBits provided(row["arguments"][0].get<std::vector<int>>());int actual=Solution_17_4().MissingNumberBits(provided);return json{{"actual",actual},{"mutationOk",actual>=0&&actual<=provided.Size()},{"probes",provided.probes}};}
''',''

def attach(value,language,entry,starters):
    plain=base_header('17.4',language)
    value=value.replace(plain,plain+BITS[language],1) if plain else BITS[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_17_4',1)
    outside,inside=parts(language,code)
    if language=='python':return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='17.4': return executeBits(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="17.4")return executeBits(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="17.4")return ExecuteBits(row);',1)
    if language=='java':return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("17.4"))return executeBits(row);',1)
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="17.4")return executeBits(row);',1)
