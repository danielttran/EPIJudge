"""Wrong return types are rejected at actual compile/runtime boundaries in every language."""
import json,unittest
from algorithms15 import body
from chapter15 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus15 import valid_observation
from models15 import declare
from verify01 import execute
class WorkerReturnTests(unittest.TestCase):
 def test_wrong_worker_return_types(self):
  catalog=json.loads((ROOT/'ctci6/runtime/catalog.json').read_text())
  for spec in (s for s in SPECS if s['ref'] in ('15.3','15.5','15.7')):
   entry=next(e for e in catalog if e['ref']==spec['ref'])
   for language in LANGUAGES:
    with self.subTest(ref=spec['ref'],language=language):
     config=entry['languages'][language];algorithm=body(spec['ref'],language)+('\nreturn 42' if language=='python' else '\nreturn 42;');_,code=declare(spec,language,algorithm)
     if language in ('csharp','java','cpp'):code=code.replace('void '+spec['method'],'int '+spec['method'],1)
     cases=[dict(ref=spec['ref'],arguments=spec['example'][0],expected=spec['example'][1])];filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language];folder=ROOT/'.epi-runs/ctci6-worker-return15'/spec['ref']/language
     try:rows=execute(language,False,cases,folder,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
     except RuntimeError as error:
      self.assertIn(language,('csharp','cpp'));self.assertIn('CS0407' if language=='csharp' else 'must return void',str(error));(folder/'compile-rejection.txt').write_text(str(error));outcome='compile-rejected'
     else:
      self.assertNotIn(language,('csharp','cpp'));self.assertFalse(valid_observation(spec['ref'],cases[0],rows[0]['observation']));outcome='runtime-rejected'
     (folder/'audit-outcome.json').write_text(json.dumps(dict(ref=spec['ref'],language=language,status=outcome))+'\n')
if __name__=='__main__':unittest.main()
