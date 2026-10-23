"""Execute real workers, not simulated sorted answers."""
import hashlib,json
from chapter15 import SPECS
from core import ROOT,LANGUAGES
from corpus15 import cases,valid_observation
from generate15 import generate15
from harness15 import source
from verify08 import verify
if __name__=='__main__':
 verify(specs=SPECS,batch=15,generator=generate15,case_builder=cases,matcher=valid_observation,adapter=source)
 p=ROOT/'ctci6/staged15/validation.json';report=json.loads(p.read_text())
 for language in LANGUAGES:
  f=ROOT/'scripts/ctci6'/('harness_order15_'+language+'.py');report['sourceHashes'][str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
 for name in ('models_fizz15.py','algorithms_fizz15.py','corpus_fizz15.py'):
  f=ROOT/'scripts/ctci6'/name;report['sourceHashes'][str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
 for language in LANGUAGES:
  f=ROOT/'scripts/ctci6'/('harness_fizz15_'+language+'.py');report['sourceHashes'][str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
 p.write_text(json.dumps(report,indent=2)+'\n')
