"""Execute clone-return and parent-mutation counterexamples in all five languages."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from chapter04 import SPECS
from models04 import declare
from verify01 import execute

class TreeIdentityRuntimeTests(unittest.TestCase):
    def test_cloned_successor_and_changed_parent_are_rejected(self):
        row=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='4.6')
        spec=next(e for e in SPECS if e['ref']=='4.6')
        case=dict(ref='4.6',arguments=[{'nodes':[[2,1,-1],[1,-1,-1]],'selected':1}])
        clone={'python':'return TreeNode(node.Parent.Data)','javascript':'return new TreeNode(node.Parent.Data);','csharp':'return new TreeNode(node!.Parent!.Data);','java':'return new TreeNode(node.Parent.Data);','cpp':'return new TreeNode(node->Parent->Data);'}
        mutate={'python':'parent = node.Parent\nnode.Parent = None\nreturn parent','javascript':'const parent=node.Parent;node.Parent=null;return parent;','csharp':'var parent=node!.Parent;node.Parent=null;return parent;','java':'TreeNode parent=node.Parent;node.Parent=null;return parent;','cpp':'auto parent=node->Parent;node->Parent=nullptr;return parent;'}
        for language in LANGUAGES:
            for kind,bodies in [('clone',clone),('parent',mutate)]:
                with self.subTest(language=language,kind=kind):
                    config=row['languages'][language];_,code=declare(spec,language,bodies[language])
                    filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                    observed=execute(language,False,[case],ROOT/'.epi-runs/ctci6-tree-identity-negative'/language/kind,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})[0]['observation']
                    self.assertNotIn('error',observed)
                    self.assertEqual(-2 if kind=='clone' else 0,observed['actual'])
                    self.assertEqual(kind=='clone',observed['mutationOk'])

if __name__=='__main__':unittest.main()
