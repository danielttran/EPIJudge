"""Opaque API query limits, stream rank types, and duplicate occurrence semantics."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from corpus10 import oracle,valid_observation
from models10 import declare
from verify01 import execute

class ListyRankContractTests(unittest.TestCase):
    def test_listy_budget_and_any_duplicate_index(self):
        case=dict(arguments=[[1,1,2,4],1],expected=0)
        self.assertTrue(valid_observation('10.4',case,dict(actual=1,mutationOk=True,probes=4)))
        for probes in (-1,1000,True):self.assertFalse(valid_observation('10.4',case,dict(actual=1,mutationOk=True,probes=probes)))
        self.assertFalse(valid_observation('10.4',case,dict(actual=-1,mutationOk=True,probes=4)))
    def test_rank_counts_other_duplicates_and_rejects_insertion_rank(self):
        args=[['RankTracker','Track','Track','Track','Track','GetRank','GetRank'],[[],[5],[1],[4],[4],[4],[2]]]
        expected=[None,None,None,None,None,2,-1]
        self.assertEqual(expected,oracle('10.10',args))
        for actual in ([None,None,None,None,None,1,-1],[None,None,None,None,None,2,1]):
            self.assertFalse(valid_observation('10.10',dict(expected=expected),dict(actual=actual,mutationOk=True)))
    def test_repeat_sequence_keeps_every_later_encounter(self):
        args=[[8,1,8,8,32000,32000]]
        self.assertEqual([8,8,32000],oracle('10.8',args))
        self.assertFalse(valid_observation('10.8',dict(expected=[8,8,32000]),dict(actual=[8,32000],mutationOk=True)))
        self.assertFalse(valid_observation('10.8',dict(expected=[8,8,32000]),dict(actual=[32000,8,8],mutationOk=True)))

class ListyRankRuntimeTests(unittest.TestCase):
    def test_linear_search_exceeds_query_limit_in_every_language(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='10.4')
        spec=next(e for e in json.loads((ROOT/'ctci6/staged10/catalog.json').read_text()) if e['ref']=='10.4')
        for language in LANGUAGES:
            with self.subTest(language=language):
                body='index = 0\nwhile True:\n    value = values.ElementAt(index)\n    if value == -1:\n        return -1\n    if value == target:\n        return index\n    index += 1' if language=='python' else 'for(let index=0;;++index){const value=values.ElementAt(index);if(value===-1)return -1;if(value===target)return index;}' if language=='javascript' else 'for(int index=0;;++index){int value=values.ElementAt(index);if(value==-1)return -1;if(value==target)return index;}'
                _,code=declare(spec,language,body)
                config=entry['languages'][language]
                filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                observation=execute(language,False,[dict(ref='10.4',arguments=[list(range(1,10001)),10000])],ROOT/'.epi-runs/ctci6-listy-linear-negative'/language,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})[0]['observation']
                self.assertIn('query budget',observation.get('error','').lower())
    def test_python_boolean_rank_is_not_an_integer_rank(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='10.10')
        config=entry['languages']['python']
        code=config['prefix']+config['solutionCode']+'\nRankTracker.GetRank = lambda self,value: True\n'
        args=[['RankTracker','Track','Track','GetRank'],[[],[1],[2],[2]]]
        observation=execute('python',False,[dict(ref='10.10',arguments=args)],ROOT/'.epi-runs/ctci6-rank-bool-negative',source_builder=lambda *_:config['harness'],companion_files={'solution.py':code})[0]['observation']
        self.assertIs(True,observation['actual'][-1])
        self.assertFalse(observation['mutationOk'])

if __name__=='__main__':unittest.main()
