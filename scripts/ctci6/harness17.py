"""Reuse the typed, expected-answer-free submission adapter."""
from harness08_typed import source as typed_source
import json
from core import ROOT

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged17')
    entries=json.loads((ROOT/'ctci6/staged17/catalog.json').read_text())
    if any(e['result']=='s' and (only_ref is None or e['ref']==only_ref) for e in entries):
        if language=='python':value=value.replace('valid=(', "valid=(type(actual) is str) if kind=='s' else (",1)
        if language=='javascript':value=value.replace("const valid=kind==='strings'", "const valid=kind==='s'?typeof actual==='string':kind==='strings'",1)
    return value
