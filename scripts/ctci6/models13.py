"""Readonly Country API; wire tuples are never passed to candidate code."""
from models08 import TYPES,declare as typed_declare,header as base_header
from core import starter_body
COUNTRY={
'csharp':'public sealed class Country {private readonly string name,continent;private readonly int population;public Country(string name,string continent,int population){this.name=name;this.continent=continent;this.population=population;}public string GetName()=>name;public string GetContinent()=>continent;public int GetPopulation()=>population;}\n',
'java':'final class Country {private final String name,continent;private final int population;public Country(String name,String continent,int population){this.name=name;this.continent=continent;this.population=population;}public String GetName(){return name;}public String GetContinent(){return continent;}public int GetPopulation(){return population;}}\n',
'cpp':'#include <numeric>\nclass Country {std::string name,continent;int population;public:Country(std::string name,std::string continent,int population):name(std::move(name)),continent(std::move(continent)),population(population){}const std::string& GetName()const{return name;}const std::string& GetContinent()const{return continent;}int GetPopulation()const{return population;}};\n',
'python':'class Country:\n    def __init__(self,name: str,continent: str,population: int):\n        self.__name,self.__continent,self.__population=name,continent,population\n    def GetName(self) -> str:\n        return self.__name\n    def GetContinent(self) -> str:\n        return self.__continent\n    def GetPopulation(self) -> int:\n        return self.__population\n',
'javascript':'class Country {#name;#continent;#population;constructor(name,continent,population){this.#name=name;this.#continent=continent;this.#population=population;}GetName(){return this.#name;}GetContinent(){return this.#continent;}GetPopulation(){return this.#population;}}\n'}
for lang,kind in {'csharp':'Country[]','java':'Country[]','cpp':'std::vector<Country>','python':'list[Country]'}.items():TYPES[lang]['countries']=kind

def declare(spec,language,body,class_name='Solution'):
    signature,code=typed_declare(spec,language,body,class_name)
    if language=='cpp':
        signature=signature.replace('std::vector<Country> countries','const std::vector<Country>& countries');code=code.replace('std::vector<Country> countries','const std::vector<Country>& countries')
    return signature,code
def header(ref,language):return base_header(ref,language)+COUNTRY[language]
def neutral(spec,language):return starter_body(spec,language)
