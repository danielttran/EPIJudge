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

if __name__=='__main__':unittest.main()
