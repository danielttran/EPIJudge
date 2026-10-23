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
    helper=ROOT/'scripts/ctci6/harness_tree04.py';report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    path.write_text(json.dumps(report,indent=2)+'\n')
