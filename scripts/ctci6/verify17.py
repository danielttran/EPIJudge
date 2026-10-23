"""Reuse the existing standalone validation loop for the moderate batch."""
from chapter17 import SPECS
from corpus17 import valid_observation as base_match
import corpus_names17

import corpus_numeric
import corpus_bits17
import corpus_binode17

def valid_observation(reference,case,observed):return corpus_binode17.valid_observation(reference,case,observed) if reference=="17.12" else corpus_bits17.valid_observation(reference,case,observed) if reference=="17.4" else corpus_numeric.valid_observation(reference,case,observed) if reference=="17.20" else corpus_names17.valid_observation(reference,case,observed) if reference=="17.7" else base_match(reference,case,observed)
from generate17 import generate17,cases
from harness17 import source
from verify08 import verify

if __name__ == '__main__':
    verify(specs=SPECS,batch=17,generator=generate17,case_builder=cases,matcher=valid_observation,adapter=source)

    import json,hashlib
    from core import ROOT
    path=ROOT/'ctci6/staged17/validation.json';report=json.loads(path.read_text())
    helper=ROOT/'scripts/ctci6/corpus_names17.py';report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    helper=ROOT/'scripts/ctci6/corpus_numeric.py';report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    helper=ROOT/'scripts/ctci6/numeric.py';report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    for name in ('corpus_bits17.py','models_bits17.py','harness_bits17.py','corpus_binode17.py','models_binode17.py','harness_binode17.py'):
        helper=ROOT/'scripts/ctci6'/name;report['sourceHashes'][str(helper.relative_to(ROOT))]=hashlib.sha256(helper.read_bytes()).hexdigest()
    path.write_text(json.dumps(report,indent=2)+'\n')
