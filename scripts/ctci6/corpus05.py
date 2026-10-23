"""Independent per-position oracles, exhaustive interval boundaries and samples."""

import random


def signed(bits):
    return bits if bits < (1 << 31) else bits - (1 << 32)


def basic_oracle(ref, args):
    if ref == "5.1":
        word, insert, low, high = args
        bits = [((word & 0xFFFFFFFF) >> i) % 2 for i in range(32)]
        for i in range(low, high + 1):
            bits[i] = ((insert & 0xFFFFFFFF) >> (i - low)) % 2
        return signed(sum(bit * (2**i) for i, bit in enumerate(bits)))
    if ref == "5.6":
        first, second = args
        return sum(((first >> i) & 1) != ((second >> i) & 1) for i in range(32))
    if ref == "5.7":
        word = args[0]
        return signed(sum(((word >> (i ^ 1)) & 1) * (2**i) for i in range(32)))
    raise ValueError(ref)


def basic_cases(spec):
    ref = spec["ref"]
    rng = random.Random(6500 + int(ref.split(".")[1]))
    args = [spec["example"][0]]
    endpoints = [-2147483648, -1, 0, 1, 2147483647, 1431655765, -1431655766]
    if ref == "5.1":
        for low in range(32):
            for high in range(low, 32):
                width = high - low + 1
                for insert in (
                    0,
                    signed((1 << width) - 1),
                    signed(rng.getrandbits(width)),
                ):
                    args.append([rng.choice(endpoints), insert, low, high])
        args += [
            [rng.randrange(-(2**31), 2**31), rng.randrange(-(2**31), 2**31), 0, 31]
            for _ in range(100)
        ]
    elif ref == "5.6":
        args += [[a, b] for a in endpoints for b in endpoints]
        args += [
            [rng.randrange(-(2**31), 2**31), rng.randrange(-(2**31), 2**31)]
            for _ in range(200)
        ]
        args += [[signed(1 << i), 0] for i in range(32)]
    else:
        args += [[a] for a in endpoints]
        args += [[signed(1 << i)] for i in range(32)]
        args += [[rng.randrange(-(2**31), 2**31)] for _ in range(200)]
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
    if ref in ("5.1", "5.6", "5.7"):
        return basic_oracle(ref, args)
    if ref == "5.2":
        value = args[0]
        if not 0 < value < 1:
            return "ERROR"
        numerator, denominator = value.as_integer_ratio()
        digits = denominator.bit_length() - 1
        return "." + format(numerator, f"0{digits}b") if digits <= 31 else "ERROR"
    if ref == "5.3":
        # Enumerate the original and each single-bit flip, then count runs as text.
        patterns = [args[0] & 0xFFFFFFFF] + [
            (args[0] & 0xFFFFFFFF) | (1 << i) for i in range(32)
        ]
        return max(
            len(run) for word in patterns for run in format(word, "032b").split("0")
        )
    if ref == "5.4":
        # Independent constrained-bit search, not the solution's carry trick.
        from functools import lru_cache

        number = args[0]
        ones = number.bit_count()

        def extreme(lower, upper, smallest):
            @lru_cache(None)
            def choose(position, left, tight_low, tight_high):
                if position < 0:
                    return 0 if left == 0 else None
                if left < 0 or left > position + 1:
                    return None
                lo = (lower >> position) & 1 if tight_low else 0
                hi = (upper >> position) & 1 if tight_high else 1
                order = range(lo, hi + 1) if smallest else range(hi, lo - 1, -1)
                for bit in order:
                    tail = choose(
                        position - 1,
                        left - bit,
                        tight_low and bit == lo,
                        tight_high and bit == hi,
                    )
                    if tail is not None:
                        return (bit << position) | tail
                return None

            return choose(30, ones, True, True) if lower <= upper else None

        smaller = extreme(1, number - 1, False)
        larger = extreme(number + 1, 2147483647, True)
        return [-1 if smaller is None else smaller, -1 if larger is None else larger]
    if ref == "5.8":
        result = args[0].copy()
        _, width, x1, x2, y = args
        for x in range(x1, x2 + 1):
            result[y * (width // 8) + x // 8] |= 1 << (7 - x % 8)
        return result
    raise ValueError(ref)


def cases(spec):
    ref = spec["ref"]
    if ref in ("5.1", "5.6", "5.7"):
        return basic_cases(spec)
    rng = random.Random(65000 + int(ref.split(".")[1]))
    args = [spec["example"][0]]
    if ref == "5.2":
        args += [
            [v]
            for v in (
                -2.0,
                -0.0,
                0.0,
                1.0,
                2.0,
                0.1,
                0.2,
                0.3,
                0.5,
                0.125,
                0.75,
                0.9999999999999999,
                5e-324,
            )
        ]
        args += [[2.0**-i] for i in range(1, 55)]
        args += [
            [rng.randrange(1, 1 << bits) / (1 << bits)]
            for bits in range(1, 54)
            for _ in range(4)
        ]
    elif ref == "5.3":
        args += [
            [signed(v)]
            for v in (0, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, 0x55555555, 0xAAAAAAAA)
        ]
        args += [
            [signed(v)] for i in range(32) for v in (1 << i, 0xFFFFFFFF ^ (1 << i))
        ]
        args += [[rng.randrange(-(2**31), 2**31)] for _ in range(200)]
    elif ref == "5.4":
        args += [[v] for v in range(1, 257)]
        args += [
            [v]
            for i in range(1, 32)
            for v in ((1 << i) - 1, 1 << (i - 1), 2147483647 ^ ((1 << i) - 1))
            if v > 0
        ]
        args += [[rng.randrange(1, 2147483648)] for _ in range(200)]
    else:
        for x1 in range(16):
            for x2 in range(x1, 16):
                args.append(
                    [
                        [rng.randrange(256) for _ in range(4)],
                        16,
                        x1,
                        x2,
                        rng.randrange(2),
                    ]
                )
        for _ in range(80):
            width = rng.choice([8, 16, 24, 256])
            height = rng.randrange(1, 9)
            x1 = rng.randrange(width)
            x2 = rng.randrange(x1, width)
            args.append(
                [
                    [rng.randrange(256) for _ in range(width // 8 * height)],
                    width,
                    x1,
                    x2,
                    rng.randrange(height),
                ]
            )
        args += [
            [[0] * (4096 // 8 * 256), 4096, 0, 4095, 255],
            [[255] * 4, 16, 0, 15, 1],
        ]
    import json

    distinct = {json.dumps(a): a for a in args}
    return [dict(arguments=a, expected=oracle(ref, a)) for a in distinct.values()]


def valid_observation(case, observed):
    def same(first, second):
        if type(first) is not type(second):
            return False
        if isinstance(first, list):
            return len(first) == len(second) and all(
                same(a, b) for a, b in zip(first, second)
            )
        return first == second

    return (
        isinstance(observed, dict)
        and observed.get("mutationOk") is True
        and same(observed.get("actual"), case["expected"])
    )
