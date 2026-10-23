"""Use existing readonly typed-array observations and exact Boolean result types."""
import json
from core import ROOT
from models04 import TREE_REFS
from harness_tree04 import attach
from harness08_typed import source as typed_source

def source(language,starters=False,only_ref=None):
    value=typed_source(language,starters,only_ref,staging_name='staged04',exclude_refs=TREE_REFS,allow_empty=True)
    entries=json.loads((ROOT/'ctci6/staged04/catalog.json').read_text())
    if any(e['result']=='b' and (only_ref is None or e['ref']==only_ref) for e in entries):
        if language=='python':value=value.replace('valid=(',"valid=(type(actual) is bool) if kind=='b' else (",1)
        if language=='javascript':value=value.replace('const valid=',"const valid=kind==='b'?typeof actual==='boolean':",1)
        if language=='java':value=value.replace('if(value instanceof String v)','if(value instanceof Boolean v)return Json.value(v);if(value instanceof String v)',1)
    trees=[e for e in entries if e['ref'] in TREE_REFS and (only_ref is None or e['ref']==only_ref)]
    if trees:value=attach(value,language,trees,starters)
    return value
