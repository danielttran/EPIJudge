import unittest
from corpus_bits17 import oracle,valid_observation

class BitQueryContractTests(unittest.TestCase):
    def test_empty_and_arbitrary_input_order(self):
        self.assertEqual(0,oracle('17.4',[[]]));self.assertEqual(2,oracle('17.4',[[4,1,0,3]]))
    def test_probes_and_type_are_part_of_observation(self):
        case=dict(arguments=[[0,1,3]],expected=2)
        self.assertTrue(valid_observation('17.4',case,dict(actual=2,mutationOk=True,probes=7)))
        for actual in (dict(actual=2,mutationOk=True,probes=45),dict(actual=2,mutationOk=True,probes=-1),dict(actual=True,mutationOk=True,probes=1),dict(actual=2,mutationOk=False,probes=7)):
            self.assertFalse(valid_observation('17.4',case,actual))

if __name__=='__main__':unittest.main()
