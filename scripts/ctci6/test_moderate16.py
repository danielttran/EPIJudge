"""Counterexamples against common incorrect moderate-task interpretations."""
import unittest
from corpus16 import oracle,valid_observation

class ModerateContractTests(unittest.TestCase):
    def test_factorial_counts_repeated_factors_and_large_endpoint(self):
        self.assertEqual(6,oracle('16.5',[25]))
        self.assertEqual(31,oracle('16.5',[125]))
        self.assertEqual(536870902,oracle('16.5',[2147483647]))
        self.assertFalse(valid_observation('16.5',dict(expected=6),dict(actual=5,mutationOk=True)))
    def test_maximum_rejects_wrapped_difference_sign(self):
        self.assertEqual(2147483647,oracle('16.7',[-2147483648,2147483647]))
        self.assertFalse(valid_observation('16.7',dict(expected=2147483647),dict(actual=-2147483648,mutationOk=True)))
    def test_board_lengths_empty_and_duplicate_conventions(self):
        self.assertEqual([0],oracle('16.11',[0,2,5]))
        self.assertEqual([6],oracle('16.11',[3,2,2]))
        self.assertEqual([6,9,12,15],oracle('16.11',[3,2,5]))
        self.assertFalse(valid_observation('16.11',dict(expected=[6]),dict(actual=[6,6],mutationOk=True)))
    def test_hits_cannot_supply_pseudo_hits(self):
        self.assertEqual([1,1],oracle('16.15',['GGRR','RGBY']))
        self.assertEqual([4,0],oracle('16.15',['RRRR','RRRR']))
        self.assertFalse(valid_observation('16.15',dict(expected=[1,1]),dict(actual=[1,2],mutationOk=True)))
    def test_sort_window_and_mutation(self):
        self.assertEqual([-1,-1],oracle('16.16',[[]]))
        self.assertEqual([-1,-1],oracle('16.16',[[1,1,2]]))
        self.assertEqual([2,4],oracle('16.16',[[1,2,4,3,3,5]]))
        self.assertFalse(valid_observation('16.16',dict(expected=[2,4]),dict(actual=[2,4],mutationOk=False)))
    def test_contiguous_is_not_separated_and_empty_is_allowed(self):
        self.assertEqual(0,oracle('16.17',[[-5,-1]]))
        self.assertEqual(5,oracle('16.17',[[2,-8,3,-2,4,-10]]))
        self.assertFalse(valid_observation('16.17',dict(expected=5),dict(actual=9,mutationOk=True)))

if __name__=='__main__':unittest.main()
