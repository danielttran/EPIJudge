import unittest
from corpus_numeric import oracle,valid_observation,allowed

class NumericContractTests(unittest.TestCase):
    def test_precedence_associativity_real_division(self):
        for expression,expected in [('8/4/2',1),('10-3*2',4),('1/2',0.5),('8/4*2',4),('1-3/2',-0.5)]:self.assertEqual(expected,oracle('16.26',[expression]))
    def test_calculator_finite_and_tolerance(self):
        case=dict(arguments=['1/3'],expected=1/3)
        for value in (float('nan'),float('inf'),True,0,1/3+0.00001):self.assertFalse(valid_observation('16.26',case,dict(actual=value,mutationOk=True)))
        self.assertTrue(valid_observation('16.26',case,dict(actual=1/3+0.0000005,mutationOk=True)))
    def test_invalid_input_is_not_admitted(self):
        self.assertFalse(allowed('1/0'));self.assertFalse(allowed('100*100*100*100'))
    def test_medians_are_actual_half_values_with_wide_sum(self):
        self.assertEqual([-2147483648,-0.5],oracle('17.20',[[-2147483648,2147483647]]))
        self.assertEqual([2147483647,2147483647],oracle('17.20',[[2147483647]*2]))
        case=dict(arguments=[[1,2]],expected=[1,1.5])
        for actual in ([1,1],[2,3],[True,1.5],[1],[1,float('nan')]):self.assertFalse(valid_observation('17.20',case,dict(actual=actual,mutationOk=True)))
        self.assertTrue(valid_observation('17.20',case,dict(actual=[1,1.5],mutationOk=True)))
    def test_mutation_rejected(self):
        self.assertFalse(valid_observation('17.20',dict(expected=[]),dict(actual=[],mutationOk=False)))

if __name__=='__main__':unittest.main()
