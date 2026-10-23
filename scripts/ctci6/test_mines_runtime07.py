"""Compile actual wrong flag and diagonal-count implementations in all five languages."""
import json,unittest
from algorithms_mines07 import body
from chapter07 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_mines07 import oracle,valid_observation
from models07 import declare
from verify01 import execute
class MinesRuntimeTests(unittest.TestCase):
 def test_flag_protection_and_diagonal_counts(self):
  entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='7.10');spec=next(s for s in SPECS if s['ref']=='7.10')
  fixtures=[[[[0,1],[0,0]],[[0,1,1],[0,1,0]]],[[[0,0],[0,1]],[[0,0,0]]]]
  for language in LANGUAGES:
   original=body(language)
   flagged=original.replace('kind==0 and visible[row][column]==9','kind==0 and visible[row][column] in (9,10)').replace('kind===0&&visible[row][column]===9','kind===0&&(visible[row][column]===9||visible[row][column]===10)').replace('kind==0&&visible[row][column]==9','kind==0&&(visible[row][column]==9||visible[row][column]==10)')
   diagonal=original.replace('for c in range(max(0,column-1),min(columns,column+2)))','for c in range(max(0,column-1),min(columns,column+2)) if r==row or c==column)').replace('number+=bombs[r][c]','if(r==row||c==column)number+=bombs[r][c]')
   for label,algorithm,index in (('flagged-reveal',flagged,0),('missing-diagonal',diagonal,1)):
    with self.subTest(language=language,variant=label):
     self.assertNotEqual(original,algorithm);config=entry['languages'][language];_,code=declare(spec,language,algorithm)
     cases=[dict(ref='7.10',arguments=fixtures[index],expected=oracle('7.10',fixtures[index]))]
     filename=('Solution.' if language in ('java','csharp') else 'solution.')+EXT[language]
     rows=execute(language,False,cases,ROOT/'.epi-runs/ctci6-mines7-variants'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     self.assertFalse(valid_observation('7.10',cases[0],rows[0]['observation']))
if __name__=='__main__':unittest.main()
