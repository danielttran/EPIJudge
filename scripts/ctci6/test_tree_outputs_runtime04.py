"""Actually execute wrong output structures and an alternative correct midpoint."""
import json
import unittest
from algorithms04 import body
from chapter04 import SPECS
from core import ROOT,LANGUAGES,EXT
from corpus04 import cases,valid_observation
from models04 import declare
from verify01 import execute

class TreeOutputExecutionTests(unittest.TestCase):
    def setUp(self):
        self.runtime={e['ref']:e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text())}
        self.specs={e['ref']:e for e in SPECS}
    def observe(self,ref,language,code,rows,label):
        config=self.runtime[ref]['languages'][language]
        _,source=declare(self.specs[ref],language,code)
        filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
        return [value['observation'] for value in execute(language,False,[dict(ref=row['ref'],arguments=row['arguments']) for row in rows],ROOT/'.epi-runs/ctci6-tree-output-negative'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+source+config['suffix']})]
    def test_depth_value_clones_are_rejected_in_every_language(self):
        case=dict(ref='4.3',arguments=[{'nodes':[[7,1,2],[7,-1,-1],[7,-1,-1]],'selected':0}],expected=[[0],[1,2]])
        for language in LANGUAGES:
            with self.subTest(language=language):
                code=body('4.3',language)
                new='DepthLink(TreeNode(node.Data))' if language=='python' else 'new DepthLink(new TreeNode(node->Data))' if language=='cpp' else 'new DepthLink(new TreeNode(node.Data))'
                old='DepthLink(node)' if language=='python' else 'new DepthLink(node)'
                self.assertIn(old,code);code=code.replace(old,new)
                observed=self.observe('4.3',language,code,[case],'cloned-depth-values')[0]
                self.assertNotIn('error',observed);self.assertEqual([[-2],[-2,-2]],observed['actual'])
                self.assertFalse(valid_observation('4.3',case,observed))
    def test_link_cycle_stops_and_is_rejected(self):
        case=dict(ref='4.3',arguments=[{'nodes':[[7,-1,-1]],'selected':0}],expected=[[0]])
        code=body('4.3','python');before,after=code.rsplit('return heads',1);code=before+'heads[0].Next = heads[0]\nreturn heads'+after
        observed=self.observe('4.3','python',code,[case],'link-cycle')[0]
        self.assertNotIn('error',observed);self.assertFalse(observed['mutationOk'])
    def test_alternative_lower_midpoint_passes_all_minimal_tree_cases(self):
        code=body('4.2','python').replace('middle = lower + (upper - lower) // 2','middle = lower + (upper - lower - 1) // 2')
        rows=[dict(ref='4.2',**case) for case in cases(self.specs['4.2'])]
        observed=self.observe('4.2','python',code,rows,'alternative-lower-midpoint')
        self.assertTrue(all(valid_observation('4.2',case,value) for case,value in zip(rows,observed)))

if __name__=='__main__':unittest.main()
