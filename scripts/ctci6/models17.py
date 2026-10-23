"""Reuse established primitive/array bindings with a visible C++17 byte-copy include."""
from models08 import declare as typed_declare,header
from core import starter_body
from models08 import neutral as collection_neutral

def neutral(spec,language):
    if spec["result"] in ("aai","strings"):return collection_neutral(spec,language)
    if spec["result"]=="ai":
        return "return new int[0];" if language=="java" else "return []" if language=="python" else "return [];" if language in ("csharp","javascript") else "return {};"
    return starter_body(spec,language)

def declare(spec,language,body,class_name='Solution'):
    signature,code=typed_declare(spec,language,body,class_name)
    if language=='cpp' and spec['ref']=='17.1':code='#include <cstring>\n'+code
    if language=='cpp' and spec['ref'] in ('17.13','17.15','17.22','17.25'):code='#include <unordered_set>\n'+code
    if language=='cpp' and spec['ref'] in ('17.18','17.22','17.26'):code='#include <unordered_map>\n'+code
    return signature,code
