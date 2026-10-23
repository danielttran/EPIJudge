"""Execute five independently corrupted cache implementations without Get refresh."""
import json
import unittest
from algorithms16 import body
from core import ROOT,LANGUAGES,EXT
from corpus16 import cache_transcript,oracle,valid_observation
from verify01 import execute

class CacheRefreshExecutionTests(unittest.TestCase):
    def test_read_without_recency_refresh_fails_in_every_language(self):
        row=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='16.25')
        args=cache_transcript(2,[('Set',1,'A'),('Set',2,'B'),('Get',1,''),('Set',3,'C'),('Get',2,''),('Get',1,'')])
        case=dict(ref='16.25',arguments=args,expected=oracle('16.25',args))
        replacements={
          'python':('        self._entries.move_to_end(key)\n',''),
          'javascript':('this.entries.delete(key);this.entries.set(key,value);return value;','return value;'),
          'csharp':('order.Remove(node);order.AddLast(node);',''),
          'java':('(16,0.75f,true)','(16,0.75f,false)'),
          'cpp':('order.splice(order.end(),order,found->second);','')}
        for language in LANGUAGES:
            with self.subTest(language=language):
                code=body('16.25',language);old,new=replacements[language]
                self.assertIn(old,code);code=code.replace(old,new,1)
                config=row['languages'][language]
                filename='LRUCache.java' if language=='java' else ('Solution.' if language=='csharp' else 'solution.')+EXT[language]
                observed=execute(language,False,[case],ROOT/'.epi-runs/ctci6-cache-no-refresh'/language,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})[0]['observation']
                self.assertNotIn('error',observed)
                self.assertFalse(valid_observation('16.25',case,observed))

if __name__=='__main__':unittest.main()
