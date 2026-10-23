"""Reuse established primitive/array bindings with a visible C++17 byte-copy include."""
from models08 import declare as typed_declare,header as base_header
import numeric
from core import starter_body
from models_bits17 import BITS
from models_binode17 import BINODE
from models_random17 import RANDOM

def header(ref,language):return base_header(ref,language)+(BITS[language] if ref=="17.4" else BINODE[language] if ref=="17.12" else RANDOM[language] if ref in ("17.2","17.3") else "")
from models08 import neutral as collection_neutral

def neutral(spec,language):
    if spec["ref"]=="17.2":return "return" if language=="python" else "return;"
    if spec["ref"]=="17.12":return "return None" if language=="python" else "return nullptr;" if language=="cpp" else "return null;"
    if spec["result"]=="d":return "return 0.0" if language=="python" else "return 0.0;"
    if spec["result"]=="ad":return "return new double[0];" if language=="java" else "return []" if language=="python" else "return [];" if language in ("csharp","javascript") else "return {};"
    if spec["result"] in ("aai","strings"):return collection_neutral(spec,language)
    if spec["result"]=="ai":
        return "return new int[0];" if language=="java" else "return []" if language=="python" else "return [];" if language in ("csharp","javascript") else "return {};"
    return starter_body(spec,language)

def declare(spec,language,body,class_name='Solution'):
    signature,code=typed_declare(spec,language,body,class_name)
    if language=='cpp' and spec['ref']=='17.20':code='#include <queue>\n'+code
    if language=='cpp' and spec['ref']=='17.1':code='#include <cstring>\n'+code
    if language=='cpp' and spec['ref'] in ('17.13','17.15','17.22','17.25'):code='#include <unordered_set>\n'+code
    if language=='cpp' and spec['ref'] in ('17.18','17.22','17.26'):code='#include <unordered_map>\n'+code
    return signature,code
