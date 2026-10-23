"""Identity, duplicate-left ordering and exact downward/structural contracts."""
import unittest
from corpus04 import oracle,valid_observation,chain

class TreeContractTests(unittest.TestCase):
    def test_bst_duplicate_side_and_external_ancestors(self):
        self.assertTrue(oracle('4.5',[{'nodes':[[5,1,-1],[5,-1,-1]],'selected':0}]))
        self.assertFalse(oracle('4.5',[{'nodes':[[5,-1,1],[5,-1,-1]],'selected':0}]))
        self.assertFalse(oracle('4.5',[{'nodes':[[10,1,-1],[5,-1,2],[12,-1,-1]],'selected':0}]))
        self.assertTrue(oracle('4.5',[{'nodes':[[10,1,-1],[5,-1,2],[12,-1,-1]],'selected':1}]))
    def test_successor_is_original_node_even_when_values_equal(self):
        view={'nodes':[[5,1,-1],[5,-1,-1]],'selected':1}
        self.assertEqual(0,oracle('4.6',[view]))
        self.assertFalse(valid_observation('4.6',dict(expected=0),dict(actual=-2,mutationOk=True)))
    def test_ancestor_compares_identity_and_handles_other_components(self):
        view={'nodes':[[9,1,-1],[9,-1,-1],[9,-1,-1]],'selected':1}
        self.assertEqual(0,oracle('4.8',[view,0]))
        self.assertEqual(-1,oracle('4.8',[view,2]))
        self.assertEqual(1,oracle('4.8',[view,1]))
    def test_subtree_checks_null_positions_and_complete_integer_values(self):
        self.assertFalse(oracle('4.10',[{'nodes':[[12,-1,-1]],'selected':0},{'nodes':[[2,-1,-1]],'selected':0}]))
        self.assertFalse(oracle('4.10',[{'nodes':[[1,1,-1],[1,-1,-1]],'selected':0},{'nodes':[[1,-1,1],[1,-1,-1]],'selected':0}]))
        self.assertTrue(oracle('4.10',[{'nodes':[],'selected':-1},{'nodes':[],'selected':-1}]))
    def test_paths_count_nonempty_endpoints_without_crossing_siblings(self):
        self.assertEqual(6,oracle('4.12',[chain(3),0]))
        self.assertEqual(5,oracle('4.12',[{'nodes':[[0,1,2],[0,-1,-1],[0,-1,-1]],'selected':0},0]))
        self.assertEqual(0,oracle('4.12',[{'nodes':[],'selected':-1},0]))
    def test_balance_checks_all_descendants(self):
        self.assertFalse(oracle('4.4',[chain(1000)]))
        self.assertTrue(oracle('4.4',[{'nodes':[],'selected':-1}]))

if __name__=='__main__':unittest.main()
