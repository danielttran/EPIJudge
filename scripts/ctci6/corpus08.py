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
    from itertools import product
    import json

    ref = spec["ref"]
    if ref in ("8.1", "8.5", "8.11"):
        return basic_cases(spec)
    rng = random.Random(68000 + int(ref.split(".")[1]))
    args = [spec["example"][0]]
    if ref == "8.4":
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
    if ref in ("8.1", "8.5", "8.11"):
        return basic_match(case, observed)
    if not isinstance(observed, dict) or observed.get("mutationOk") is not True:
        return False
    try:
        return canonical(ref, observed.get("actual")) == canonical(
            ref, case["expected"]
        )
    except (ValueError, TypeError):
        return False
