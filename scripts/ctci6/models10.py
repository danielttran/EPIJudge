"""Existing bindings plus the explicit opaque Listy and RankTracker APIs."""
from models08 import declare as typed_declare,header as base_header,neutral as collection_neutral,TYPES
from core import starter_body
from models_file10 import NUMBER_FILE

LISTY={
 'csharp':'public abstract class Listy { public abstract int ElementAt(int index); }\n',
 'java':'abstract class Listy { public abstract int ElementAt(int index); }\n',
 'cpp':'class Listy { public: virtual int ElementAt(int index)=0; virtual ~Listy()=default; };\n',
 'python':'class Listy:\n    def ElementAt(self, index: int) -> int:\n        raise RuntimeError("Provided by the judge")\n',
 'javascript':'class Listy { ElementAt(index) { throw new Error("Provided by the judge"); } }\n'}
for _language in TYPES:TYPES[_language]['listy']='Listy&' if _language=='cpp' else 'Listy'

def header(ref,language):
    return base_header(ref,language)+(LISTY[language] if ref=='10.4' else NUMBER_FILE[language] if ref=='10.7' else '')

def declare(spec,language,body,class_name='Solution'):
    if spec['ref']=='10.10':
        signature='RankTracker(); Track(value: int) -> None; GetRank(value: int) -> int' if language=='python' else 'new RankTracker(); Track(value); GetRank(value)' if language=='javascript' else 'RankTracker(); void Track(int value); int GetRank(int value)'
        return signature,body
    return typed_declare(spec,language,body,class_name)

def neutral(spec,language):
    if spec['ref']=='10.10':
        if language=='python':return 'class RankTracker:\n    def __init__(self):\n        pass\n    def Track(self, value: int) -> None:\n        pass\n    def GetRank(self, value: int) -> int:\n        return -1\n'
        if language=='javascript':return 'class RankTracker { constructor(){} Track(value){} GetRank(value){return -1;} }'
        if language=='cpp':return 'class RankTracker {public:RankTracker()=default;void Track(int value){}int GetRank(int value){return -1;}};'
        return ('public class ' if language=='csharp' else 'class ')+'RankTracker {public RankTracker(){}public void Track(int value){}public int GetRank(int value){return -1;}}'
    if spec['result']=='ai':
        return 'return new int[0];' if language=='java' else 'return []' if language=='python' else 'return [];' if language in ('csharp','javascript') else 'return {};'
    if spec['result']=='strings':return collection_neutral(spec,language)
    return starter_body(spec,language)

import models_external10
_previous_external_header=header
_previous_external_neutral=neutral
def header(ref,language):
    if ref=='10.6':return base_header(ref,language)+models_external10.API[language]
    return _previous_external_header(ref,language)
def neutral(spec,language):
    if spec['ref']=='10.6':return 'return &inputFile;' if language=='cpp' else 'return inputFile' if language=='python' else 'return inputFile;'
    return _previous_external_neutral(spec,language)

_previous_tail_header=header
def header(ref,language):
    from tail12 import EXTRA
    return _previous_tail_header(ref,language)+(EXTRA[language] if ref=="12.1" else "")
