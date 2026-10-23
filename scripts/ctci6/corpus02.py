"""Independent scalar reference results and identity-aware list observations."""

from collections import Counter
import json
import random


def oracle(ref, args):
    if ref == "2.1":
        return list(dict.fromkeys(args[0]))
    if ref == "2.2":
        values, k = args
        return len(values) - k if 1 <= k <= len(values) else None
    if ref == "2.3":
        values, index = args
        success = 0 <= index < len(values) - 1
        return dict(
            success=success,
            values=values[:index] + values[index + 1 :] if success else values,
        )
    if ref == "2.4":
        values, pivot = args
        return [x for x in values if x < pivot] + [x for x in values if x >= pivot]
    if ref == "2.5":
        first, second, forward = args
        if not first and not second:
            return []

        def number(digits):
            ordered = digits if forward else digits[::-1]
            return int("".join(map(str, ordered)) or "0")

        result = list(map(int, str(number(first) + number(second))))
        return result if forward else result[::-1]
    if ref == "2.6":
        return args[0] == args[0][::-1]
    if ref == "2.7":
        return len(args[0]) if args[2] else None
    if ref == "2.8":
        return args[1] if args[1] >= 0 else None
    raise ValueError(ref)


def cases(spec):
    ref = spec["ref"]
    rows = [spec["example"][0]]
    rng = random.Random(6200 + int(ref.split(".")[1]))
    lists = [
        [],
        [0],
        [-1],
        [1000, 1000],
        [5, 5, 5],
        [3, 1, 3, 2, 1],
        [1, 2, 1],
        [1000, -2000, -2000, 1000],
        [-2147483648, 2147483647],
        [7] * 2000,
    ]
    lists += [
        [rng.randrange(-3, 4) for _ in range(rng.randrange(30))] for _ in range(35)
    ]
    if ref in ("2.1", "2.6"):
        rows += [[a] for a in lists]
    elif ref == "2.2":
        rows += [
            [a, k]
            for a in lists
            for k in (-2147483648, 0, 1, 2, len(a), len(a) + 1, 2147483647)
        ]
    elif ref == "2.3":
        rows += [
            [a, i]
            for a in lists
            for i in ([-1] if not a else [-1, 0, len(a) // 2, len(a) - 1])
        ]
    elif ref == "2.4":
        rows += [[a, pivot] for a in lists for pivot in (-2147483648, 0, 2, 2147483647)]
    elif ref == "2.5":
        for flag in (False, True):
            rows += [
                [a, b, flag]
                for a in ([], [0], [9], [8, 7], [9] * 2000)
                for b in ([], [0], [1], [3, 2])
            ]
            for _ in range(40):
                a, b = rng.randrange(10**12), rng.randrange(10**12)
                left, right = list(map(int, str(a))), list(map(int, str(b)))
                rows.append(
                    [left if flag else left[::-1], right if flag else right[::-1], flag]
                )
    elif ref == "2.7":
        rows += [
            [a, b, c]
            for a in ([], [1], [1, 1])
            for b in ([], [1], [1, 1, 1])
            for c in ([], [1], [8, 1])
        ]
        for _ in range(40):
            rows.append(
                [[rng.randrange(3) for _ in range(rng.randrange(15))] for _ in range(3)]
            )
        rows.append([[1] * 1500, [1] * 1500, [1] * 1000])
    elif ref == "2.8":
        rows += [
            [a, i]
            for a in lists
            for i in ([-1] if not a else [-1, 0, len(a) // 2, len(a) - 1])
        ]
    distinct = {json.dumps(a): a for a in rows}
    return [dict(arguments=a, expected=oracle(ref, a)) for a in distinct.values()]


def input_graph(ref, args):
    segments = args[:3] if ref == "2.7" else args[:2] if ref == "2.5" else args[:1]
    nodes = []
    offset = 0
    ends = []
    for values in segments:
        nodes.extend(
            [value, offset + i + 1 if i + 1 < len(values) else None]
            for i, value in enumerate(values)
        )
        ends.append(offset + len(values) - 1 if values else None)
        offset += len(values)
    if ref == "2.7":
        common = len(args[0]) + len(args[1]) if args[2] else None
        for end in ends[:2]:
            if end is not None:
                nodes[end][1] = common
    elif ref == "2.8" and nodes and args[1] >= 0:
        nodes[-1][1] = args[1]
    return nodes


def valid_observation(ref, case, observed):
    """Grade values AND identities from a language-neutral observation protocol."""
    if observed.get("error"):
        return False
    args, expected = case["arguments"], case["expected"]
    before, after = observed["before"], observed["after"]
    if before != input_graph(ref, args):
        return False
    ids, values = observed["reachableIds"], observed["reachableValues"]
    returned, boolean = observed["returnedId"], observed["returnedBool"]
    if len(before) != len(after) or len(ids) != len(values):
        return False
    if ref == "2.1":
        kept = []
        seen = set()
        for i, value in enumerate(args[0]):
            if value not in seen:
                kept.append(i)
                seen.add(value)
        return (
            not observed["cycle"]
            and ids == kept
            and values == expected
            and all(a[0] == b[0] for a, b in zip(before, after))
        )
    if ref == "2.2":
        return returned == expected and before == after
    if ref == "2.3":
        desired = [list(row) for row in before]
        selected = args[1]
        success = expected["success"]
        if success:
            desired[selected] = [before[selected + 1][0], before[selected + 1][1]]
        kept = [i for i in range(len(before)) if not success or i != selected + 1]
        return (
            type(boolean) is bool
            and boolean is success
            and after == desired
            and ids == kept
            and values == expected["values"]
            and not observed["cycle"]
        )
    if ref == "2.4":
        if (
            observed["cycle"]
            or Counter(ids) != Counter(range(len(before)))
            or any(a[0] != b[0] for a, b in zip(before, after))
        ):
            return False
        pivot = args[1]
        boundary = next((i for i, v in enumerate(values) if v >= pivot), len(values))
        return all(v >= pivot for v in values[boundary:]) and all(
            values[i] == before[node_id][0] for i, node_id in enumerate(ids)
        )
    if ref == "2.5":
        return (
            before == after
            and not observed["cycle"]
            and values == expected
            and all(i >= len(before) for i in ids)
            and len(set(ids)) == len(ids)
        )
    if ref == "2.6":
        return type(boolean) is bool and boolean == expected and before == after
    if ref == "2.7":
        desired = len(args[0]) + len(args[1]) if args[2] else None
        return returned == desired and before == after
    if ref == "2.8":
        return returned == expected and before == after
    raise ValueError(ref)
