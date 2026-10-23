"""Reuse the typed, expected-answer-free submission adapter."""
from harness08_typed import source as typed_source
from models08 import header as base_header
from models16 import header
import json
from core import ROOT
from numeric import adapt
from harness_rand16 import attach as attach_rand
from harness_cache16 import attach

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged16',exclude_refs=('16.25','16.23'),allow_empty=True)
    if language=='python':value=value.replace('else type(actual) is int and -2147483648<=actual<=2147483647', "else type(actual) is int and -1<=actual<=4294967295 if kind=='l' else type(actual) is int and -2147483648<=actual<=2147483647")
    if language=='javascript':value=value.replace(':Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647;', ":kind==='l'?Number.isSafeInteger(actual)&&actual>=-1&&actual<=4294967295:Number.isInteger(actual)&&actual>=-2147483648&&actual<=2147483647;")
    if language=='cpp':
        ref=only_ref or '8.4'
        value=value.replace(base_header(ref,language),header(ref,language),1)
    if language=='java':
        value=value.replace('if(value instanceof Integer v)return Json.value(v);','if(value instanceof Integer v)return Json.value(v);if(value instanceof Long v)return Json.value(v);')
    entries=json.loads((ROOT/'ctci6/staged16/catalog.json').read_text())
    kinds={e['result'] for e in entries if only_ref is None or e['ref']==only_ref}
    if 's' in kinds:
        if language=='python':value=value.replace('valid=(', "valid=(type(actual) is str) if kind=='s' else (",1)
        if language=='javascript':value=value.replace("const valid=kind==='strings'", "const valid=kind==='s'?typeof actual==='string':kind==='strings'",1)
    if 'b' in kinds:
        if language=='python':value=value.replace('valid=(', "valid=(type(actual) is bool) if kind=='b' else (",1)
        if language=='javascript':value=value.replace("const valid=", "const valid=kind==='b'?typeof actual==='boolean':",1)
        if language=='java':value=value.replace('if(value instanceof String v)', 'if(value instanceof Boolean v)return Json.value(v);if(value instanceof String v)',1)
    caches=[e for e in entries if e['ref']=='16.25' and (only_ref is None or only_ref==e['ref'])]
    if caches:
        cache=caches[0]
        value=attach(value,language,cache['languages'][language]['starterCode' if starters else 'solutionCode'])
    for entry in entries:
        if entry["ref"]=="16.23" and (only_ref is None or only_ref==entry["ref"]):value=attach_rand(value,language,entry,starters)
    kinds={e["result"] for e in entries if only_ref is None or e["ref"]==only_ref}
    return adapt(value,language,kinds)
