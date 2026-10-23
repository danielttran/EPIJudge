"""Execute unsynchronized/wrong-gate workers and a valid surplus-permit alternative."""
import json,unittest
from algorithms15 import body
from chapter15 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus15 import valid_observation
from models15 import declare
from verify01 import execute
class OrderRuntimeTests(unittest.TestCase):
 def test_actual_workers(self):
  entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='15.5');spec=SPECS[0]
  for language in LANGUAGES:
   original=body('15.5',language)
   variants={'no-wait':'context.Work()' if language=='python' else 'context.Work();','wrong-gate':original.replace('context.Wait(role-1)','context.Wait(1)'), 'surplus-permit':original.replace('    context.Signal(role)','    context.Signal(role)\n    context.Signal(role)') if language=='python' else original.replace('if(role<2)context.Signal(role);','if(role<2){context.Signal(role);context.Signal(role);}')}
   for label,algorithm in variants.items():
    with self.subTest(language=language,variant=label):
     self.assertNotEqual(algorithm,original);config=entry['languages'][language];_,code=declare(spec,language,algorithm);cases=[dict(ref='15.5',arguments=[[2,1,0],1,[]],expected=[0,1,2])]
     filename=('Solution.' if language in ('java','csharp') else 'solution.')+EXT[language]
     rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-order15-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     self.assertEqual(valid_observation('15.5',cases[0],rows[0]['observation']),label=='surplus-permit')
if __name__=='__main__':unittest.main()
