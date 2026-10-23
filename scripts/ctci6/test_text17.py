"""Disambiguating text-query and dictionary-composition contracts."""
import unittest
from corpus17 import oracle,valid_observation

class HardTextContractTests(unittest.TestCase):
    def test_distance_counts_index_steps_and_absence(self):
        self.assertEqual(1,oracle('17.11',[['a','b'],'a','b']))
        self.assertEqual(-1,oracle('17.11',[['a','x'],'a','b']))
        self.assertEqual(1,oracle('17.11',[['a','x','b','a'],'a','b']))
    def test_composed_word_requires_two_pieces_but_can_reuse_vocabulary(self):
        self.assertEqual('',oracle('17.15',[['cat','cat']]))
        self.assertEqual('catcat',oracle('17.15',[['cat','catcat']]))
        self.assertEqual('catdog',oracle('17.15',[['dogcat','cat','catdog','dog']]))
        self.assertFalse(valid_observation('17.15',dict(expected='catdog'),dict(actual='dogcat',mutationOk=True)))
    def test_multisearch_includes_overlaps_and_all_empty_boundaries(self):
        args=['aaa',['aa','','aa','aaaa']]
        expected=[[0,1],[0,1,2,3],[0,1],[]]
        self.assertEqual(expected,oracle('17.17',args))
        self.assertEqual([[0]],oracle('17.17',['',['']]))
        self.assertFalse(valid_observation('17.17',dict(expected=expected),dict(actual=[[0],[0,1,2],[0],[]],mutationOk=True)))
        self.assertFalse(valid_observation('17.17',dict(expected=[[0,1]]),dict(actual=[[False,True]],mutationOk=True)))

if __name__=='__main__':unittest.main()
