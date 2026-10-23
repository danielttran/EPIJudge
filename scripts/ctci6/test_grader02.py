"""Regression checks for identity-sensitive and any-valid-answer grading."""

import copy
import unittest

from corpus02 import valid_observation


def observation(before, *, returned=None, boolean=None, ids=(), values=(), after=None):
    return dict(
        before=before,
        after=copy.deepcopy(before) if after is None else after,
        returnedId=returned,
        returnedBool=boolean,
        reachableIds=list(ids),
        reachableValues=list(values),
        cycle=False,
    )


class ListGraderTests(unittest.TestCase):
    def test_observation_must_describe_the_declared_input_graph(self):
        case = dict(arguments=[[7, 7], 1], expected=1)
        value = observation([[9, 1], [7, None]], returned=1)
        self.assertFalse(valid_observation("2.2", case, value))

    def test_partition_accepts_an_unstable_valid_order(self):
        case = dict(arguments=[[5, 1, 4, 2], 4], expected=[1, 2, 5, 4])
        value = observation(
            [[5, 1], [1, 2], [4, 3], [2, None]],
            returned=3,
            ids=[3, 1, 2, 0],
            values=[2, 1, 4, 5],
            after=[[5, None], [1, 2], [4, 0], [2, 1]],
        )
        self.assertTrue(valid_observation("2.4", case, value))
        value["reachableIds"] = [3, 1, 2, 2]
        self.assertFalse(valid_observation("2.4", case, value))

    def test_partition_rejects_equal_pivot_before_smaller_value(self):
        case = dict(arguments=[[4, 1], 4], expected=[1, 4])
        value = observation([[4, 1], [1, None]], returned=0, ids=[0, 1], values=[4, 1])
        self.assertFalse(valid_observation("2.4", case, value))

    def test_kth_rejects_a_copy_and_equal_payload_wrong_identity(self):
        case = dict(arguments=[[7, 7], 1], expected=1)
        value = observation([[7, 1], [7, None]], returned=1)
        self.assertTrue(valid_observation("2.2", case, value))
        for wrong in (0, 2):
            value["returnedId"] = wrong
            self.assertFalse(valid_observation("2.2", case, value))

    def test_delete_preserves_the_bypassed_successor_alias(self):
        before = [[8, 1], [4, 2], [7, 3], [2, None]]
        case = dict(
            arguments=[[8, 4, 7, 2], 1], expected=dict(success=True, values=[8, 7, 2])
        )
        value = observation(
            before,
            boolean=True,
            ids=[0, 1, 3],
            values=[8, 7, 2],
            after=[[8, 1], [7, 3], [7, 3], [2, None]],
        )
        self.assertTrue(valid_observation("2.3", case, value))
        value["after"][2][1] = None
        self.assertFalse(valid_observation("2.3", case, value))

    def test_sum_rejects_an_aliased_operand_even_with_correct_values(self):
        case = dict(arguments=[[1], [], False], expected=[1])
        value = observation([[1, None]], returned=0, ids=[0], values=[1])
        self.assertFalse(valid_observation("2.5", case, value))
        value.update(returnedId=1, reachableIds=[1])
        self.assertTrue(valid_observation("2.5", case, value))

    def test_intersection_uses_shared_identity_not_equal_values(self):
        case = dict(arguments=[[1], [1], [1]], expected=1)
        value = observation([[1, 2], [1, 2], [1, None]], returned=2)
        self.assertTrue(valid_observation("2.7", case, value))
        value["returnedId"] = 1
        self.assertFalse(valid_observation("2.7", case, value))

    def test_loop_entry_is_not_an_arbitrary_collision_node(self):
        case = dict(arguments=[[6, 1, 6, 4, 8], 2], expected=2)
        value = observation([[6, 1], [1, 2], [6, 3], [4, 4], [8, 2]], returned=2)
        self.assertTrue(valid_observation("2.8", case, value))
        value["returnedId"] = 3
        self.assertFalse(valid_observation("2.8", case, value))


if __name__ == "__main__":
    unittest.main()
