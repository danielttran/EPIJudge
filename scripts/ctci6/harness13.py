"""Decode real Country objects; compare actual readonly observations only."""
import json
from core import ROOT
from models08 import header as base_header
from models13 import header
from harness08_typed import source as typed_source

PARTS={
'python':r'''
def executeCountry13(row):
    countries=[Country(*record) for record in row['arguments'][0]]
    members=countries.copy()
    before=[(c.GetName(),c.GetContinent(),c.GetPopulation()) for c in countries]
    actual=PopulationByContinent(countries,row['arguments'][1])
    valid=type(actual) is int and -2147483648<=actual<=2147483647 and len(countries)==len(members) and all(a is b for a,b in zip(countries,members)) and [(c.GetName(),c.GetContinent(),c.GetPopulation()) for c in countries]==before
    return dict(actual=actual,mutationOk=valid)
''',
'javascript':r'''
function executeCountry13(row){const countries=row.arguments[0].map(record=>new Country(...record)),members=countries.slice(),before=JSON.stringify(countries.map(c=>[c.GetName(),c.GetContinent(),c.GetPopulation()]));const actual=PopulationByContinent(countries,row.arguments[1]);return {actual,mutationOk:Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647&&countries.length===members.length&&countries.every((c,i)=>c===members[i])&&JSON.stringify(countries.map(c=>[c.GetName(),c.GetContinent(),c.GetPopulation()]))===before};}
''',
'csharp':r'''
static object ExecuteCountry13(JsonElement row){var args=row.GetProperty("arguments");var countries=args[0].EnumerateArray().Select(r=>new Country(r[0].GetString()!,r[1].GetString()!,r[2].GetInt32())).ToArray();var members=countries.ToArray();var before=countries.Select(c=>(c.GetName(),c.GetContinent(),c.GetPopulation())).ToArray();int actual=new Solution_13_7().PopulationByContinent(countries,args[1].GetString()!);bool valid=countries.Length==members.Length&&countries.Select((c,i)=>ReferenceEquals(c,members[i])).All(v=>v)&&countries.Select(c=>(c.GetName(),c.GetContinent(),c.GetPopulation())).SequenceEqual(before);return new {actual,mutationOk=valid};}
''',
'java':r'''
static JsonValue executeCountry13(JsonObject row){var args=row.get("arguments").asArray();var records=args.get(0).asArray();var countries=new Country[records.size()];for(int i=0;i<countries.length;++i){var r=records.get(i).asArray();countries[i]=new Country(r.get(0).asString(),r.get(1).asString(),r.get(2).asInt());}var members=countries.clone();var before=new ArrayList<List<Object>>();for(var c:countries)before.add(List.of(c.GetName(),c.GetContinent(),c.GetPopulation()));int actual=new Solution_13_7().PopulationByContinent(countries,args.get(1).asString());boolean valid=Arrays.equals(countries,members);for(int i=0;i<countries.length;++i)valid&=List.of(countries[i].GetName(),countries[i].GetContinent(),countries[i].GetPopulation()).equals(before.get(i));return new JsonObject().add("actual",actual).add("mutationOk",valid);}
''',
'cpp':r'''
json executeCountry13(const json& row){std::vector<Country> countries;for(const auto& r:row["arguments"][0])countries.emplace_back(r[0].get<std::string>(),r[1].get<std::string>(),r[2].get<int>());const auto before=row["arguments"][0];int actual=Solution_13_7().PopulationByContinent(countries,row["arguments"][1].get<std::string>());auto after=json::array();for(const auto& c:countries)after.push_back(json::array({c.GetName(),c.GetContinent(),c.GetPopulation()}));return json{{"actual",actual},{"mutationOk",after==before}};}
'''}

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged13',exclude_refs=('13.7',),allow_empty=True)
    # Empty typed adapter uses the nonbasic header; replace its exact owned prefix.
    basic=base_header('8.2',language)
    if basic not in value:raise ValueError('Unknown empty typed header '+language)
    value=value.replace(basic,header('13.7',language),1)
    entry=next(e for e in json.loads((ROOT/'ctci6/staged13/catalog.json').read_text()) if e['ref']=='13.7')
    code=entry['languages'][language]['starterCode' if starters else 'solutionCode']
    if language not in ('python','javascript'):code=code.replace('class Solution','class Solution_13_7',1)
    part=PARTS[language]
    if language=='python':return value.replace('def execute(row):',code+part+"\ndef execute(row):\n    if row['ref']=='13.7':return executeCountry13(row)\n",1)
    if language=='javascript':return value.replace('function execute(row){',code+part+'\nfunction execute(row){if(row.ref==="13.7")return executeCountry13(row);',1)
    if language=='csharp':return value.replace('class Harness {',code+'\nclass Harness {\n'+part,1).replace('static object Execute(JsonElement row){','static object Execute(JsonElement row){if(row.GetProperty("ref").GetString()=="13.7")return ExecuteCountry13(row);',1)
    if language=='java':return value.replace('public class Harness {',code+'\npublic class Harness {\n'+part,1).replace('static JsonValue execute(JsonObject row){','static JsonValue execute(JsonObject row){if(row.get("ref").asString().equals("13.7"))return executeCountry13(row);',1)
    return value.replace('json execute(const json& row){',code+'\n'+part+'\njson execute(const json& row){if(row["ref"]=="13.7")return executeCountry13(row);',1)
