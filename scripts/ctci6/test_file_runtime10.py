"""Compile actual read/rewind-budget violations in each supported language."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from chapter10 import SPECS
from models10 import declare
from verify01 import execute

class NumberFileRuntimeTests(unittest.TestCase):
    def test_sticky_eof_and_rewind_limits(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='10.7');spec=next(e for e in SPECS if e['ref']=='10.7')
        for language in LANGUAGES:
            with self.subTest(language=language):
                body='first = file.ReadNext()\nif smallMemory:\n    file.Reset()\n    file.Reset()\n    return 0\nif first == -1:\n    file.ReadNext()\n    return 0\nfile.Reset()\nreturn 0' if language=='python' else 'const first=file.ReadNext();if(smallMemory){file.Reset();file.Reset();return 0;}if(first===-1){file.ReadNext();return 0;}file.Reset();return 0;' if language=='javascript' else 'int first=file.ReadNext();if(smallMemory){file.Reset();file.Reset();return 0;}if(first==-1){file.ReadNext();return 0;}file.Reset();return 0;'
                _,code=declare(spec,language,body);config=entry['languages'][language];filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                cases=[dict(ref='10.7',arguments=args) for args in ([[],True],[[],False],[[[0,0]],False])]
                results=execute(language,False,cases,ROOT/'.epi-runs/ctci6-file-api-negative'/language,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
                for index,row in enumerate(results):self.assertIn('file read budget' if index==1 else 'file reset budget',row['observation'].get('error','').lower())

if __name__=='__main__':unittest.main()
