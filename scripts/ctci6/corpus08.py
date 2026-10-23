"""Independent initial recursion/DP references and boundary corpora."""

import random


def oracle(ref, args):
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


def cases(spec):
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


def valid_observation(case, observed):
    return (
        isinstance(observed, dict)
        and observed.get("mutationOk") is True
        and type(observed.get("actual")) is int
        and observed["actual"] == case["expected"]
    )
