"""Counterexamples for case normalization, wide differences and occurrence pairing."""
import unittest
from corpus16 import oracle,valid_observation

class ModeratePairContractTests(unittest.TestCase):
    def test_word_queries_share_counts_without_consuming_occurrences(self):
        args=[['A','a','AB'],['a','A','ab','B','a']]
        self.assertEqual([2,2,1,0,2],oracle('16.2',args))
        self.assertFalse(valid_observation('16.2',dict(expected=[2,2,1,0,2]),dict(actual=[1,1,0,0,1],mutationOk=True)))
    def test_difference_widens_before_subtracting_and_empty_is_not_zero(self):
        self.assertEqual(4294967295,oracle('16.6',[[-2147483648],[2147483647]]))
        self.assertEqual(-1,oracle('16.6',[[],[0]]))
        self.assertFalse(valid_observation('16.6',dict(expected=4294967295),dict(actual=1,mutationOk=True)))
    def test_sum_swap_uses_first_original_occurrence_and_no_wrapped_membership(self):
        self.assertEqual([4,6],oracle('16.21',[[4,1,2,1,1,2],[3,6,3,3]]))
        self.assertEqual([0,-2147483648],oracle('16.21',[[0],[-2147483648,-2147483648]]))
        self.assertEqual([],oracle('16.21',[[0],[-2147483648,2147483647,2147483647,2147483647,3]]))
        self.assertEqual([],oracle('16.21',[[],[]]))
        self.assertEqual([],oracle('16.21',[[0,1],[0,0]]))
    def test_pairs_consume_each_occurrence_and_keep_multiplicity(self):
        self.assertEqual([[2,2]],oracle('16.24',[[2,2,2],4]))
        self.assertEqual([[1,3],[1,3],[2,2]],oracle('16.24',[[1,1,2,2,3,3],4]))
        case=dict(expected=[[2,2]])
        for actual in ([[2,2],[2,2],[2,2]],[],[[True,3]]):
            self.assertFalse(valid_observation('16.24',case,dict(actual=actual,mutationOk=True)))
    def test_pair_sums_do_not_wrap_at_signed_endpoints(self):
        self.assertEqual([],oracle('16.24',[[2147483647,2147483647],-2]))
        self.assertEqual([[-2147483648,2147483647]],oracle('16.24',[[-2147483648,2147483647],-1]))

if __name__=='__main__':unittest.main()
