"""Property acceptance for minimal trees, original linked values and sequence order."""
import unittest
from corpus04 import minimal_valid,oracle,valid_observation

class TreeOutputContractTests(unittest.TestCase):
    def test_two_minimal_shapes_are_both_accepted(self):
        lower=dict(root=0,nodes=[[1,-1,1,-1],[2,-1,-1,0]])
        upper=dict(root=0,nodes=[[2,1,-1,-1],[1,-1,-1,0]])
        self.assertTrue(minimal_valid([1,2],lower));self.assertTrue(minimal_valid([1,2],upper))
    def test_bst_values_are_insufficient_without_minimum_height_and_parent_links(self):
        chain=dict(root=0,nodes=[[1,-1,1,-1],[2,-1,2,0],[3,-1,-1,1]])
        self.assertFalse(minimal_valid([1,2,3],chain))
        self.assertFalse(minimal_valid([1,2],dict(root=0,nodes=[[1,-1,1,-1],[2,-1,-1,-1]])))
        self.assertFalse(minimal_valid([1],dict(root=0,nodes=[[True,-1,-1,-1]])))
        self.assertFalse(minimal_valid([1],dict(root=0,nodes=[[1,0,-1,-1]])))
    def test_depths_preserve_original_identities_and_left_right_order(self):
        args=[{'nodes':[[7,1,2],[7,-1,-1],[7,-1,-1]],'selected':0}]
        expected=[[0],[1,2]]
        self.assertEqual(expected,oracle('4.3',args))
        for actual in ([[7],[7,7]],[[0],[2,1]],[[-2],[-2,-2]]):self.assertFalse(valid_observation('4.3',dict(expected=expected),dict(actual=actual,mutationOk=True)))
    def test_sequences_allow_outer_reordering_but_reject_duplicates_and_inner_reordering(self):
        case=dict(expected=[[2,1,3],[2,3,1]])
        self.assertTrue(valid_observation('4.9',case,dict(actual=[[2,3,1],[2,1,3]],mutationOk=True)))
        for actual in ([[2,1,3],[2,1,3],[2,3,1]],[[1,2,3],[2,3,1]]):self.assertFalse(valid_observation('4.9',case,dict(actual=actual,mutationOk=True)))
        self.assertEqual([[]],oracle('4.9',[{'nodes':[],'selected':-1}]))
        self.assertFalse(valid_observation('4.9',dict(expected=[[]]),dict(actual=[],mutationOk=True)))

if __name__=='__main__':unittest.main()
