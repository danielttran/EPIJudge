"""Lazy readonly inclusive-range stream with observable read/rewind limits."""
from models08 import header as base_header
from models_file10 import NUMBER_FILE

def parts(language,code):
    if language=='python':return code+'''
class JudgeNumberFile(NumberFile):
    def __init__(self,ranges,small):
        self.__ranges=tuple(tuple(pair) for pair in ranges)
        self.__index=0;self.__cursor=ranges[0][0] if ranges else 0
        self.reads=0;self.resets=0;self.__small=small
        self.__budget=(2 if small else 1)*(sum(end-start+1 for start,end in ranges)+1)
    def ReadNext(self):
        self.reads+=1
        if self.reads>self.__budget:raise RuntimeError('File read budget exceeded')
        if self.__index==len(self.__ranges):return -1
        value=self.__cursor;self.__cursor+=1
        if self.__cursor>self.__ranges[self.__index][1]:
            self.__index+=1
            if self.__index<len(self.__ranges):self.__cursor=self.__ranges[self.__index][0]
        return value
    def Reset(self):
        self.resets+=1
        if self.resets>(1 if self.__small else 0):raise RuntimeError('File reset budget exceeded')
        self.__index=0;self.__cursor=self.__ranges[0][0] if self.__ranges else 0
def executeFile(row):
    ranges,small=row['arguments'];provided=JudgeNumberFile(ranges,small);actual=FindMissingInt(provided,small)
    return dict(actual=actual,mutationOk=type(actual) is int and 0<=actual<=2147483647,reads=provided.reads,resets=provided.resets)
''',''
    if language=='javascript':return code+'''
class JudgeNumberFile extends NumberFile {#ranges;#index=0;#cursor;#small;#budget;constructor(ranges,small){super();this.#ranges=ranges.map(pair=>pair.slice());this.#cursor=ranges.length?ranges[0][0]:0;this.#small=small;this.#budget=(small?2:1)*(ranges.reduce((total,pair)=>total+pair[1]-pair[0]+1,0)+1);this.reads=0;this.resets=0;}ReadNext(){if(++this.reads>this.#budget)throw new Error('File read budget exceeded');if(this.#index===this.#ranges.length)return -1;const value=this.#cursor++;if(this.#cursor>this.#ranges[this.#index][1]){++this.#index;if(this.#index<this.#ranges.length)this.#cursor=this.#ranges[this.#index][0];}return value;}Reset(){if(++this.resets>(this.#small?1:0))throw new Error('File reset budget exceeded');this.#index=0;this.#cursor=this.#ranges.length?this.#ranges[0][0]:0;}}
function executeFile(row){const [ranges,small]=row.arguments,provided=new JudgeNumberFile(ranges,small),actual=FindMissingInt(provided,small);return {actual,mutationOk:Number.isInteger(actual)&&actual>=0&&actual<=2147483647,reads:provided.reads,resets:provided.resets};}
''',''
    if language=='csharp':return code+'''
sealed class JudgeNumberFile:NumberFile {private readonly int[][] ranges;private readonly bool small;private readonly long budget;private int index;private long cursor;public long Reads;public int Resets;public JudgeNumberFile(int[][] ranges,bool small){this.ranges=ranges.Select(pair=>pair.ToArray()).ToArray();this.small=small;budget=(small?2L:1L)*(ranges.Sum(pair=>(long)pair[1]-pair[0]+1)+1);cursor=ranges.Length==0?0:ranges[0][0];}public override int ReadNext(){if(++Reads>budget)throw new InvalidOperationException("File read budget exceeded");if(index==ranges.Length)return -1;int value=(int)cursor++;if(cursor>ranges[index][1]){index++;if(index<ranges.Length)cursor=ranges[index][0];}return value;}public override void Reset(){if(++Resets>(small?1:0))throw new InvalidOperationException("File reset budget exceeded");index=0;cursor=ranges.Length==0?0:ranges[0][0];}}
''','''static object ExecuteFile(JsonElement row){var args=row.GetProperty("arguments");bool small=args[1].GetBoolean();var provided=new JudgeNumberFile(JsonSerializer.Deserialize<int[][]>(args[0].GetRawText())!,small);int actual=new Solution_10_7().FindMissingInt(provided,small);return new {actual,mutationOk=actual>=0,reads=provided.Reads,resets=provided.Resets};}
'''
    if language=='java':return code+'''
class JudgeNumberFile extends NumberFile {private final int[][] ranges;private final boolean small;private final long budget;private int index;private long cursor;long reads;int resets;JudgeNumberFile(int[][] ranges,boolean small){this.ranges=new int[ranges.length][];long length=0;for(int i=0;i<ranges.length;++i){this.ranges[i]=ranges[i].clone();length+=(long)ranges[i][1]-ranges[i][0]+1;}this.small=small;budget=(small?2L:1L)*(length+1);cursor=ranges.length==0?0:ranges[0][0];}public int ReadNext(){if(++reads>budget)throw new IllegalStateException("File read budget exceeded");if(index==ranges.length)return -1;int value=(int)cursor++;if(cursor>ranges[index][1]){index++;if(index<ranges.length)cursor=ranges[index][0];}return value;}public void Reset(){if(++resets>(small?1:0))throw new IllegalStateException("File reset budget exceeded");index=0;cursor=ranges.length==0?0:ranges[0][0];}}
''','''static JsonValue executeFile(JsonObject row){var args=row.get("arguments").asArray();var raw=args.get(0).asArray();int[][] ranges=new int[raw.size()][];for(int i=0;i<ranges.length;++i)ranges[i]=integers(raw.get(i).asArray());boolean small=args.get(1).asBoolean();var provided=new JudgeNumberFile(ranges,small);int actual=new Solution_10_7().FindMissingInt(provided,small);return new JsonObject().add("actual",actual).add("mutationOk",actual>=0).add("reads",provided.reads).add("resets",provided.resets);}
'''
    return code+'''
class JudgeNumberFile:public NumberFile {const std::vector<std::vector<int>> ranges;bool small;size_t index=0;long long cursor,budget;public:long long reads=0;int resets=0;JudgeNumberFile(std::vector<std::vector<int>> ranges,bool small):ranges(std::move(ranges)),small(small){long long length=0;for(const auto& pair:this->ranges)length+=static_cast<long long>(pair[1])-pair[0]+1;budget=(small?2LL:1LL)*(length+1);cursor=this->ranges.empty()?0:this->ranges[0][0];}int ReadNext() override{if(++reads>budget)throw std::runtime_error("File read budget exceeded");if(index==ranges.size())return -1;int value=static_cast<int>(cursor++);if(cursor>ranges[index][1]){++index;if(index<ranges.size())cursor=ranges[index][0];}return value;}void Reset() override{if(++resets>(small?1:0))throw std::runtime_error("File reset budget exceeded");index=0;cursor=ranges.empty()?0:ranges[0][0];}};
json executeFile(const json& row){bool small=row["arguments"][1].get<bool>();JudgeNumberFile provided(row["arguments"][0].get<std::vector<std::vector<int>>>(),small);int actual=Solution_10_7().FindMissingInt(provided,small);return json{{"actual",actual},{"mutationOk",actual>=0},{"reads",provided.reads},{"resets",provided.resets}};}
''',''

def attach(value,language,entry,starters):
    plain=base_header('10.7',language)
    value=value.replace(plain,plain+NUMBER_FILE[language],1) if plain else NUMBER_FILE[language]+value
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_10_7',1)
    outside,inside=parts(language,code)
    if language=='python':return value.replace('def execute(row):',outside+"\ndef execute(row):\n    if row['ref']=='10.7': return executeFile(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',outside+'\nfunction execute(row){if(row.ref==="10.7")return executeFile(row);',1)
    if language=='csharp':return value.replace('class Harness {',outside+'\nclass Harness {\n'+inside,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="10.7")return ExecuteFile(row);',1)
    if language=='java':return value.replace('public class Harness {',outside+'\npublic class Harness {\n'+inside,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("10.7"))return executeFile(row);',1)
    return value.replace('json execute(const json& row){',outside+'\njson execute(const json& row){if(row["ref"]=="10.7")return executeFile(row);',1)
