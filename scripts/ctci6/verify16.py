"""Reuse the existing standalone validation loop for the moderate batch."""
from chapter16 import SPECS
from corpus16 import cases, valid_observation
from generate16 import generate16
from harness16 import source
from verify08 import verify
from core import ROOT
import json,hashlib

if __name__ == '__main__':
    verify(specs=SPECS,batch=16,generator=generate16,case_builder=cases,matcher=valid_observation,adapter=source)

    report_path=ROOT/'ctci6/staged16/validation.json'
    report=json.loads(report_path.read_text())
    helper=ROOT/'scripts/ctci6/harness_cache16.py'
    report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    report_path.write_text(json.dumps(report,indent=2)+'\n')
