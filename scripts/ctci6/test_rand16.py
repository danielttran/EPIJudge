import unittest
from fractions import Fraction
from collections import Counter
from corpus_rand16 import oracle,valid_observation

class UniformSevenTests(unittest.TestCase):
    def test_exact_accepted_preimages(self):
        counts=Counter(state%7 for state in range(21));self.assertEqual({i:3 for i in range(7)},dict(counts))
        self.assertEqual(Fraction(1,7),Fraction(3,25)/(1-Fraction(4,25)))
        biased=Counter(state%7 for state in range(25));self.assertEqual(4,biased[0]);self.assertEqual(3,biased[6])
    def test_reference_rejections_and_other_valid_mappings(self):
        self.assertEqual(0,oracle('16.23',[[4,4,0,0]]))
        case=dict(arguments=[[4,4,0,0]],expected=0)
        self.assertTrue(valid_observation('16.23',case,dict(actual=6,mutationOk=True,uniformOk=True)))
        for actual,uniform in ((7,True),(-1,True),(True,True),(0,False)):
            self.assertFalse(valid_observation('16.23',case,dict(actual=actual,mutationOk=True,uniformOk=uniform)))

if __name__=='__main__':unittest.main()
