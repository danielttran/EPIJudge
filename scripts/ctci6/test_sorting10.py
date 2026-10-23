"""Nonunique results and executed array-preservation counterexamples."""
import json
import unittest
from core import ROOT,LANGUAGES,EXT
from corpus10 import valid_observation
from models10 import declare
from algorithms10 import body
from verify01 import execute

class SortingContractTests(unittest.TestCase):
    def test_anagram_group_order_is_free_but_fragmentation_is_not(self):
        case=dict(arguments=[['ab','x','ba','ab','']])
        self.assertTrue(valid_observation('10.2',case,dict(actual=['ba','ab','ab','','x'],mutationOk=True)))
        for values in (['ab','x','ba','ab',''],['ab','ba','x',''],['ab','ba','ab','x',None]):
            self.assertFalse(valid_observation('10.2',case,dict(actual=values,mutationOk=True)))
    def test_duplicate_index_and_empty_target_conventions(self):
        case=dict(arguments=[[1,1,2,1],1],expected=0)
        for index in (0,1,3):self.assertTrue(valid_observation('10.3',case,dict(actual=index,mutationOk=True)))
        for index in (-1,2,4,True):self.assertFalse(valid_observation('10.3',case,dict(actual=index,mutationOk=True)))
        gaps=dict(arguments=[['','a'],''],expected=-1)
        self.assertFalse(valid_observation('10.5',gaps,dict(actual=0,mutationOk=True)))
    def test_matrix_coordinate_and_peak_properties(self):
        case=dict(arguments=[[[1,1],[1,2]],1],expected=[0,0])
        self.assertTrue(valid_observation('10.9',case,dict(actual=[1,0],mutationOk=True)))
        self.assertFalse(valid_observation('10.9',case,dict(actual=[-1,-1],mutationOk=True)))
        peaks=dict(arguments=[[3,1,2]])
        self.assertTrue(valid_observation('10.11',peaks,dict(actual=[2,3,1],mutationOk=True)))
        for values in ([3,1,2],[1,9,2]):self.assertFalse(valid_observation('10.11',peaks,dict(actual=values,mutationOk=True)))

class ArrayObservationRuntimeTests(unittest.TestCase):
    def test_copy_only_and_readonly_array_mutations_fail_in_every_language(self):
        entry=next(e for e in json.loads((ROOT/'ctci6/runtime/catalog.json').read_text()) if e['ref']=='10.1')
        spec=next(e for e in json.loads((ROOT/'ctci6/staged10/catalog.json').read_text()) if e['ref']=='10.1')
        clones={'csharp':'first=(int[])first.Clone();\n','java':'first=first.clone();\n','python':'first = first.copy()\n','javascript':'first=first.slice();\n'}
        readonly={'csharp':'second[0]=123456789;','java':'second[0]=123456789;','python':'second[0] = 123456789\n','javascript':'second[0]=123456789;','cpp':'const_cast<std::vector<int>&>(second)[0]=123456789;'}
        import re
        for language in LANGUAGES:
            correct=body('10.1',language)
            copy_only=clones[language]+correct if language!='cpp' else 'auto copy=first;\n'+re.sub(r'\bfirst\b','copy',correct)
            wrong_second=correct.replace('return first' if language=='python' else 'return first;',readonly[language]+('return first' if language=='python' else 'return first;'))
            for label,algorithm in (('copy-only',copy_only),('readonly-second',wrong_second)):
                with self.subTest(language=language,violation=label):
                    _,code=declare(spec,language,algorithm)
                    config=entry['languages'][language]
                    filename=('Solution.' if language in ('csharp','java') else 'solution.')+EXT[language]
                    observation=execute(language,False,[dict(ref='10.1',arguments=[[1,4,7,99,99],3,[2,6]])],ROOT/'.epi-runs/ctci6-array-negative'/language/label,source_builder=lambda *_:config['harness'],companion_files={filename:config['prefix']+code+config['suffix']})[0]['observation']
                    self.assertEqual([1,2,4,6,7],observation['actual'])
                    self.assertFalse(observation['mutationOk'])

if __name__=='__main__':unittest.main()
