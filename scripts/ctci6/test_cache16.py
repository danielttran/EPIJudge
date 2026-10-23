"""State, refresh, replacement and nullable-string cache contract regressions."""
import unittest
from corpus16 import cache_transcript,oracle,valid_observation

class CacheContractTests(unittest.TestCase):
    def test_get_refreshes_before_eviction(self):
        args=cache_transcript(2,[('Set',1,'A'),('Set',2,'B'),('Get',1,''),('Set',3,'C'),('Get',2,''),('Get',1,'')])
        self.assertEqual([None,None,None,'A',None,None,'A'],oracle('16.25',args))
    def test_replacement_refreshes_without_consuming_another_slot(self):
        args=cache_transcript(2,[('Set',1,'old'),('Set',2,'two'),('Set',1,'new'),('Set',3,'three'),('Get',1,''),('Get',2,'')])
        self.assertEqual([None,None,None,None,None,'new',None],oracle('16.25',args))
    def test_missing_and_stored_empty_are_distinct(self):
        args=cache_transcript(1,[('Set',7,''),('Get',7,''),('Get',8,'')])
        expected=[None,None,'',None]
        self.assertEqual(expected,oracle('16.25',args))
        self.assertFalse(valid_observation('16.25',dict(expected=expected),dict(actual=[None,None,None,None],mutationOk=True)))
        self.assertFalse(valid_observation('16.25',dict(expected=expected),dict(actual=[None,None,0,None],mutationOk=True)))
    def test_new_instances_do_not_inherit_prior_keys(self):
        self.assertEqual([None,None,'a'],oracle('16.25',cache_transcript(1,[('Set',1,'a'),('Get',1,'')])))
        self.assertEqual([None,None],oracle('16.25',cache_transcript(1,[('Get',1,'')])))

if __name__=='__main__':unittest.main()
