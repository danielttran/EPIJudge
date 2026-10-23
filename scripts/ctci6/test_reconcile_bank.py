"""Receipt correlation must tolerate numeric display, never fabricate equivalence."""
import unittest
from reconcile_bank import case_key

class ReceiptCaseTests(unittest.TestCase):
    def test_median_integer_spelling_matches_double_display(self):
        self.assertEqual(case_key(dict(arguments=[[5,1,9,2]],expected=[5,3,5,3.5])),case_key(dict(arguments=[[5,1,9,2]],expected=[5.0,3.0,5.0,3.5])))
    def test_boolean_is_not_number(self):
        self.assertNotEqual(case_key(dict(arguments=[],expected=False)),case_key(dict(arguments=[],expected=0)))
    def test_argument_numeric_types_are_not_rewritten(self):
        self.assertNotEqual(case_key(dict(arguments=[1],expected=0)),case_key(dict(arguments=[1.0],expected=0)))
    def test_exact_large_integers_do_not_round_together(self):
        self.assertNotEqual(case_key(dict(arguments=[],expected=10**40+1)),case_key(dict(arguments=[],expected=10**40+2)))
    def test_sequence_order_and_null_are_preserved(self):
        self.assertNotEqual(case_key(dict(arguments=[],expected=[1,2])),case_key(dict(arguments=[],expected=[2,1])))
        self.assertNotEqual(case_key(dict(arguments=[],expected=None)),case_key(dict(arguments=[],expected=[])))
if __name__=='__main__':unittest.main()
