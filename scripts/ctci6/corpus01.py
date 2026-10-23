"""Original cases and deliberately different small-input reference algorithms."""

import itertools
import random
from collections import Counter


def oracle(ref, args):
    if ref == "1.1":
        return len(set(args[0])) == len(args[0])
    if ref == "1.2":
        return sorted(args[0]) == sorted(args[1])
    if ref == "1.3":
        return list("".join(args[0][: args[1]]).replace(" ", "%20"))
    if ref == "1.4":
        letters = [c.lower() for c in args[0] if "A" <= c <= "Z" or "a" <= c <= "z"]
        return sum(n % 2 for n in Counter(letters).values()) <= 1
    if ref == "1.5":
        # Enumerate legal edits instead of mirroring the two-pointer solution.
        a, b = args
        if a == b:
            return True
        if len(a) == len(b):
            return sum(x != y for x, y in zip(a, b)) == 1
        if len(a) > len(b):
            a, b = b, a
        return len(b) == len(a) + 1 and any(
            b[:i] + b[i + 1 :] == a for i in range(len(b))
        )
    if ref == "1.6":
        encoded = "".join(
            letter + str(len(list(run))) for letter, run in itertools.groupby(args[0])
        )
        return encoded if len(encoded) < len(args[0]) else args[0]
    if ref == "1.7":
        a = args[0]
        return [[a[len(a) - 1 - c][r] for c in range(len(a))] for r in range(len(a))]
    if ref == "1.8":
        a = args[0]
        zeroes = [
            (r, c) for r, row in enumerate(a) for c, x in enumerate(row) if x == 0
        ]
        return [
            [
                0 if any(r == zr or c == zc for zr, zc in zeroes) else x
                for c, x in enumerate(row)
            ]
            for r, row in enumerate(a)
        ]
    if ref == "1.9":
        a, b = args
        return (
            bool(a)
            and len(a) == len(b)
            and any(a[i:] + a[:i] == b for i in range(len(a)))
        )
    raise ValueError(ref)


def cases(spec):
    ref = spec["ref"]
    args = [spec["example"][0]]
    rng = random.Random(6100 + int(ref.split(".")[1]))
    ascii_edges = [
        "",
        "a",
        "aA",
        "a a",
        "\0",
        "\0\0",
        "\t\n",
        "Aa! 9",
        "x" * 10000,
        "".join(map(chr, range(128))),
    ]
    if ref in ("1.1", "1.4"):
        args += [[s] for s in ascii_edges]
        args += [
            ["".join(rng.choice("abAB !09\0") for _ in range(rng.randrange(40)))]
            for _ in range(40)
        ]
    elif ref in ("1.2", "1.5", "1.9"):
        args += [
            [a, b]
            for a in ("", "a", "ab", "aa", "aA", "\0")
            for b in ("", "a", "ab", "ba", "aa", "aA", "\0")
        ]
        args += [["x" * 10000, "x" * 9999 + "y"], ["a b", "ba "], ["\0a", "a\0"]]
        for _ in range(40):
            a = "".join(rng.choice("abA !") for _ in range(rng.randrange(15)))
            b = (
                a[rng.randrange(len(a) + 1) :]
                if ref == "1.5"
                else "".join(rng.sample(a, len(a)))
            )
            args.append([a, b])
    elif ref == "1.3":
        for text in (
            "",
            "go",
            " ",
            " a",
            "a ",
            "  ",
            "a  b",
            "%20 ",
            "\0 \t",
            " " * 10000,
        ):
            args.append([list(text) + ["?"] * (2 * text.count(" ")), len(text)])
        for _ in range(40):
            text = "".join(rng.choice("ab %0\0") for _ in range(rng.randrange(30)))
            args.append([list(text) + ["!"] * (2 * text.count(" ")), len(text)])
    elif ref == "1.6":
        args += [
            [s]
            for s in (
                "",
                "a",
                "aa",
                "aaa",
                "ab",
                "Aa",
                "abbbbb",
                "a" * 12,
                "z" * 10000,
                "ab" * 5000,
            )
        ]
        args += [
            ["".join(rng.choice("aAb") for _ in range(rng.randrange(60)))]
            for _ in range(40)
        ]
    elif ref in ("1.7", "1.8"):
        args += [[[]], [[[0]]], [[[1]]], [[[-2147483648]]]]
        if ref == "1.8":
            args += [
                [[[], [], []]],
                [[[0, 1, 2]]],
                [[[1], [0], [3]]],
                [[[1, 0], [2, 3], [4, 5]]],
            ]
        for _ in range(40):
            rows = rng.randrange(7)
            cols = rows if ref == "1.7" else rng.randrange(7)
            args.append(
                [[[rng.randrange(-2, 4) for _ in range(cols)] for _ in range(rows)]]
            )
        size = 100
        args.append([[[r * size + c + 1 for c in range(size)] for r in range(size)]])
    # Keep the worked example first, with deterministic de-duplication.
    import json

    distinct = {json.dumps(a): a for a in args}
    return [dict(arguments=a, expected=oracle(ref, a)) for a in distinct.values()]
