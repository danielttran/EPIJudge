"""Counterexamples for noncanonical group representatives and exact lines."""
import unittest
from corpus_line16 import oracle as line_oracle, valid_observation as line_valid
from corpus_names17 import oracle as name_oracle, valid_observation as name_valid

class GroupLineTests(unittest.TestCase):
    def test_scaled_and_tied_lines_are_valid(self):
        args=[[[0,0],[1,1],[0,1]]];case=dict(arguments=args,expected=line_oracle('16.14',args))
        for actual in ([2,-2,0],[1,0,0],[0,1,-1]):
            self.assertTrue(line_valid('16.14',case,dict(actual=actual,mutationOk=True)))
        for actual in ([0,0,0],[1,1,99],[True,0,0]):
            self.assertFalse(line_valid('16.14',case,dict(actual=actual,mutationOk=True)))
    def test_duplicate_occurrences_count_and_near_parallel_is_not_collinear(self):
        args=[[[0,0],[1000,1],[999,1],[998,1]]];case=dict(arguments=args,expected=line_oracle('16.14',args))
        self.assertFalse(line_valid('16.14',case,dict(actual=[1,-1000,0],mutationOk=True)))
        args=[[[1,2]]*5+[[3,4],[5,6]]];case=dict(arguments=args,expected=line_oracle('16.14',args))
        self.assertTrue(line_valid('16.14',case,dict(actual=[1,-1,1],mutationOk=True)))
        self.assertFalse(line_valid('16.14',case,dict(actual=[1,0,-1],mutationOk=True)))
    def test_empty_and_single_point(self):
        for args,actual in (([[]],[]),([[[2,3]]],[0,1,-3])):
            self.assertTrue(line_valid('16.14',dict(arguments=args,expected=line_oracle('16.14',args)),dict(actual=actual,mutationOk=True)))
    def test_arbitrary_representatives_order_and_zero_groups(self):
        args=[['John','Jon','Johnny','Chris'],[10,3,0,0],[[0,1],[1,2],[1,0],[2,2]]]
        case=dict(arguments=args,expected=name_oracle('17.7',args))
        self.assertTrue(name_valid('17.7',case,dict(actual=[[3,0],[2,13]],mutationOk=True)))
        for actual in ([[0,13]],[[0,13],[1,13],[3,0]],[[0,26],[3,0]],[[4,13],[3,0]]):
            self.assertFalse(name_valid('17.7',case,dict(actual=actual,mutationOk=True)))
    def test_case_distinct_names_and_mutation(self):
        args=[['A','a'],[1,2],[]];case=dict(arguments=args,expected=name_oracle('17.7',args))
        self.assertFalse(name_valid('17.7',case,dict(actual=[[0,3]],mutationOk=True)))
        self.assertFalse(name_valid('17.7',case,dict(actual=[[0,1],[1,2]],mutationOk=False)))

if __name__=='__main__':unittest.main()
