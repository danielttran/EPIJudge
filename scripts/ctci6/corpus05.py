"""Independent per-position oracles, exhaustive interval boundaries and samples."""

import random


def signed(bits):
    return bits if bits < (1 << 31) else bits - (1 << 32)


def oracle(ref, args):
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


def cases(spec):
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


def valid_observation(case, observed):
    return (
        isinstance(observed, dict)
        and observed.get("mutationOk") is True
        and type(observed.get("actual")) is int
        and observed["actual"] == case["expected"]
    )
