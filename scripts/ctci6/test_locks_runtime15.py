"""Execute transaction/order failures and a different valid closure-iteration order."""
import json,unittest
from algorithms_locks15 import body
from chapter15 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_locks15 import oracle,valid_observation
from models15 import declare
from verify01 import execute

# An independent transitive-closure iteration order still computes the same least reachability fixed point.
def reverse_closure(language,original):
 if language=='python':return original.replace('for middle in range(self._count):','for middle in range(self._count-1,-1,-1):')
 if language=='javascript':return original.replace('for(let middle=0;middle<this.count;++middle)','for(let middle=this.count-1;middle>=0;--middle)')
 return original.replace('for(int middle=0;middle<count;++middle)','for(int middle=count-1;middle>=0;--middle)')
class LocksRuntimeTests(unittest.TestCase):
 def test_native_factory_variants(self):
  entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='15.4');spec=next(s for s in SPECS if s['ref']=='15.4')
  for language in LANGUAGES:
   original=body(language)
   if language=='python':
    cycle='if any(reach[i][i] for i in range(self._count)):return False'
    skip=original.replace(cycle,'')
    commit=original.replace(cycle,'if any(reach[i][i] for i in range(self._count)):\n            self._orders[owner]=order.copy()\n            return False')
    order=original.replace('path[position]!=resource','False')
   elif language=='javascript':
    skip=original.replace('for(let i=0;i<this.count;++i)if(reach[i][i])return false;','')
    commit=original.replace('if(reach[i][i])return false;','if(reach[i][i]){this.orders[owner]=order.slice();return false;}')
    order=original.replace('path[position]!==resource','false')
   else:
    term='reach[i,i]' if language=='csharp' else 'reach[i][i]'
    skip=original.replace('for(int i=0;i<count;++i)if('+term+')return false;','')
    clone='order.ToArray()' if language=='csharp' else 'order.clone()' if language=='java' else 'order'
    commit=original.replace('if('+term+')return false;','if('+term+'){orders[owner]='+clone+';return false;}')
    order=original.replace('path[next[owner]]!=resource','false')
   fixtures={
    'admit-cycle':[2,[[0,0,1],[1,1,0]],[[0,0],[0,1],[1,1],[1,0]],[]],
    'commit-rejection':[3,[[0,0,1],[1,1,2],[0,2,1]],[[0,0],[0,1],[1,1],[1,2]],[]],
    'ignore-order':[3,[[0,0,1]],[[0,1],[0,0],[0,1]],[]],
    'reverse-closure':[3,[[0,2,0],[1,1,2],[2,0,1]],[[0,2],[0,0],[1,1],[1,2]],[]]}
   for label,algorithm in (('admit-cycle',skip),('commit-rejection',commit),('ignore-order',order),('reverse-closure',reverse_closure(language,original))):
    with self.subTest(language=language,variant=label):
     self.assertNotEqual(original,algorithm);config=entry['languages'][language];_,code=declare(spec,language,algorithm);args=fixtures[label];cases=[dict(ref='15.4',arguments=args,expected=oracle('15.4',args))]
     filename='DeadlockFreeLocks.java' if language=='java' else ('Solution.' if language=='csharp' else 'solution.')+EXT[language]
     rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-locks15-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     self.assertEqual(valid_observation('15.4',cases[0],rows[0]['observation']),label=='reverse-closure')
 def test_cpp_declare_requires_boolean_return(self):
  language='cpp';entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='15.4');config=entry['languages'][language];code=body(language).replace('bool Declare(', 'int Declare(',1);self.assertNotEqual(code,body(language));args=[1,[[0,0]],[[0,0]],[]];cases=[dict(ref='15.4',arguments=args,expected=oracle('15.4',args))];folder=ROOT/'.epi-runs/ctci6-locks15-variants/cpp/wrong-return'
  with self.assertRaises(RuntimeError) as caught:
   execute(language,False,cases,folder,source_builder=lambda *_:config['harness'],companion_files={'solution.cpp':config['prefix']+code+config['suffix']})
  self.assertIn('Declare must return bool',str(caught.exception));(folder/'compile-rejection.txt').write_text(str(caught.exception))
if __name__=='__main__':unittest.main()
