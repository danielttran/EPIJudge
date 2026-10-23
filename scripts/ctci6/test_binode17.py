import unittest
from corpus_binode17 import oracle,inserted,valid_observation

class BiNodeContractTests(unittest.TestCase):
    def test_original_inorder_identity_survives_duplicates(self):
        args=[inserted([2,1,2,3])];expected=oracle('17.12',args)
        self.assertEqual([1,0,2,3],expected['order']);self.assertEqual([-1,1,0,2],expected['previous']);self.assertEqual([0,2,3,-1],expected['next'])
        self.assertEqual([1,2,2,3],expected['values'])
    def test_clone_missing_backlinks_and_cycles_do_not_pass(self):
        args=[inserted([2,1,3])];case=dict(arguments=args,expected=oracle('17.12',args))
        for field,value in [('head',-2),('previous',[-1,-1,-1]),('cycle',True),('order',[1,2,0]),('values',[1,9,3])]:
            actual=dict(case['expected']);actual[field]=value
            self.assertFalse(valid_observation('17.12',case,dict(actual=actual,mutationOk=True)))
        self.assertFalse(valid_observation('17.12',case,dict(actual=case['expected'],mutationOk=False)))
    def test_empty_and_deep_chain(self):
        self.assertEqual(-1,oracle('17.12',[inserted([])])['head'])
        actual=oracle('17.12',[inserted(range(999,-1,-1))]);self.assertEqual(1000,len(actual['order']));self.assertEqual(999,actual['head']);self.assertEqual(list(range(1000)),actual['values'])

if __name__=='__main__':unittest.main()
