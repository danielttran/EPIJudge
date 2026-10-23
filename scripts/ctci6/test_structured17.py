"""Contract counterexamples for optimal towers, reconstructed text and sparse pairs."""
import unittest
from corpus17 import oracle,valid_observation

class StructuredHardContractTests(unittest.TestCase):
    def test_tower_requires_both_strict_dimensions_and_original_indices(self):
        args=[[[1,1],[1,2],[2,3]]];case=dict(arguments=args,expected=oracle('17.8',args))
        for actual in ([0,2],[1,2]):self.assertTrue(valid_observation('17.8',case,dict(actual=actual,mutationOk=True)))
        for actual in ([0,1,2],[2,1],[0,0]):self.assertFalse(valid_observation('17.8',case,dict(actual=actual,mutationOk=True)))
    def test_respace_returns_all_characters_with_minimum_unknown_cost(self):
        args=['abcd',['ab','abc','cd']];case=dict(arguments=args,expected=oracle('17.13',args))
        self.assertTrue(valid_observation('17.13',case,dict(actual=['ab','cd'],mutationOk=True)))
        self.assertFalse(valid_observation('17.13',case,dict(actual=['abc','d'],mutationOk=True)))
        self.assertFalse(valid_observation('17.13',case,dict(actual=['ab'],mutationOk=True)))
        unknown=dict(arguments=['xyz',[]],expected=['x','y','z'])
        self.assertTrue(valid_observation('17.13',unknown,dict(actual=['xyz'],mutationOk=True)))
        self.assertFalse(valid_observation('17.13',dict(arguments=['',[]],expected=[]),dict(actual=[''],mutationOk=True)))
    def test_word_transform_accepts_nonshortest_simple_valid_path(self):
        words=['aaa','aba','abb','aab','bab','bbb'];args=['aaa','bbb',words]
        case=dict(arguments=args,expected=oracle('17.22',args))
        self.assertTrue(valid_observation('17.22',case,dict(actual=words,mutationOk=True)))
        self.assertFalse(valid_observation('17.22',case,dict(actual=['aaa','bbb'],mutationOk=True)))
        self.assertFalse(valid_observation('17.22',case,dict(actual=['aaa','aab','aaa','aba','abb','bbb'],mutationOk=True)))
    def test_rectangle_accepts_equal_area_orientations_and_word_reuse(self):
        args=[['ab','a','b']];case=dict(arguments=args,expected=oracle('17.25',args))
        for actual in (['ab'],['a','b']):self.assertTrue(valid_observation('17.25',case,dict(actual=actual,mutationOk=True)))
        args=[['aa']];case=dict(arguments=args,expected=oracle('17.25',args))
        self.assertTrue(valid_observation('17.25',case,dict(actual=['aa','aa'],mutationOk=True)))
        self.assertFalse(valid_observation('17.25',case,dict(actual=['aa'],mutationOk=True)))
        self.assertFalse(valid_observation('17.25',dict(arguments=[['ab']],expected=[]),dict(actual=['ab'],mutationOk=True)))
    def test_similarity_reports_original_ids_and_actual_counts(self):
        args=[[20,10],[[1,2,3],[2,3,4]]];expected=[[10,20,2,4]]
        self.assertEqual(expected,oracle('17.26',args))
        case=dict(arguments=args,expected=expected)
        for actual in ([[0,1,2,4]],[[10,20,1,2]],[[20,10,2,4]]):self.assertFalse(valid_observation('17.26',case,dict(actual=actual,mutationOk=True)))
        self.assertEqual([],oracle('17.26',[[1,2],[[],[]]]))

if __name__=='__main__':unittest.main()
