"""Run actual functional aggregation implementations and neutral starters."""
from chapter13 import SPECS
from corpus13 import cases,valid_observation
from generate13 import generate13
from harness13 import source
from verify08 import verify
if __name__=='__main__':
    verify(specs=SPECS,batch=13,generator=generate13,case_builder=cases,matcher=valid_observation,adapter=source)
    import json,hashlib
    from core import ROOT
    path=ROOT/'ctci6/staged13/validation.json';report=json.loads(path.read_text())
    names=['corpus_subset13.py','harness_subset13.py','harness_rand16.py','models_rand16.py']+['harness_subset13_'+language+'.py' for language in ('python','javascript','csharp','java','cpp')]
    inputs=[ROOT/'scripts/ctci6'/name for name in names]+[ROOT/'interviewcake/runtime'/name for name in ('harness.py','harness.js','Harness.cs','Harness.java','harness.cpp')]
    for helper in inputs:report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    path.write_text(json.dumps(report,indent=2)+'\n')
