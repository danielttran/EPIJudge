"""Reuse the typed, expected-answer-free submission adapter."""
from harness08_typed import source as typed_source
import json
from core import ROOT
from numeric import adapt
from harness_bits17 import attach
from harness_binode17 import attach as attach_binode

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged17',exclude_refs=('17.4','17.12'),allow_empty=True)
    entries=json.loads((ROOT/'ctci6/staged17/catalog.json').read_text())
    if any(e['result']=='s' and (only_ref is None or e['ref']==only_ref) for e in entries):
        if language=='python':value=value.replace('valid=(', "valid=(type(actual) is str) if kind=='s' else (",1)
        if language=='javascript':value=value.replace("const valid=kind==='strings'", "const valid=kind==='s'?typeof actual==='string':kind==='strings'",1)
    for entry in entries:
        if entry["ref"]=="17.4" and (only_ref is None or only_ref==entry["ref"]):value=attach(value,language,entry,starters)
    for entry in entries:
        if entry["ref"]=="17.12" and (only_ref is None or only_ref==entry["ref"]):value=attach_binode(value,language,entry,starters)
    kinds={e["result"] for e in entries if only_ref is None or e["ref"]==only_ref}
    return adapt(value,language,kinds)
