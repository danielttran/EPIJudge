"""Directed edges, empty routes and all valid topological orders."""
import unittest
from corpus04 import oracle,valid_observation

class GraphContractTests(unittest.TestCase):
    def test_directed_route_and_zero_edge_path(self):
        self.assertTrue(oracle('4.1',[2,[],1,1]))
        self.assertTrue(oracle('4.1',[2,[[0,1]],0,1]))
        self.assertFalse(oracle('4.1',[2,[[0,1]],1,0]))
        self.assertFalse(oracle('4.1',[3,[[0,1],[1,0],[1,1]],0,2]))
        self.assertFalse(valid_observation('4.1',dict(expected=True),dict(actual=1,mutationOk=True)))
    def test_topological_order_accepts_alternatives_and_preserves_direction(self):
        case=dict(arguments=[4,[[0,2],[1,2],[2,3]]],expected=[0,1,2,3])
        for actual in ([0,1,2,3],[1,0,2,3]):self.assertTrue(valid_observation('4.7',case,dict(actual=actual,mutationOk=True)))
        for actual in ([],[0,1,2],[0,0,2,3],[2,0,1,3],[0,1,2,4],[True,0,2,3]):self.assertFalse(valid_observation('4.7',case,dict(actual=actual,mutationOk=True)))
    def test_duplicate_dependencies_and_cycles_are_not_partial_orders(self):
        self.assertEqual([0,1],oracle('4.7',[2,[[0,1],[0,1]]]))
        self.assertEqual([],oracle('4.7',[3,[[0,1],[1,0]]]))
        self.assertEqual([],oracle('4.7',[1,[[0,0]]]))
        self.assertEqual([],oracle('4.7',[0,[]]))
        case=dict(arguments=[3,[[0,1],[1,0]]],expected=[])
        self.assertTrue(valid_observation('4.7',case,dict(actual=[],mutationOk=True)))
        self.assertFalse(valid_observation('4.7',case,dict(actual=[2],mutationOk=True)))

if __name__=='__main__':unittest.main()
