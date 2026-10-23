"""Actual five-language identity and backward-link counterexamples."""
import json
import unittest
from algorithms17 import body
from chapter17 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus_binode17 import inserted,oracle,valid_observation
from models17 import declare
from verify01 import execute

class BiNodeRuntimeTests(unittest.TestCase):
    def test_cloned_node_and_missing_previous_links_are_rejected(self):
        row=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='17.12');spec=next(e for e in SPECS if e['ref']=='17.12')
        args=[[inserted([3,1,4])],[inserted([2,1,3])]]
        cases=[dict(ref='17.12',arguments=a,expected=oracle('17.12',a)) for a in args]
        for language in LANGUAGES:
            with self.subTest(language=language):
                code=body('17.12',language)
                old,new=('node.Node1 = previous','node.Node1 = None') if language=='python' else ('node->Node1=previous','node->Node1=nullptr') if language=='cpp' else ('node.Node1=previous','node.Node1=null')
                self.assertIn(old,code);code=code.replace(old,new)
                clone='if root is not None and root.Data == 3:\n    return BiNode(root.Data)\n' if language=='python' else 'if(root!==null&&root.Data===3)return new BiNode(root.Data);' if language=='javascript' else 'if(root!=nullptr&&root->Data==3)return new BiNode(root->Data);' if language=='cpp' else 'if(root!=null&&root.Data==3)return new BiNode(root.Data);'
                _,code=declare(spec,language,clone+code);config=row['languages'][language]
                filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                results=execute(language,False,cases,ROOT/'.epi-runs/ctci6-binode-negative'/language,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})
                for case,result in zip(cases,results):
                    observed=result['observation'];self.assertNotIn('error',observed);self.assertFalse(valid_observation('17.12',case,observed))
                self.assertEqual(-2,results[0]['observation']['actual']['head'])
                self.assertEqual(cases[1]['expected']['order'],results[1]['observation']['actual']['order'])
                self.assertEqual([-1]*3,results[1]['observation']['actual']['previous'])

if __name__=='__main__':unittest.main()
