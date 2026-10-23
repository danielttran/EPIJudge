"""Counterexamples for the hard batch's explicit contracts and independent oracles."""
import unittest
from corpus17 import oracle,multiples,valid_observation

class HardContractTests(unittest.TestCase):
    def test_add_wraps_both_signed_boundaries(self):
        for args,expected in (([2147483647,1],-2147483648),([-2147483648,-1],2147483647),([-1,1],0),([-2147483648,-2147483648],0)):
            self.assertEqual(expected,oracle('17.1',args))
        self.assertFalse(valid_observation('17.1',dict(expected=-2147483648),dict(actual=2147483648,mutationOk=True)))
    def test_digit_oracle_agrees_with_direct_decimal_counting(self):
        total=0
        for n in range(501):
            total+=str(n).count('2')
            self.assertEqual(total,oracle('17.6',[n]))
        self.assertEqual(2071027783,oracle('17.6',[2147483647]))
        self.assertEqual(9,oracle('17.6',[25]))
    def test_multiple_index_and_deduplication(self):
        values=multiples()
        self.assertEqual((1,3,5,7,9,15,21,25,27),tuple(values[:9]))
        self.assertEqual(501,len(set(values)))
        self.assertEqual(284765625,values[500])
        self.assertLess(values[500]*7,2147483648)
    def test_majority_verification_and_minus_one_value(self):
        self.assertEqual([],oracle('17.10',[[1,2,3]]))
        self.assertEqual([],oracle('17.10',[[1,1,2,2]]))
        self.assertEqual([-1],oracle('17.10',[[-1,0,-1]]))
        self.assertFalse(valid_observation('17.10',dict(expected=[]),dict(actual=[3],mutationOk=True)))
    def test_appointments_are_not_independent_pairs(self):
        self.assertEqual(180,oracle('17.16',[[30,15,60,75,45,15,15,45]]))
        self.assertEqual(100,oracle('17.16',[[1,100,1]]))
        self.assertEqual(0,oracle('17.16',[[]]))
    def test_histogram_is_volume_not_container_area(self):
        self.assertEqual(7,oracle('17.21',[[3,0,2,0,4]]))
        self.assertEqual(0,oracle('17.21',[[1,2,3,4]]))
        self.assertEqual(999800000,oracle('17.21',[[100000]+[0]*9998+[100000]]))
        self.assertFalse(valid_observation('17.21',dict(expected=7),dict(actual=12,mutationOk=True)))


class RangeAndMatrixTests(unittest.TestCase):
    def test_balanced_window_returns_original_earliest_indices(self):
        self.assertEqual([0,3],oracle('17.5',['A1B2C']))
        self.assertEqual([-1,-1],oracle('17.5',['ABC']))
        self.assertFalse(valid_observation('17.5',dict(expected=[0,3]),dict(actual=[1,4],mutationOk=True)))
    def test_smallest_k_retains_duplicate_occurrences_and_endpoints(self):
        self.assertEqual([-2147483648,-2147483648],oracle('17.14',[[-2147483648,2147483647,-2147483648],2]))
        self.assertEqual([],oracle('17.14',[[3,2],0]))
        self.assertFalse(valid_observation('17.14',dict(expected=[1,1]),dict(actual=[1,2],mutationOk=True)))
    def test_covering_range_ignores_target_order_but_not_missing_values(self):
        self.assertEqual([1,3],oracle('17.18',[[7,5,9,1,5,9,1],[1,5,9]]))
        self.assertEqual([-1,-1],oracle('17.18',[[1,2],[3]]))
        self.assertEqual([-1,-1],oracle('17.18',[[1,2],[]]))
    def test_missing_two_is_not_one_missing_or_square_sum_overflow(self):
        self.assertEqual([1,2],oracle('17.19',[[]]))
        self.assertEqual([2,4],oracle('17.19',[[1,3,5]]))
        self.assertEqual([1,100000],oracle('17.19',[[v for v in range(2,100000)]]))
    def test_black_border_allows_white_interior_and_requires_full_edges(self):
        self.assertEqual([0,0,3],oracle('17.23',[[[0,0,0],[0,1,0],[0,0,0]]]))
        self.assertEqual([0,0,1],oracle('17.23',[[[0,1,0],[1,1,1],[0,1,0]]]))
        self.assertEqual([],oracle('17.23',[[[1,1],[1,1]]]))
    def test_submatrix_is_nonempty_and_obeys_tie_order(self):
        self.assertEqual([-2,0,1,0,1],oracle('17.24',[[[-5,-2]]]))
        self.assertEqual([12,0,1,1,2],oracle('17.24',[[[1,-2,3],[-4,5,6]]]))
        self.assertEqual([0,0,0,0,0],oracle('17.24',[[[0,0],[0,0]]]))
        self.assertFalse(valid_observation('17.24',dict(expected=[-2,0,1,0,1]),dict(actual=[0,0,0,0,0],mutationOk=True)))

if __name__=='__main__':unittest.main()
