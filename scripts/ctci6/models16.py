"""Reuse established typed bindings; the moderate batch adds integer-array results."""
from models08 import declare, header as base_header, TYPES
from models08 import neutral as collection_neutral
from core import starter_body

def neutral(spec,language):
    if spec['result'] in ('aai','strings'):return collection_neutral(spec,language)
    if spec['result']=='ai':
        return 'return new int[0];' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    return starter_body(spec,language)

for _language,_type in {'csharp':'long','java':'long','cpp':'long long','python':'int'}.items():TYPES[_language]['l']=_type

def header(ref,language):
    return base_header(ref,language)+('#include <unordered_map>\n#include <unordered_set>\n' if language=='cpp' else '')
