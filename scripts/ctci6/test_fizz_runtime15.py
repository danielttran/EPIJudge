"""Compile actual missing waits/wrong ownership/handoffs and valid strided workers."""
import json,unittest
from algorithms_fizz15 import body
from chapter15 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_fizz15 import oracle,valid_observation
from models15 import declare
from verify01 import execute
class FizzRuntimeTests(unittest.TestCase):
 def test_actual_four_worker_variants(self):
  entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='15.7');spec=next(s for s in SPECS if s['ref']=='15.7')
  for language in LANGUAGES:
   original=body(language)
   missing_wait=original.replace('    context.Wait(role)\n','').replace('context.Wait(role);','')
   wrong_both=original.replace('return 3 if value%15==0','return 1 if value%15==0').replace('value%15===0?3','value%15===0?1').replace('value%15==0?3','value%15==0?1')
   wrong_handoff=original.replace('context.Signal(owner(value+1))','context.Signal(0)').replace('context.Signal(Owner(value+1))','context.Signal(0)').replace('context.Signal(owner.applyAsInt(value+1))','context.Signal(0)')
   strided=original.replace('for value in range(1,limit+1):','for value in range((1,3,5,15)[role],limit+1,(1,3,5,15)[role]):').replace('for(let value=1;value<=limit;++value)','for(let value=[1,3,5,15][role];value<=limit;value+=[1,3,5,15][role])')
   if language in ('cpp','csharp','java'):strided=strided.replace('for(int value=1;value<=limit;++value)',('int steps[4]={1,3,5,15};' if language=='cpp' else 'int[] steps={1,3,5,15};')+'for(int value=steps[role];value<=limit;value+=steps[role])')
   for label,algorithm in (('no-wait',missing_wait),('wrong-both-role',wrong_both),('wrong-handoff',wrong_handoff),('strided-values',strided)):
    with self.subTest(language=language,variant=label):
     self.assertNotEqual(original,algorithm);config=entry['languages'][language];_,code=declare(spec,language,algorithm);args=[30,[3,2,1,0],1,[]];cases=[dict(ref='15.7',arguments=args,expected=oracle('15.7',args))]
     filename=('Solution.' if language in ('java','csharp') else 'solution.')+EXT[language]
     rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-fizz15-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     self.assertEqual(valid_observation('15.7',cases[0],rows[0]['observation']),label=='strided-values')
if __name__=='__main__':unittest.main()
