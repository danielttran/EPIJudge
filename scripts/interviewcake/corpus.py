"""Independent brute-force/model oracles and deterministic bounded corpora."""

import base64
import collections
import itertools
import json
import random
import re

from specs import ROOT, S

R = random.Random(0x1CA4E)


def tree(a):
    if not a:
        return None
    nodes = [[a[0], None, None]]
    i = 1
    for n in nodes:
        for child in (1, 2):
            if i < len(a) and a[i] is not None:
                n[child] = [a[i], None, None]
                nodes.append(n[child])
            i += 1
    return nodes[0]


def leaves(t, d=0):
    return (
        []
        if t is None
        else [d]
        if t[1] is None and t[2] is None
        else leaves(t[1], d + 1) + leaves(t[2], d + 1)
    )


def inorder(t):
    return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])


def bst_array(values):
    def build(v):
        if not v:
            return None
        k = len(v) // 2
        return [v[k], build(v[:k]), build(v[k + 1 :])]

    q = [build(sorted(values))]
    out = []
    for t in q:
        if t is None:
            out.append(None)
        else:
            out.append(t[0])
            q.extend(t[1:])
    while out and out[-1] is None:
        out.pop()
    return out


def fingerprint(file):
    b = (
        base64.b64decode(file["base64"])
        if "base64" in file
        else file["content"].encode()
    )
    last = max(0, len(b) - 64)
    return (len(b), *(b[p : p + 64] for p in (0, last // 2, last)))


def oracle(s, a):
    slug = s["sourceId"]
    mode = s["mode"]
    if slug == "second-largest-item-in-bst":
        return sorted(inorder(tree(a[0])))[-2]
    if slug == "stock-price":
        return max(y - x for i, x in enumerate(a[0]) for y in a[0][i + 1 :])
    if slug == "balanced-binary-tree":
        d = leaves(tree(a[0]))
        return not d or max(d) - min(d) <= 1
    if slug == "bst-checker":
        v = inorder(tree(a[0]))
        return all(x < y for x, y in itertools.pairwise(v))
    if slug == "bracket-validator":
        old = None
        t = "".join(c for c in a[0] if c in "()[]{}")
        while old != t:
            old = t
            t = t.replace("()", "").replace("[]", "").replace("{}", "")
        return not t
    if slug == "cafe-order-checker":
        first, second, served = a
        states = {(0, 0)}
        for v in served:
            states = {
                (i + 1, j) for i, j in states if i < len(first) and first[i] == v
            } | {(i, j + 1) for i, j in states if j < len(second) and second[j] == v}
        return (len(first), len(second)) in states
    if slug == "nth-fibonacci":
        f = [0, 1]
        for _ in range(2, a[0] + 1):
            f.append(f[-1] + f[-2])
        return f[a[0]]
    if mode == "delete":
        return a[0][: a[1]] + a[0][a[1] + 1 :]
    if mode == "cycle":
        return a[1] >= 0
    if mode == "files":
        groups = collections.defaultdict(list)
        for f in a[0]:
            groups[fingerprint(f)].append(f)
        return [
            [x["path"] for x in sorted(g, key=lambda f: (f["modified"], f["path"]))]
            for g in groups.values()
            if len(g) == 2
        ]
    if mode == "duplicate":
        return next(x for x, c in collections.Counter(a[0]).items() if c > 1)
    if slug == "find-rotation-point":
        return min(range(len(a[0])), key=lambda i: a[0][i])
    if mode in ("color", "shuffle", "rand5", "rand7"):
        return True
    if slug == "highest-product-of-3":
        return max(x * y * z for x, y, z in itertools.combinations(a[0], 3))
    if mode in ("queue", "stack", "trie", "temperature"):
        out = []
        data = []
        seen = set()
        for op, args in zip(*a):
            if op in ("Enqueue", "Push", "Insert"):
                data.append(args[0])
                out.append(None)
            elif op in ("Dequeue", "Pop"):
                out.append(
                    data.pop(0 if op == "Dequeue" else -1)
                    if data
                    else {"error": "empty"}
                )
            elif op == "GetMax":
                out.append(
                    max(data)
                    if data
                    else None
                    if mode == "temperature"
                    else {"error": "empty"}
                )
            elif op == "GetMin":
                out.append(min(data) if data else None)
            elif op == "GetMean":
                out.append(sum(data) / len(data) if data else None)
            elif op == "GetMode":
                counts = collections.Counter(data)
                out.append(
                    next(v for v, c in counts.items() if c == max(counts.values()))
                    if data
                    else None
                )
            elif op == "AddWord":
                out.append(args[0] not in seen)
                seen.add(args[0])
        return out
    if slug == "inflight-entertainment":
        return any(x + y == a[1] for x, y in itertools.combinations(a[0], 2))
    if mode == "kth":
        return len(a[1]) - a[0]
    if slug == "coin":

        def count(amount, coins):
            if not coins:
                return int(amount == 0)
            return sum(
                count(amount - k * coins[0], coins[1:])
                for k in range(amount // coins[0] + 1)
            )

        return count(*a)
    if slug == "merge-sorted-arrays":
        return sorted(a[0] + a[1])
    if mode == "meetings":
        # Endpoint sweep oracle, separate from the reference's sort-and-extend loop.
        events = collections.Counter()
        for x, y in a[0]:
            events[x] += 1
            events[y] -= 1
        answer = []
        active = 0
        start = None
        for x in sorted(events):
            before = active
            active += events[x]
            if before == 0 and active > 0:
                start = x
            if before > 0 and active == 0:
                answer.append([start, x])
        return answer
    if mode == "path":
        graph, start, end = a
        q = collections.deque([[start]])
        seen = {start}
        while q:
            path = q.popleft()
            if path[-1] == end:
                return path
            for x in graph[path[-1]]:
                if x not in seen:
                    seen.add(x)
                    q.append(path + [x])
        return None
    if slug == "matching-parens":
        balance = 0
        for i in range(a[1], len(a[0])):
            balance += (a[0][i] == "(") - (a[0][i] == ")")
            if balance == 0:
                return i
        raise ValueError("Missing closer in corpus")
    if slug == "permutation-palindrome":
        return sum(c % 2 for c in collections.Counter(a[0]).values()) <= 1
    if slug == "product-of-other-numbers":
        import math

        return [math.prod(a[0][:i] + a[0][i + 1 :]) for i in range(len(a[0]))]
    if mode == "rect":
        r, t = a
        x = max(r[0], t[0])
        y = max(r[1], t[1])
        w = min(r[0] + r[2], t[0] + t[2]) - x
        h = min(r[1] + r[3], t[1] + t[3]) - y
        return [x, y, w, h] if min(w, h) > 0 else [0, 0, 0, 0]
    if mode == "set":
        return sorted({"".join(p) for p in itertools.permutations(a[0])})
    if mode == "reverse_list":
        return a[0][::-1]
    if mode == "chars":
        return a[0][::-1]
    if mode == "words":
        return " ".join(a[0].split(" ")[::-1])
    if slug == "cake-thief":
        types, capacity = a
        if any(w == 0 and v > 0 for w, v in types):
            return {"error": "infinite"}
        types = [(w, v) for w, v in types if w]
        memo = {}

        def search(i, left):
            if i == len(types):
                return 0
            if (i, left) not in memo:
                w, v = types[i]
                memo[i, left] = max(
                    k * v + search(i + 1, left - k * w) for k in range(left // w + 1)
                )
            return memo[i, left]

        return search(0, capacity)
    if slug == "find-unique-int-among-duplicates":
        return next(x for x, c in collections.Counter(a[0]).items() if c == 1)
    if slug == "top-scores":
        return sorted(a[0], reverse=True)
    if slug == "which-appears-twice":
        return next(x for x, c in collections.Counter(a[0]).items() if c == 2)
    if mode == "wordcloud":
        return dict(
            collections.Counter(
                x.lower() for x in re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", a[0])
            )
        )
    raise ValueError(slug)


def cases(s):
    slug = s["sourceId"]
    mode = s["mode"]
    args = [a for a, e in s["examplesData"]]
    # Independently verify every published example; multiple-answer exemplars use property predicates later.
    for a, expected in s["examplesData"]:
        real = oracle(s, a)
        if mode not in ("duplicate", "path", "temperature"):
            assert real == expected, (slug, a, real, expected)
    extra = []
    if mode in (
        "pure",
        "duplicate",
        "path",
        "set",
        "rect",
        "meetings",
        "kth",
        "reverse_list",
        "chars",
        "words",
        "delete",
        "cycle",
        "files",
        "color",
        "shuffle",
        "rand5",
        "rand7",
        "queue",
        "stack",
        "trie",
        "temperature",
        "wordcloud",
    ):
        pass
    for trial in range(18):
        if slug == "second-largest-item-in-bst":
            extra.append([bst_array(R.sample(range(-100, 101), R.randint(2, 25)))])
        elif slug == "stock-price":
            extra.append([[R.randrange(30) for _ in range(R.randint(2, 25))]])
        elif slug in ("balanced-binary-tree", "bst-checker"):
            a = bst_array(R.sample(range(-100, 101), R.randint(0, 20)))
            if slug == "bst-checker" and a and trial % 2:
                a[R.randrange(len(a))] = R.randrange(-100, 101)
            extra.append([a])
        elif slug == "bracket-validator":
            extra.append(
                ["".join(R.choice("()[]{}abc ") for _ in range(R.randrange(40)))]
            )
        elif slug == "cafe-order-checker":
            total = R.randrange(15)
            v = R.sample(range(-100, 101), total)
            cut = R.randrange(total + 1)
            left = v[:cut]
            right = v[cut:]
            served = []
            i = j = 0
            while i < len(left) or j < len(right):
                if j == len(right) or i < len(left) and R.randrange(2):
                    served.append(left[i])
                    i += 1
                else:
                    served.append(right[j])
                    j += 1
            if trial % 3 == 0 and served:
                R.shuffle(served)
            if trial % 5 == 0:
                served.append(1000)
            extra.append([left, right, served])
        elif slug == "nth-fibonacci":
            extra.append([R.randrange(47)])
        elif mode == "delete":
            a = [R.randrange(-5, 6) for _ in range(R.randint(2, 20))]
            extra.append([a, R.randrange(len(a) - 1)])
        elif mode == "cycle":
            a = [R.randrange(5) for _ in range(R.randrange(20))]
            extra.append([a, R.randrange(-1, len(a)) if a else -1])
        elif mode == "duplicate":
            n = R.randint(1, 30)
            extra.append([[R.randint(1, n) for _ in range(n + 1)]])
        elif slug == "find-rotation-point":
            a = sorted(
                R.sample(
                    ["".join(p) for p in itertools.product("abcd", repeat=3)],
                    R.randint(1, 30),
                )
            )
            k = R.randrange(len(a))
            extra.append([a[k:] + a[:k]])
        elif mode == "color":
            n = R.randrange(12)
            a = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i):
                    if R.randrange(3) == 0:
                        a[i].append(j)
                        a[j].append(i)
            extra.append(
                [a, ["color" + str(i) for i in range(max(map(len, a), default=0) + 1)]]
            )
        elif slug == "highest-product-of-3":
            extra.append([[R.randrange(-20, 21) for _ in range(R.randint(3, 12))]])
        elif mode in ("queue", "stack", "temperature"):
            names = {
                "queue": ["Enqueue", "Dequeue"],
                "stack": ["Push", "Pop", "GetMax"],
                "temperature": ["Insert", "GetMin", "GetMax", "GetMean", "GetMode"],
            }[mode]
            ops = []
            values = []
            for _ in range(50):
                op = R.choice(names)
                ops.append(op)
                values.append(
                    [
                        R.randrange(111)
                        if mode == "temperature"
                        else R.randrange(-20, 21)
                    ]
                    if op in ("Insert", "Push", "Enqueue")
                    else []
                )
            extra.append([ops, values])
        elif mode == "shuffle":
            extra.append([[R.randrange(5) for _ in range(R.randrange(0, 5))]])
        elif slug == "inflight-entertainment":
            extra.append(
                [[R.randrange(30) for _ in range(R.randrange(20))], R.randrange(60)]
            )
        elif mode == "kth":
            a = [R.randrange(4) for _ in range(R.randint(1, 20))]
            extra.append([R.randint(1, len(a)), a])
        elif slug == "coin":
            extra.append([R.randrange(25), R.sample(range(1, 12), R.randrange(0, 6))])
        elif slug == "merge-sorted-arrays":
            extra.append(
                [
                    sorted(R.randrange(-20, 21) for _ in range(R.randrange(20))),
                    sorted(R.randrange(-20, 21) for _ in range(R.randrange(20))),
                ]
            )
        elif mode == "meetings":
            extra.append(
                [
                    [
                        [x := R.randrange(-20, 21), x + R.randint(1, 10)]
                        for _ in range(R.randrange(15))
                    ]
                ]
            )
        elif mode == "path":
            n = R.randint(1, 12)
            g = {str(i): [] for i in range(n)}
            for i in range(n):
                for j in range(i):
                    if R.randrange(4) == 0:
                        g[str(i)].append(str(j))
                        g[str(j)].append(str(i))
            extra.append([g, str(R.randrange(n)), str(R.randrange(n))])
        elif mode == "trie":
            values = ["", "a", "ab", "abc", "b", "https://x/a", "https://x/b"]
            extra.append([["AddWord"] * 25, [[R.choice(values)] for _ in range(25)]])
        elif slug == "matching-parens":
            n = R.randint(1, 12)
            text = "x" + "(" * n + "body" + ")" * n + "tail"
            extra.append([text, R.randint(1, n)])
        elif slug == "permutation-palindrome":
            extra.append(["".join(R.choice("abcde") for _ in range(R.randrange(30)))])
        elif slug == "product-of-other-numbers":
            extra.append([[R.randrange(-3, 4) for _ in range(R.randint(2, 10))]])
        elif mode == "rect":
            extra.append(
                [
                    [
                        R.randrange(-20, 21),
                        R.randrange(-20, 21),
                        R.randint(1, 20),
                        R.randint(1, 20),
                    ]
                    for _ in range(2)
                ]
            )
        elif mode == "set":
            extra.append(["".join(R.sample("abcd", R.randrange(5)))])
        elif mode == "reverse_list":
            extra.append([[R.randrange(4) for _ in range(R.randrange(20))]])
        elif mode == "chars":
            extra.append(
                ["".join(R.choice("abc xyz!?") for _ in range(R.randrange(30)))]
            )
        elif mode == "words":
            extra.append(
                [
                    " ".join(
                        "".join(R.choice("abcdef") for _ in range(R.randint(1, 8)))
                        for _ in range(R.randrange(8))
                    )
                ]
            )
        elif mode in ("rand5", "rand7"):
            # All prefixes are valid source draws and eventually fall back to a deterministic stream.
            extra.append(
                [
                    [
                        R.randint(1, 7 if mode == "rand5" else 5)
                        for _ in range(R.randrange(12))
                    ]
                ]
            )
        elif slug == "cake-thief":
            extra.append(
                [
                    [[R.randrange(8), R.randrange(30)] for _ in range(R.randrange(6))],
                    R.randrange(25),
                ]
            )
        elif slug == "find-unique-int-among-duplicates":
            a = R.sample(range(1, 1000), R.randint(1, 15))
            v = a[:1] + a[1:] * 2
            R.shuffle(v)
            extra.append([v])
        elif slug == "top-scores":
            k = R.randrange(25)
            extra.append([[R.randint(0, k) for _ in range(R.randrange(40))], k])
        elif slug == "which-appears-twice":
            n = R.randint(1, 60)
            a = list(range(1, n + 1)) + [R.randint(1, n)]
            R.shuffle(a)
            extra.append([a])
        elif mode == "wordcloud":
            extra.append(
                [
                    " ".join(
                        R.choice(
                            [
                                "Coast",
                                "COAST",
                                "coast",
                                "isn't",
                                "blue-green",
                                "Blue",
                                "red--blue",
                                "'coast'",
                                "!!",
                            ]
                        )
                        for _ in range(R.randrange(25))
                    )
                ]
            )
    boundary = {
        "second-largest-item-in-bst": [
            [[0, -2147483648, 2147483647]],
            [[0, -1, None, -2]],
        ],
        "balanced-binary-tree": [
            [[]],
            [[1, None, 2, None, 3, None, 4]],
            [[1, 2, 3, 4, None, None, None, 5]],
        ],
        "bst-checker": [
            [[]],
            [[-2147483648, None, 2147483647]],
            [[2147483647, -2147483648]],
            [[5, 3, 8, None, 6]],
        ],
        "nth-fibonacci": [[46], [1]],
        "cafe-order-checker": [
            [[8, 3], [5, 9], [8, 5, 3]],
            [[8, 3], [5, 9], [8, 5, 3, 9, 1000]],
            [[8, 3], [5, 9], [8, 5, 3, 3]],
            [[8, 3], [], [8, 3]],
            [[], [5, 9], [5, 9]],
            [[], [5, 9], [9, 5]],
            [[8, 3], [], [8]],
        ],
        "find-rotation-point": [[["a", "b", "c"]]],
        "graph-coloring": [
            [[[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], ["a", "b", "c", "d"]]
        ],
        "shuffle": [[[0, 1, 2, 3]], [[0]], [[0, 1, 2]]],
        "coin": [[0, [1, 2]], [100, [1, 5, 10, 25]]],
        "merging-ranges": [[[]], [[[1, 10], [2, 3], [3, 4], [10, 12]]]],
        "recursive-string-permutations": [["aab"], ["abcde"]],
        "temperature-tracker": [
            [
                [
                    "Insert",
                    "Insert",
                    "GetMode",
                    "GetMode",
                    "GetMean",
                    "GetMin",
                    "GetMax",
                ],
                [[0], [110], [], [], [], [], []],
            ]
        ],
        "cake-thief": [
            [[[0, 0], [2, 10000000000]], 6],
            [[[0, 0]], 0],
            [[[0, 1], [1, 0]], 0],
        ],
        "word-cloud": [
            ["A--B can't shouldn't re-enter RE-ENTER 'A'"],
            ["a-b-c a'b'c -dash trail- '' --"],
            ["a-" * 4999 + "a"],
        ],
    }
    extra.extend(boundary.get(slug, []))
    if mode == "files":
        common = "x" * 512
        collision = common[:90] + "Y" + common[91:]
        extra.extend(
            [
                [
                    [
                        {"path": "a", "content": "", "modified": 1},
                        {"path": "n/b", "content": "", "modified": 1},
                    ]
                ],
                [
                    [
                        {"path": "left/a", "content": "repeat", "modified": 500},
                        {"path": "right/b", "content": "repeat", "modified": 100},
                        {"path": "other", "content": "unique", "modified": 1},
                    ]
                ],
                [
                    [
                        {"path": "a", "content": common, "modified": 1},
                        {"path": "b", "content": collision, "modified": 2},
                    ]
                ],
                [
                    [
                        {
                            "path": "binary/a",
                            "base64": base64.b64encode(bytes(range(256)) * 2).decode(),
                            "modified": 2,
                        },
                        {
                            "path": "binary/b",
                            "base64": base64.b64encode(bytes(range(256)) * 2).decode(),
                            "modified": 3,
                        },
                    ]
                ],
            ]
        )
    rows = [{"arguments": a, "expected": oracle(s, a)} for a in args + extra]
    # Preserve chosen human-readable exemplars for any-valid outputs.
    for row, (_, expected) in zip(rows, s["examplesData"]):
        row["expected"] = expected
    return rows


if __name__ == "__main__":
    for s in S:
        rows = cases(s)
        (ROOT / "interviewcake/cases" / (s["id"] + ".json")).write_text(
            json.dumps(rows, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    print(
        "41 corpora:",
        sum(
            len(json.loads(p.read_text(encoding="utf-8")))
            for p in (ROOT / "interviewcake/cases").glob("*.json")
        ),
        "cases",
    )
