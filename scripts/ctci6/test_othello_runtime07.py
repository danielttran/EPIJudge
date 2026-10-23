"""Compile wrong diagonal/pass rules against independently selected witness games."""
import json,unittest,textwrap
from algorithms_othello07 import body
from chapter07 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_othello07 import cases as build_cases,valid_observation
from models07 import declare
from verify01 import execute

def mutant(language,label):
 original=body(language)
 if label=='missing-diagonal':return original.replace('if dr==dc==0:continue','if (dr==0 and dc==0) or (dr!=0 and dc!=0):continue').replace('if(dr===0&&dc===0)continue','if((dr===0&&dc===0)||(dr!==0&&dc!==0))continue').replace('if(dr==0&&dc==0)continue','if((dr==0&&dc==0)||(dr!=0&&dc!=0))continue')
 return original.replace('turn=3-color if can_move(3-color) else color if can_move(color) else 0','turn=3-color').replace('turn=canMove(3-color)?3-color:canMove(color)?color:0','turn=3-color').replace('turn=CanMove(3-color)?3-color:CanMove(color)?color:0','turn=3-color').replace('turn=rules.canMove(3-color)?3-color:rules.canMove(color)?color:0','turn=3-color')
class OthelloRuntimeTests(unittest.TestCase):
 def test_real_diagonal_and_auto_pass_violations(self):
  entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='7.8');spec=next(s for s in SPECS if s['ref']=='7.8');all_cases=build_cases(spec)
  for label in ('missing-diagonal','missing-pass'):
   namespace={};exec('def wrong(size,actions):\n'+textwrap.indent(mutant('python',label),'    '),namespace)
   witness=next(case for case in all_cases if namespace['wrong'](*case['arguments'])!=case['expected'])
   for language in LANGUAGES:
    with self.subTest(language=language,variant=label):
     algorithm=mutant(language,label);self.assertNotEqual(algorithm,body(language));config=entry['languages'][language];_,code=declare(spec,language,algorithm)
     cases=[dict(ref='7.8',**witness)];filename=('Solution.' if language in ('java','csharp') else 'solution.')+EXT[language]
     rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-othello7-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     self.assertFalse(valid_observation('7.8',cases[0],rows[0]['observation']))
if __name__=='__main__':unittest.main()
