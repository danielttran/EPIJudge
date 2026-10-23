import unittest
from corpus_file10 import oracle,valid_observation

class MissingFileContractTests(unittest.TestCase):
    def test_interval_oracle_does_not_expand_duplicates_or_limits(self):
        self.assertEqual(8,oracle('10.7',[[[0,7],[0,7],[2147483647,2147483647]],False]))
        self.assertEqual(1048576,oracle('10.7',[[[0,1048575]],True]))
    def test_any_absent_integer_is_accepted_not_just_the_first(self):
        case=dict(arguments=[[[0,2],[4,4]],True],expected=3)
        for value in (3,5,2147483647):self.assertTrue(valid_observation('10.7',case,dict(actual=value,mutationOk=True,reads=10,resets=1)))
        for value in (0,2,4,-1,2147483648,True):self.assertFalse(valid_observation('10.7',case,dict(actual=value,mutationOk=True,reads=10,resets=1)))
    def test_pass_and_rewind_budgets_are_mode_specific(self):
        case=dict(arguments=[[[0,2]],False],expected=3)
        for reads,resets in ((5,0),(4,1),(-1,0)):
            self.assertFalse(valid_observation('10.7',case,dict(actual=3,mutationOk=True,reads=reads,resets=resets)))
        self.assertTrue(valid_observation('10.7',case,dict(actual=3,mutationOk=True,reads=4,resets=0)))

if __name__=='__main__':unittest.main()
