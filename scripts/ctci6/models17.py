"""Reuse established primitive/array bindings with a visible C++17 byte-copy include."""
from models08 import declare as typed_declare,header
from core import starter_body

def neutral(spec,language):
    if spec["result"]=="ai":
        return "return new int[0];" if language=="java" else "return []" if language=="python" else "return [];" if language in ("csharp","javascript") else "return {};"
    return starter_body(spec,language)

def declare(spec,language,body,class_name='Solution'):
    signature,code=typed_declare(spec,language,body,class_name)
    if language=='cpp' and spec['ref']=='17.1':code='#include <cstring>\n'+code
    if language=='cpp' and spec['ref']=='17.18':code='#include <unordered_map>\n'+code
    return signature,code
