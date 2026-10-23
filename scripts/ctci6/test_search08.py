"""Negative contract tests for magic-index and row-sensitive queen grading."""
import unittest
from corpus08 import oracle, valid_observation

class SearchContractTests(unittest.TestCase):
    def test_magic_accepts_any_match_and_rejects_false_absence(self):
        case = dict(arguments=[[0, 1, 1, 3], False], expected=0)
        for value in (0, 1, 3):
            self.assertTrue(valid_observation('8.3', case, dict(actual=value, mutationOk=True)))
        for value in (-1, 2, 4, True, None):
            self.assertFalse(valid_observation('8.3', case, dict(actual=value, mutationOk=True)))
        self.assertFalse(valid_observation('8.3', case, dict(actual=0, mutationOk=False)))
        self.assertTrue(valid_observation('8.3', dict(arguments=[[], True]), dict(actual=-1, mutationOk=True)))

    def test_queens_outer_order_only_and_all_symmetries(self):
        boards = oracle('8.12', [])
        self.assertEqual(92, len(boards))
        case = dict(expected=boards)
        self.assertTrue(valid_observation('8.12', case, dict(actual=boards[::-1], mutationOk=True)))
        for value in ([sorted(board) for board in boards], boards[:-1], boards[:-1]+[boards[0]], [[True]*8]*92):
            self.assertFalse(valid_observation('8.12', case, dict(actual=value, mutationOk=True)))

    def test_boxes_strict_all_dimensions_and_no_rotation(self):
        for boxes in ([[[5,5,5],[5,4,4]]], [[[5,5,5],[4,5,4]]], [[[5,5,5],[4,4,5]]]):
            self.assertEqual(5, oracle('8.13', boxes))
        self.assertEqual(10, oracle('8.13', [[[10,1,10],[1,10,1]]]))
        self.assertEqual(78, oracle('8.13', [[[i,i,i] for i in range(1,13)]]))

    def test_boolean_groupings_not_precedence(self):
        self.assertEqual(1, oracle('8.14', ['1^0|1', True]))
        self.assertEqual(1, oracle('8.14', ['1^0|1', False]))
        self.assertEqual(0, oracle('8.14', ['', True]))
        self.assertEqual(208012, oracle('8.14', ['|'.join(['1']*13), True]))
        self.assertEqual(0, oracle('8.14', ['|'.join(['1']*13), False]))

if __name__ == '__main__':
    unittest.main()
