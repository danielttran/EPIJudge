"""Independent initial recursion/DP references and boundary corpora."""

import random


def basic_oracle(ref, args):
    if ref == "8.1":
        from functools import lru_cache

        @lru_cache(None)
        def routes(steps):
            if steps < 0:
                return 0
            if steps == 0:
                return 1
            return sum(routes(steps - hop) for hop in (1, 2, 3))

        return routes(args[0])
    if ref == "8.5":
        return args[0] * args[1]
    if ref == "8.11":
        amount = args[0]
        return sum(
            (amount - 25 * quarters - 10 * dimes) // 5 + 1
            for quarters in range(amount // 25 + 1)
            for dimes in range((amount - 25 * quarters) // 10 + 1)
        )
    raise ValueError(ref)


def basic_cases(spec):
    ref = spec["ref"]
    rng = random.Random(6800 + int(ref.split(".")[1]))
    args = [spec["example"][0]]
    if ref == "8.1":
        args += [[n] for n in [-2147483648, -100, -3, -2, -1, *range(37)]]
    elif ref == "8.5":
        args += [[a, b] for a in range(32) for b in range(32)]
        args += [
            [a, b] for a in (0, 1, 2, 46339, 46340) for b in (0, 1, 2, 46339, 46340)
        ]
        args += [[rng.randrange(46341), rng.randrange(46341)] for _ in range(100)]
    else:
        args += [
            [n]
            for n in (
                *range(126),
                9999,
                10000,
                *[rng.randrange(10001) for _ in range(100)],
            )
        ]
    distinct = {tuple(a): a for a in args}
    return [dict(arguments=a, expected=oracle(ref, a)) for a in distinct.values()]


def basic_match(case, observed):
    return (
        isinstance(observed, dict)
        and observed.get("mutationOk") is True
        and type(observed.get("actual")) is int
        and observed["actual"] == case["expected"]
    )


def oracle(ref, args):
    from itertools import combinations, permutations, product

    if ref in ("8.1", "8.5", "8.11"):
        return basic_oracle(ref, args)
    if ref == "8.3":
        return next((i for i, value in enumerate(args[0]) if i == value), -1)
    if ref == "8.12":
        # Enumerate full permutations, independent of the row/mask solution.
        return [list(board) for board in permutations(range(8))
                if all(abs(board[a] - board[b]) != b - a
                       for a in range(8) for b in range(a + 1, 8))]
    if ref == "8.13":
        # Exhaust all fitting paths without sorting or the solution's DP order.
        boxes = args[0]
        def above(bottom):
            return boxes[bottom][1] + max(
                (above(top) for top in range(len(boxes))
                 if all(boxes[top][d] < boxes[bottom][d] for d in range(3))),
                default=0)
        return max((above(i) for i in range(len(boxes))), default=0)
    if ref == "8.14":
        from functools import lru_cache
        @lru_cache(None)
        def evaluations(text):
            if not text:
                return ()
            if len(text) == 1:
                return (text == "1",)
            result = []
            for split in range(1, len(text), 2):
                for left in evaluations(text[:split]):
                    for right in evaluations(text[split + 1:]):
                        result.append(left and right if text[split] == "&" else
                                      left or right if text[split] == "|" else left != right)
            return tuple(result)
        return sum(value == args[1] for value in evaluations(args[0]))
    if ref == "8.4":
        return [
            list(subset)
            for size in range(len(args[0]) + 1)
            for subset in combinations(args[0], size)
        ]
    if ref in ("8.7", "8.8"):
        return sorted({"".join(chars) for chars in permutations(args[0])})
    if ref == "8.9":
        result = []
        for chars in product("()", repeat=2 * args[0]):
            balance = 0
            for char in chars:
                balance += 1 if char == "(" else -1
                if balance < 0:
                    break
            else:
                if balance == 0:
                    result.append("".join(chars))
        return result
    raise ValueError(ref)


def cases(spec):
    from itertools import product, combinations, combinations_with_replacement
    import json

    ref = spec["ref"]
    if ref in ("8.1", "8.5", "8.11"):
        return basic_cases(spec)
    rng = random.Random(68000 + int(ref.split(".")[1]))
    args = [spec["example"][0]]
    if ref == "8.3":
        args += [[list(values), False] for n in range(6)
                 for values in combinations_with_replacement(range(-2, 5), n)]
        args += [[list(values), True] for n in range(7)
                 for values in combinations(range(-3, 8), n)]
        args += [[values, flag] for flag in (True, False)
                 for values in ([-2147483648, 2147483647], list(range(10000)),
                                list(range(-10000, 0)), list(range(1, 10001))) ]
        args += [[[4] * 10000, False], [[-2147483648] * 10000, False]]
    elif ref == "8.12":
        # Deliberately preserve repeated no-argument calls to catch accumulated state.
        answer = oracle(ref, [])
        return [dict(arguments=[], expected=answer) for _ in range(3)]
    elif ref == "8.13":
        args += [[values] for values in ([], [[1, 1, 1]], [[2, 2, 2]] * 3,
                 [[5, 5, 5], [5, 4, 4]], [[5, 5, 5], [4, 5, 4]],
                 [[5, 5, 5], [4, 4, 5]], [[10, 1, 10], [1, 10, 1]],
                 [[i, i, i] for i in range(1, 13)], [[1000, 1000, 1000]])]
        args += [[[list(box) for box in values]]
                 for values in combinations_with_replacement(list(product((1, 2), repeat=3)), 3)]
        args += [[[[rng.randrange(1, 15) for _ in range(3)] for _ in range(rng.randrange(13))]]
                 for _ in range(60)]
    elif ref == "8.14":
        args += [["", desired] for desired in (True, False)]
        for n in range(1, 5):
            for literals in product("01", repeat=n):
                for operators in product("&|^", repeat=n-1):
                    text = "".join(literals[i] + (operators[i] if i < n-1 else "") for i in range(n))
                    args += [[text, desired] for desired in (False, True)]
        args += [[operation.join([literal] * 13), desired]
                 for operation in "&|^" for literal in "01" for desired in (False, True)]
        args += [["".join(rng.choice("01") + (rng.choice("&|^") if i < 6 else "")
                         for i in range(7)), desired] for desired in (False, True) for _ in range(20)]
    elif ref == "8.4":
        args += [
            [a]
            for a in ([], [1], [-2147483648, 2147483647], [3, 1, 2], list(range(12)))
        ]
        args += [[rng.sample(range(-100, 101), rng.randrange(7))] for _ in range(35)]
    elif ref == "8.7":
        args += [["abcdefgh"[:length]] for length in range(9)]
        args += [
            ["".join(rng.sample("abcdefghijklmnop", rng.randrange(6)))]
            for _ in range(20)
        ]
    elif ref == "8.8":
        args += [
            ["".join(chars)]
            for length in range(5)
            for chars in product("abc", repeat=length)
        ]
        args += [
            [text]
            for text in (
                "aaaaaaaa",
                "aabbccdd",
                "aaaaabbb",
                "abcdefgh",
                "aabbccc",
                "zzzzzzzz",
            )
        ]
    else:
        args += [[pairs] for pairs in range(9)]
    distinct = {json.dumps(a): a for a in args}
    return [dict(arguments=a, expected=oracle(ref, a)) for a in distinct.values()]


def canonical(ref, value):
    if type(value) is not list:
        raise ValueError("Return a collection")
    if ref == "8.12":
        if any(type(row) is not list or len(row) != 8
               or any(type(v) is not int or not 0 <= v < 8 for v in row)
               for row in value):
            raise ValueError("Return eight column integers per board")
        return sorted(tuple(row) for row in value)
    if ref == "8.4":
        if any(
            type(row) is not list
            or any(type(v) is not int for v in row)
            or len(set(row)) != len(row)
            for row in value
        ):
            raise ValueError("Each subset must contain distinct integer members")
        return sorted(tuple(sorted(row)) for row in value)
    if any(type(item) is not str for item in value):
        raise ValueError("Return strings")
    return sorted(value)


def valid_observation(ref, case, observed):
    if ref == "8.3":
        if not isinstance(observed, dict) or observed.get("mutationOk") is not True:
            return False
        actual, values = observed.get("actual"), case["arguments"][0]
        return type(actual) is int and ((actual == -1 and not any(i == v for i, v in enumerate(values)))
                                       or 0 <= actual < len(values) and values[actual] == actual)
    if ref in ("8.1", "8.5", "8.11", "8.13", "8.14"):
        return basic_match(case, observed)
    if not isinstance(observed, dict) or observed.get("mutationOk") is not True:
        return False
    try:
        return canonical(ref, observed.get("actual")) == canonical(
            ref, case["expected"]
        )
    except (ValueError, TypeError):
        return False
