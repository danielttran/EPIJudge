"""Execute the actual generic class and both primitive instantiations."""
from chapter07 import SPECS
from corpus07 import cases,valid_observation
from generate07 import generate07
from harness07 import source
from verify08 import verify
if __name__=='__main__':
    verify(specs=SPECS,batch=7,generator=generate07,case_builder=cases,matcher=valid_observation,adapter=source)
    import json,hashlib
    from core import ROOT
    path=ROOT/'ctci6/staged07/validation.json';report=json.loads(path.read_text())
    for language in ('python','javascript','csharp','java','cpp'):
        helper=ROOT/'scripts/ctci6'/('harness_circular07_'+language+'.py');report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    path.write_text(json.dumps(report,indent=2)+'\n')
