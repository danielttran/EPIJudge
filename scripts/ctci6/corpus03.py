"""Original operation transcripts with deliberately simple independent models."""

import json
import random

from chapter03 import APIS


def oracle(ref, args):
    if ref == "3.5":
        return sorted(args[0])
    operations, arguments = args
    capacity = arguments[0][0] if ref in ("3.1", "3.3") else None
    if capacity is not None and not 1 <= capacity <= 256:
        return [dict(error="capacity")]
    output = [None]
    values = []
    stacks = [[], [], []]

    def error(code):
        return dict(error=code)

    for op, values_in in zip(operations[1:], arguments[1:]):
        value = None
        if ref == "3.1":
            index = values_in[0]
            if not 0 <= index < 3:
                value = error("index")
            else:
                chosen = stacks[index]
                if op == "Push":
                    if len(chosen) == capacity:
                        value = error("full")
                    else:
                        chosen.append(values_in[1])
                elif op in ("Pop", "Peek"):
                    value = (
                        error("empty")
                        if not chosen
                        else chosen.pop()
                        if op == "Pop"
                        else chosen[-1]
                    )
                elif op == "IsEmpty":
                    value = not chosen
                elif op == "IsFull":
                    value = len(chosen) == capacity
                else:
                    raise ValueError(op)
        elif ref == "3.2":
            if op == "Push":
                values.append(values_in[0])
            elif op == "IsEmpty":
                value = not values
            elif not values:
                value = error("empty")
            elif op == "Pop":
                value = values.pop()
            elif op == "Peek":
                value = values[-1]
            elif op == "GetMin":
                value = min(values)
            else:
                raise ValueError(op)
        elif ref == "3.3":
            if op == "Push":
                values.append(values_in[0])
            elif op == "IsEmpty":
                value = not values
            elif op == "Pop":
                value = values.pop() if values else error("empty")
            elif op == "PopAt":
                index = values_in[0]
                count = (len(values) + capacity - 1) // capacity
                if not 0 <= index < count:
                    value = error("index")
                else:
                    value = values.pop(min((index + 1) * capacity, len(values)) - 1)
            else:
                raise ValueError(op)
        elif ref == "3.4":
            if op == "Add":
                values.append(values_in[0])
            elif op == "Size":
                value = len(values)
            elif not values:
                value = error("empty")
            elif op == "Peek":
                value = values[0]
            elif op == "Remove":
                value = values.pop(0)
            else:
                raise ValueError(op)
        elif ref == "3.6":
            if op == "Enqueue":
                if values_in[1] not in ("dog", "cat"):
                    value = error("species")
                else:
                    values.append(tuple(values_in))
            elif op == "Size":
                value = len(values)
            elif op == "Peek":
                value = values[0][0] if values else None
            else:
                species = (
                    None
                    if op == "DequeueAny"
                    else "dog"
                    if op == "DequeueDog"
                    else "cat"
                    if op == "DequeueCat"
                    else "invalid"
                )
                if species == "invalid":
                    raise ValueError(op)
                index = next(
                    (
                        i
                        for i, a in enumerate(values)
                        if species is None or a[1] == species
                    ),
                    None,
                )
                value = values.pop(index)[0] if index is not None else None
        else:
            raise ValueError(ref)
        output.append(value)
    return output


def cases(spec):
    ref = spec["ref"]
    args = [spec["example"][0]]
    rng = random.Random(6300 + int(ref.split(".")[1]))
    if ref == "3.5":
        args += [
            [a]
            for a in (
                [],
                [1],
                [2, 2],
                [7, 1, 5],
                [1, 2, 3],
                [3, 2, 1],
                [-2147483648, 0, 2147483647],
                [4] * 2000,
                list(range(2000)),
                list(range(1999, -1, -1)),
            )
        ]
        args += [
            [[rng.randrange(-5, 6) for _ in range(rng.randrange(40))]]
            for _ in range(40)
        ]
    else:
        cls = APIS[ref][0]
        if ref in ("3.1", "3.3"):
            args += [
                [[cls], [[capacity]]]
                for capacity in (-2147483648, -1, 0, 257, 2147483647)
            ]
        for trial in range(45):
            capacity = (1, 2, 3, 256)[trial % 4] if ref in ("3.1", "3.3") else None
            ops, arguments = [cls], [[capacity] if capacity is not None else []]
            for index in range(60 if trial < 44 else 2000):
                payload = rng.choice([-2147483648, 2147483647, -1, 0, 1, 2, 2])
                if ref == "3.1":
                    op = rng.choice(["Push", "Pop", "Peek", "IsEmpty", "IsFull"])
                    stack = rng.choice([-1, 0, 1, 2, 3])
                    value = [stack, payload] if op == "Push" else [stack]
                elif ref == "3.2":
                    op = rng.choice(
                        ["Push", "Push", "Pop", "Peek", "GetMin", "IsEmpty"]
                    )
                    value = [payload] if op == "Push" else []
                elif ref == "3.3":
                    op = rng.choice(["Push", "Push", "Pop", "PopAt", "IsEmpty"])
                    value = (
                        [payload]
                        if op == "Push"
                        else [rng.randrange(-1, 8)]
                        if op == "PopAt"
                        else []
                    )
                elif ref == "3.4":
                    op = rng.choice(["Add", "Add", "Remove", "Peek", "Size"])
                    value = [payload] if op == "Add" else []
                else:
                    op = rng.choice(
                        [
                            "Enqueue",
                            "Enqueue",
                            "DequeueAny",
                            "DequeueDog",
                            "DequeueCat",
                            "Peek",
                            "Size",
                        ]
                    )
                    value = (
                        [index - 1000, rng.choice(["dog", "cat", "dog", "fish"])]
                        if op == "Enqueue"
                        else []
                    )
                ops.append(op)
                arguments.append(value)
            args.append([ops, arguments])
        if ref == "3.1":
            args.append(
                [
                    [
                        cls,
                        "Push",
                        "Push",
                        "IsFull",
                        "Pop",
                        "Pop",
                        "Push",
                        "Peek",
                        "IsEmpty",
                    ],
                    [[1], [0, 9], [0, 8], [0], [0], [0], [0, 7], [0], [1]],
                ]
            )
        elif ref == "3.2":
            args.append(
                [
                    [
                        cls,
                        "Push",
                        "Push",
                        "Pop",
                        "GetMin",
                        "Pop",
                        "GetMin",
                        "Push",
                        "GetMin",
                    ],
                    [[], [4], [4], [], [], [], [], [-2147483648], []],
                ]
            )
        elif ref == "3.3":
            args.append(
                [
                    [cls] + ["Push"] * 8 + ["PopAt"] * 5 + ["Pop"] * 5,
                    [[2]]
                    + [[i] for i in range(8)]
                    + [[0], [1], [0], [1], [0]]
                    + [[]] * 5,
                ]
            )
        elif ref == "3.4":
            args.append(
                [
                    [
                        cls,
                        "Add",
                        "Add",
                        "Remove",
                        "Add",
                        "Peek",
                        "Size",
                        "Peek",
                        "Remove",
                        "Remove",
                        "Remove",
                    ],
                    [[], [6], [2], [], [9], [], [], [], [], [], []],
                ]
            )
        else:
            args.append(
                [
                    [
                        cls,
                        "DequeueAny",
                        "Enqueue",
                        "Enqueue",
                        "Enqueue",
                        "Size",
                        "DequeueCat",
                        "Peek",
                        "DequeueAny",
                        "DequeueDog",
                        "Size",
                    ],
                    [
                        [],
                        [],
                        [8, "dog"],
                        [3, "fish"],
                        [-4, "cat"],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                    ],
                ]
            )
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
        if isinstance(first, dict):
            return first.keys() == second.keys() and all(
                same(first[k], second[k]) for k in first
            )
        return first == second

    return (
        isinstance(observed, dict)
        and observed.get("mutationOk") is True
        and same(observed.get("actual"), case["expected"])
    )
