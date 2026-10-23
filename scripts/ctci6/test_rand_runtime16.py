"""Execute biased modulo plus genuinely different unbiased rejection schemes."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from chapter16 import SPECS
from models16 import declare
from corpus_rand16 import valid_observation
from verify01 import execute

class UniformSevenRuntimeTests(unittest.TestCase):
    def test_biased_modulo_rejected_and_higher_rejection_scheme_accepted(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='16.23');spec=next(e for e in SPECS if e['ref']=='16.23');case=dict(ref='16.23',arguments=[[4,4,0,0]],expected=0)
        for language in LANGUAGES:
            for kind in ('biased','alternative'):
                with self.subTest(language=language,kind=kind):
                    if kind=='biased':body='return (5*source.Next()+source.Next())%7' if language=='python' else 'return (5*source.Next()+source.Next())%7;'
                    elif language=='python':body='while True:\n    even = 2*source.Next()\n    second = source.Next()\n    if second != 4:\n        value = even+second%2\n        if value < 7:\n            return value'
                    elif language=='javascript':body='while(true){const even=2*source.Next(),second=source.Next();if(second!==4){const value=even+second%2;if(value<7)return value;}}'
                    else:body='while(true){int even=2*source.Next();int second=source.Next();if(second!=4){int value=even+second%2;if(value<7)return value;}}'
                    _,code=declare(spec,language,body);config=entry['languages'][language];filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                    observed=execute(language,False,[case],ROOT/'.epi-runs/ctci6-random-variants'/language/kind,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})[0]['observation']
                    if kind=='alternative':self.assertNotIn('error',observed)
                    self.assertEqual(kind=='alternative',valid_observation('16.23',case,observed))
    def test_three_draw_attempts_are_not_arbitrarily_forbidden(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='16.23');spec=next(e for e in SPECS if e['ref']=='16.23');config=entry['languages']['python']
        body='while True:\n    state = 25*source.Next()+5*source.Next()+source.Next()\n    if state < 119:\n        return state%7'
        _,code=declare(spec,'python',body);case=dict(ref='16.23',arguments=[[4,4,0,0]],expected=0)
        observed=execute('python',False,[case],ROOT/'.epi-runs/ctci6-random-variants/python/three-draw',source_builder=lambda *_:config['harness'],companion_files={'solution.py':config['prefix']+code})[0]['observation']
        self.assertNotIn('error',observed);self.assertTrue(valid_observation('16.23',case,observed))

if __name__=='__main__':unittest.main()
