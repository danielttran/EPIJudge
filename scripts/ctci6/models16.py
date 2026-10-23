"""Reuse established typed bindings; the moderate batch adds integer-array results."""
from models08 import declare as typed_declare, header as base_header, TYPES
from models08 import neutral as collection_neutral
import numeric
from core import starter_body
from models_rand16 import RAND5

def neutral(spec,language):
    if spec["result"]=="d":return "return 0.0" if language=="python" else "return 0.0;"
    if spec["result"]=="ad":return "return new double[0];" if language=="java" else "return []" if language=="python" else "return [];" if language in ("csharp","javascript") else "return {};"
    if spec['ref']=='16.25':
        if language=='python':return 'class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n    def Get(self, key: int) -> str | None:\n        return None\n    def Set(self, key: int, value: str) -> None:\n        pass\n'
        if language=='javascript':return 'class LRUCache {constructor(capacity){}Get(key){return null;}Set(key,value){}}'
        if language=='csharp':return 'public class LRUCache {public LRUCache(int capacity){}public string? Get(int key){return null;}public void Set(int key,string value){}}'
        if language=='java':return 'class LRUCache {public LRUCache(int capacity){}public String Get(int key){return null;}public void Set(int key,String value){}}'
        return '#include <optional>\nclass LRUCache {public:explicit LRUCache(int capacity){}std::optional<std::string> Get(int key){return std::nullopt;}void Set(int key,const std::string& value){}};'

    if spec['result'] in ('aai','strings'):return collection_neutral(spec,language)
    if spec['result']=='ai':
        return 'return new int[0];' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    return starter_body(spec,language)

for _language,_type in {'csharp':'long','java':'long','cpp':'long long','python':'int'}.items():TYPES[_language]['l']=_type

def header(ref,language):
    return base_header(ref,language)+(RAND5[language] if ref=='16.23' else '')+('#include <unordered_map>\n#include <unordered_set>\n' if language=='cpp' else '')

def declare(spec,language,body,class_name='Solution'):
    if spec['ref']=='16.25':
        signature={'python':'LRUCache(capacity: int); Get(key: int) -> str | None; Set(key: int, value: str) -> None','javascript':'new LRUCache(capacity); Get(key) -> string | null; Set(key, value)','cpp':'LRUCache(int capacity); std::optional<std::string> Get(int key); void Set(int key, const std::string& value)','csharp':'LRUCache(int capacity); string? Get(int key); void Set(int key, string value)','java':'LRUCache(int capacity); String Get(int key); void Set(int key, String value)'}[language]
        return signature,body
    return typed_declare(spec,language,body,class_name)
