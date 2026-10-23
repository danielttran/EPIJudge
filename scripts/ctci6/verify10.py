"""Reuse the existing standalone validation loop for the moderate batch."""
from chapter10 import SPECS
from corpus10 import valid_observation as base_match
from corpus_external10 import valid_observation as external_match
from corpus_file10 import valid_observation as file_match
def valid_observation(reference,case,observed):return external_match(reference,case,observed) if reference=="10.6" else file_match(reference,case,observed) if reference=="10.7" else base_match(reference,case,observed)
from generate10 import generate10,cases
from harness10 import source
from verify08 import verify

if __name__ == '__main__':
    verify(specs=SPECS,batch=10,generator=generate10,case_builder=cases,matcher=valid_observation,adapter=source)

    import json,hashlib
    from core import ROOT
    path=ROOT/'ctci6/staged10/validation.json';report=json.loads(path.read_text())
    for name in ('models_file10.py','harness_file10.py','corpus_file10.py'):
        helper=ROOT/'scripts/ctci6'/name;report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    for name in ('models_external10.py','algorithms_external10.py','corpus_external10.py','harness_external10.py')+tuple('harness_external10_'+language+'.py' for language in ('python','javascript','csharp','java','cpp')):
        helper=ROOT/'scripts/ctci6'/name;report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    path.write_text(json.dumps(report,indent=2)+'\n')
