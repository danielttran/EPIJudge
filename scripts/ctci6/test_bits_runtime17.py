"""Actually compile and reject invalid API access and excessive queries in all languages."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from chapter17 import SPECS
from models17 import declare
from verify01 import execute

class BitAccessRuntimeTests(unittest.TestCase):
    def test_invalid_column_index_and_linear_budget(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='17.4')
        spec=next(e for e in SPECS if e['ref']=='17.4')
        for language in LANGUAGES:
            with self.subTest(language=language):
                body='if numbers.Size() == 1:\n    return numbers.FetchBit(0,32)\nif numbers.Size() == 3:\n    return numbers.FetchBit(3,0)\nfor _ in range(4*numbers.Size()+33):\n    numbers.FetchBit(0,0)\nreturn 0' if language=='python' else 'if(numbers.Size()===1)return numbers.FetchBit(0,32);if(numbers.Size()===3)return numbers.FetchBit(3,0);for(let i=0;i<4*numbers.Size()+33;++i)numbers.FetchBit(0,0);return 0;' if language=='javascript' else 'if(numbers.Size()==1)return numbers.FetchBit(0,32);if(numbers.Size()==3)return numbers.FetchBit(3,0);for(int i=0;i<4*numbers.Size()+33;++i)numbers.FetchBit(0,0);return 0;'
                _,code=declare(spec,language,body);config=entry['languages'][language]
                filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                cases=[dict(ref='17.4',arguments=[list(range(n))]) for n in (1,3,2)]
                results=execute(language,False,cases,ROOT/'.epi-runs/ctci6-bit-api-negative'/language,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
                for index,row in enumerate(results):self.assertIn('invalid bit query' if index<2 else 'bit query budget',row['observation'].get('error','').lower())

if __name__=='__main__':unittest.main()
