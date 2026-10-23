"""Execute the graph batch through the established standalone loop."""
from chapter04 import SPECS
from corpus04 import cases,valid_observation
from generate04 import generate04
from harness04 import source
from verify08 import verify

if __name__=='__main__':
    verify(specs=SPECS,batch=4,generator=generate04,case_builder=cases,matcher=valid_observation,adapter=source)
    import json,hashlib
    from core import ROOT
    path=ROOT/'ctci6/staged04/validation.json';report=json.loads(path.read_text())
    for name in ('harness_tree04.py','harness_tree_outputs04.py','models_random04.py','algorithms_random04.py','corpus_random04.py','harness_random04.py','harness_random04_python.py','harness_random04_javascript.py','harness_random04_csharp.py','harness_random04_java.py','harness_random04_cpp.py','harness_random17.py','random_checker17.py','harness_rand16.py','models_random17.py'):
        helper=ROOT/'scripts/ctci6'/name;report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    for name in ('harness.py','harness.js','Harness.cs','Harness.java','harness.cpp'):
        helper=ROOT/'interviewcake/runtime'/name;report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    path.write_text(json.dumps(report,indent=2)+'\n')
