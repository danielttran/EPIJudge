"""Execute deterministic circular-wait, ownership/leak failures and descending-order alternative."""
import json,unittest
from algorithms_dining15 import body
from chapter15 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_dining15 import oracle,valid_observation
from models15 import declare
from verify01 import execute
class DiningRuntimeTests(unittest.TestCase):
 def test_actual_philosopher_variants(self):
  entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='15.3');spec=next(s for s in SPECS if s['ref']=='15.3')
  for language in LANGUAGES:
   original=body(language)
   no_forks='context.Eat()' if language=='python' else 'context.Eat();'
   leak=original.replace('    context.Drop(higher)\n','').replace('    context.Drop(lower)','').replace('context.Drop(higher);','').replace('context.Drop(lower);','')
   left_first=original.replace('lower,higher=min(left,right),max(left,right)','lower,higher=left,right').replace('lower=Math.min(left,right),higher=Math.max(left,right)','lower=left,higher=right').replace('lower=Math.Min(left,right),higher=Math.Max(left,right)','lower=left,higher=right').replace('lower=std::min(left,right),higher=std::max(left,right)','lower=left,higher=right')
   descending=original.replace('min(left,right)','temporary(left,right)').replace('max(left,right)','min(left,right)').replace('temporary(left,right)','max(left,right)').replace('Min(left,right)','Temporary(left,right)').replace('Max(left,right)','Min(left,right)').replace('Temporary(left,right)','Max(left,right)')
   for label,algorithm in (('no-forks',no_forks),('leaked-forks',leak),('circular-wait',left_first),('descending-order',descending)):
    with self.subTest(language=language,variant=label):
     self.assertNotEqual(original,algorithm);config=entry['languages'][language];_,code=declare(spec,language,algorithm);args=[3,1,[2,1,0],0,[]];cases=[dict(ref='15.3',arguments=args,expected=oracle('15.3',args))]
     filename=('Solution.' if language in ('java','csharp') else 'solution.')+EXT[language]
     rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-dining15-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     self.assertEqual(valid_observation('15.3',cases[0],rows[0]['observation']),label=='descending-order')
if __name__=='__main__':unittest.main()
