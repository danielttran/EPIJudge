from collections import Counter
from fractions import Fraction
from itertools import combinations,permutations
from math import comb,factorial
import unittest
from corpus_random17 import oracle,valid_observation

class RandomCollectionContractTests(unittest.TestCase):
    def test_subset_to_permutation_reduction_has_exact_uniform_weights(self):
        for n in range(6):
            for count in range(n+1):
                weights=Counter();mass=Fraction(1,comb(n,count)*factorial(count)*factorial(n-count))
                for selected in combinations(range(n),count):
                    remaining=[i for i in range(n) if i not in selected]
                    for first in permutations(selected):
                        for second in permutations(remaining):weights[first+second]+=mass
                self.assertEqual(factorial(n),len(weights));self.assertEqual({Fraction(1,factorial(n))},set(weights.values()))
    def test_duplicate_occurrences_require_weighted_value_probabilities(self):
        # For [7,7,9], choosing value 7 has two compatible one-index subsets.
        self.assertEqual(Fraction(1,6),Fraction(2,3)*Fraction(1,2)*Fraction(1,2))
        self.assertNotEqual(Fraction(1,6),Fraction(1,2)*Fraction(1,2)*Fraction(1,2))
        self.assertEqual(Fraction(1,6),Fraction(1,3)*Fraction(1,2))
    def test_output_order_is_free_but_counts_and_types_are_exact(self):
        case=dict(arguments=[[7,7,9],2],expected=[7,9])
        for actual in ([7,9],[9,7],[7,7]):self.assertTrue(valid_observation('17.3',case,dict(actual=actual,mutationOk=True,uniformOk=True)))
        for actual in ([9,9],[7],[True,9]):self.assertFalse(valid_observation('17.3',case,dict(actual=actual,mutationOk=True,uniformOk=True)))
        self.assertFalse(valid_observation('17.3',case,dict(actual=[7,9],mutationOk=True,uniformOk=False)))
    def test_shuffle_accepts_any_correct_occurrence_permutation(self):
        case=dict(arguments=[[1,1,2]],expected=[2,1,1])
        self.assertTrue(valid_observation('17.2',case,dict(actual=[1,2,1],mutationOk=True,uniformOk=True)))
        self.assertFalse(valid_observation('17.2',case,dict(actual=[1,2,2],mutationOk=True,uniformOk=True)))
    def test_examples_are_concrete_possible_outcomes(self):
        self.assertEqual([30,20,10],oracle('17.2',[[10,20,30]]));self.assertEqual([10,30],oracle('17.3',[[10,20,30,40],2]))

if __name__=='__main__':unittest.main()
