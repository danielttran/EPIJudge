"""Bank-owned typed adapter with identity, state, filesystem and random properties."""

import contextlib
import hashlib
import io
import json
import math
import pathlib
import time

import solution as user

ClassName: str = ""
Method: str = ""
Kinds: list[str] = []
Result: str = ""
Mode: str = ""


# CONFIGURATION
class ContractError(Exception):
    pass


class NeedChoice(Exception):
    def __init__(self, lower, upper):
        self.lower, self.upper = lower, upper


def check(ok, message="The result violates the bank contract."):
    if not ok:
        raise ContractError(message)


def fresh():
    return getattr(user, ClassName)()


def call(instance, method, *args):
    return getattr(instance, method)(*args)


def typed_result(value, kind):
    """Reject Python values that cannot satisfy the displayed typed API."""
    if kind == "void":
        check(value is None, "A void method must return None.")
    elif kind in ("i", "l"):
        check(
            type(value) is int, "Return an integer, not a bool or floating-point value."
        )
    elif kind == "b":
        check(type(value) is bool, "Return a boolean.")
    elif kind == "s":
        check(type(value) is str, "Return a string.")
    elif kind == "ai":
        check(
            type(value) is list and all(type(v) is int for v in value),
            "Return a list of integers.",
        )
    elif kind == "as":
        check(
            value is None or type(value) is list and all(type(v) is str for v in value),
            "Return None or a list of strings.",
        )
    elif kind == "set":
        check(
            type(value) is set and all(type(v) is str for v in value),
            "Return a set of strings.",
        )
    elif kind == "map":
        check(
            type(value) is dict
            and all(type(k) is str and type(v) is int for k, v in value.items()),
            "Return a string-to-integer dictionary.",
        )
    elif kind == "meetings":
        check(
            type(value) is list and all(isinstance(v, user.Meeting) for v in value),
            "Return a list of meeting objects.",
        )
        check(
            all(type(v.StartTime) is int and type(v.EndTime) is int for v in value),
            "Meeting endpoints must be integers.",
        )
    elif kind == "rect":
        check(isinstance(value, user.Rectangle), "Return a rectangle object.")
        check(
            all(
                type(getattr(value, field)) is int
                for field in ("LeftX", "BottomY", "Width", "Height")
            ),
            "Rectangle fields must be integers.",
        )
    elif kind == "pairs":
        check(
            type(value) is list and all(isinstance(v, user.FilePaths) for v in value),
            "Return a list of file-path pairs.",
        )
        check(
            all(
                type(v.OriginalPath) is str and type(v.DuplicatePath) is str
                for v in value
            ),
            "File paths must be strings.",
        )
    return value


def container_snapshot(value):
    """Keep identity as well as content for every read-only nested container."""
    if isinstance(value, list):
        return ("list", id(value), tuple(container_snapshot(v) for v in value))
    if isinstance(value, dict):
        return (
            "dict",
            id(value),
            tuple(sorted((k, container_snapshot(v)) for k, v in value.items())),
        )
    if isinstance(value, (user.Meeting, user.CakeType, user.Rectangle)):
        return (type(value).__name__, id(value), tuple(sorted(vars(value).items())))
    return (type(value), value)


def load(value, kind):
    if kind == "tree":
        if not value:
            return None
        root = user.BinaryTreeNode(value[0])
        q = [root]
        i = 1
        for n in q:
            for field in ("Left", "Right"):
                if i < len(value) and value[i] is not None:
                    child = user.BinaryTreeNode(value[i])
                    setattr(n, field, child)
                    q.append(child)
                i += 1
        return root
    if kind == "list":
        head = None
        for v in reversed(value):
            head = user.LinkedListNode(v, head)
        return head
    if kind == "graph":
        nodes = [user.GraphNode("v" + str(i)) for i in range(len(value))]
        for n, neighbors in zip(nodes, value):
            n.Neighbors = {nodes[j] for j in neighbors}
        return nodes
    if kind == "meetings":
        return [user.Meeting(*v) for v in value]
    if kind == "rect":
        return user.Rectangle(*value)
    if kind == "cakes":
        return [user.CakeType(*v) for v in value]
    if kind == "chars":
        return list(value)
    return value


def list_nodes(head):
    nodes = []
    seen = set()
    while head is not None:
        check(id(head) not in seen, "Output list contains a cycle.")
        seen.add(id(head))
        nodes.append(head)
        head = head.Next
    return nodes


def tree_nodes(root):
    nodes = []
    seen = set()
    q = [] if root is None else [root]
    while q:
        n = q.pop()
        check(id(n) not in seen, "Input must remain a tree.")
        seen.add(id(n))
        nodes.append(n)
        if n.Left is not None:
            q.append(n.Left)
        if n.Right is not None:
            q.append(n.Right)
    return nodes


def dump(value, kind=""):
    if value is None:
        return [] if kind == "list" else None
    if kind == "tree":
        return [
            [n.Value, id(n.Left) if n.Left else None, id(n.Right) if n.Right else None]
            for n in tree_nodes(value)
        ]
    if kind == "list":
        return [n.Value for n in list_nodes(value)]
    if kind == "meetings":
        return [[n.StartTime, n.EndTime] for n in value]
    if kind == "rect":
        return [value.LeftX, value.BottomY, value.Width, value.Height]
    if kind == "cakes":
        return [[n.Weight, n.Value] for n in value]
    if kind == "chars":
        return "".join(value)
    if kind == "pairs":
        return [[n.OriginalPath, n.DuplicatePath] for n in value]
    if isinstance(value, set):
        return sorted(value)
    return value


def preserve(args):
    trees = [n for v, k in zip(args, Kinds) if k == "tree" for n in tree_nodes(v)]
    lists = [n for v, k in zip(args, Kinds) if k == "list" for n in list_nodes(v)]
    tv = [(n.Value, n.Left, n.Right) for n in trees]
    lv = [(n.Value, n.Next) for n in lists]
    before = [json.dumps(dump(v, k), sort_keys=True) for v, k in zip(args, Kinds)]
    containers = [
        container_snapshot(v) for v, k in zip(args, Kinds) if k not in ("tree", "list")
    ]

    def verify():
        check(
            all((n.Value, n.Left, n.Right) == v for n, v in zip(trees, tv)),
            "Tree values and links must remain unchanged.",
        )
        check(
            all((n.Value, n.Next) == v for n, v in zip(lists, lv)),
            "List values and links must remain unchanged.",
        )
        check(
            [json.dumps(dump(v, k), sort_keys=True) for v, k in zip(args, Kinds)]
            == before,
            "Read-only input was modified.",
        )
        check(
            [
                container_snapshot(v)
                for v, k in zip(args, Kinds)
                if k not in ("tree", "list")
            ]
            == containers,
            "Read-only input objects and nested containers must retain their identity.",
        )

    return verify


def fs_snapshot(root):
    entries = []
    for p in sorted(pathlib.Path(root).rglob("*")):
        entries.append(
            ("D", str(p.relative_to(root)))
            if p.is_dir()
            else (
                "F",
                str(p.relative_to(root)),
                p.stat().st_mtime_ns,
                hashlib.sha256(p.read_bytes()).hexdigest(),
            )
        )
    return entries


def state(raw):
    obj = fresh()
    output = []
    count = 0
    for method, args in zip(*raw):
        empty = count == 0 and (
            Mode == "queue"
            and method == "Dequeue"
            or Mode == "stack"
            and method in ("Pop", "GetMax")
        )
        try:
            value = call(obj, method, *args)
            check(not empty, "Empty-state operation must signal an error.")
            if method in ("Enqueue", "Push", "Insert"):
                typed_result(value, "void")
            elif method in ("Dequeue", "Pop", "GetMax") and Mode in ("queue", "stack"):
                typed_result(value, "i")
            elif method == "AddWord":
                typed_result(value, "b")
            elif method in ("GetMin", "GetMax", "GetMode"):
                check(
                    value is None or type(value) is int,
                    "Return None or an integer statistic.",
                )
            elif method == "GetMean":
                check(
                    value is None
                    or type(value) in (int, float)
                    and math.isfinite(value),
                    "Return None or a finite numeric mean.",
                )
            output.append(value)
        except (ContractError, NeedChoice):
            raise
        except Exception:
            if not empty:
                raise
            output.append({"error": "empty"})
        if method in ("Enqueue", "Push"):
            count += 1
        elif method in ("Dequeue", "Pop") and not empty:
            count -= 1
    return output


def random_check(raw):
    shuffle = Mode == "shuffle"
    maximum = 7 if Mode == "rand5" else 5
    outcomes = 5 if Mode == "rand5" else 7
    original = list(raw[0]) if shuffle else []
    probabilities = {}
    unresolved = 0.0
    branches = 0
    pending = [([], 1.0)]
    while pending:
        prefix, weight = pending.pop()
        position = 0
        draws = 0
        branches += 1
        check(branches <= 100000, "Too many random decision branches.")

        def draw(lower, upper, choices=prefix):
            nonlocal position, draws
            draws += 1
            check(draws <= 128, "Randomized algorithm exceeded draw budget.")
            check(
                lower <= upper
                and (
                    0 <= lower <= upper < max(1, len(original))
                    if shuffle
                    else lower == 1 and upper == maximum
                ),
                "Unexpected random-source bounds.",
            )
            if position >= len(choices):
                raise NeedChoice(lower, upper)
            result = choices[position]
            position += 1
            check(lower <= result <= upper, "Invalid injected choice.")
            return result

        user.RandomSource.Draw = staticmethod(draw)
        a = list(original)
        try:
            result = call(fresh(), Method, a) if shuffle else call(fresh(), Method)
            if shuffle:
                typed_result(result, "void")
                check(
                    sorted(a) == sorted(original),
                    "Shuffle changed element multiplicities.",
                )
                result = tuple(a)
            else:
                check(
                    draws > 0 and type(result) is int and 1 <= result <= outcomes,
                    "Invalid die result or source usage.",
                )
                if Mode == "rand7":
                    check(draws % 2 == 0, "Rand7 must use two Rand5 draws per attempt.")
            probabilities[result] = probabilities.get(result, 0.0) + weight
        except NeedChoice as next_choice:
            limit = max(8, 2 * len(original)) if shuffle else 8
            if len(prefix) >= limit:
                unresolved += weight
                continue
            for choice in range(next_choice.lower, next_choice.upper + 1):
                pending.append(
                    (
                        prefix + [choice],
                        weight / (next_choice.upper - next_choice.lower + 1),
                    )
                )
    if shuffle:
        if len(set(original)) == len(original) and len(original) <= 5:
            factorial = math.factorial(len(original))
            check(
                unresolved < 1e-10
                and len(probabilities) == factorial
                and all(abs(p - 1 / factorial) < 1e-9 for p in probabilities.values()),
                "Shuffle is biased over full permutations.",
            )
    else:
        check(
            unresolved < 0.02,
            "Rejection probability exceeds bounded judge exploration.",
        )
        for result in range(1, outcomes + 1):
            p = probabilities.get(result, 0.0)
            check(
                p <= 1 / outcomes + 1e-9 and p + unresolved >= 1 / outcomes - 1e-9,
                "Die transformation is biased over injected choices.",
            )
    seed = 0x85EBCA6B
    counts = [0] * (outcomes + 1)
    pairs = [0] * (outcomes**2)
    triples = [0] * (outcomes**3)
    previous = earlier = None
    samples = 4096
    instance = fresh()
    permutation_counts = {}
    score_permutations = (
        shuffle and len(original) <= 5 and len(set(original)) == len(original)
    )
    for trial in range(samples):
        draws = 0
        forced_prefix = raw[0] if not shuffle and trial == 0 else []

        def draw(lower, upper, choices=forced_prefix):
            nonlocal draws, seed
            draws += 1
            check(draws <= 128, "Too many random draws.")
            check(
                lower <= upper
                and (
                    0 <= lower <= upper < max(1, len(original))
                    if shuffle
                    else lower == 1 and upper == maximum
                ),
                "Unexpected random-source bounds.",
            )
            if draws <= len(choices):
                result = choices[draws - 1]
                check(
                    type(result) is int and lower <= result <= upper,
                    "Invalid forced source prefix.",
                )
                return result
            seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
            return lower + (seed * (upper - lower + 1) >> 32)

        user.RandomSource.Draw = staticmethod(draw)
        a = list(original)
        result = call(instance, Method, a) if shuffle else call(instance, Method)
        if shuffle:
            typed_result(result, "void")
            check(sorted(a) == sorted(original), "Shuffle changed elements.")
            if len(a) > 1:
                check(draws > 0, "Use supplied random source.")
            if score_permutations:
                permutation = tuple(a)
                permutation_counts[permutation] = (
                    permutation_counts.get(permutation, 0) + 1
                )
        else:
            check(
                draws > 0 and type(result) is int and 1 <= result <= outcomes,
                "Invalid die result/source usage.",
            )
            if Mode == "rand7":
                check(draws % 2 == 0, "Rand7 must use two Rand5 draws per attempt.")
            counts[result] += 1
            if previous is not None:
                pairs[(previous - 1) * outcomes + result - 1] += 1
            if earlier is not None:
                triples[
                    ((earlier - 1) * outcomes + previous - 1) * outcomes + result - 1
                ] += 1
            earlier, previous = previous, result
    if score_permutations:
        bins = math.factorial(len(original))
        expected = samples / bins
        check(
            len(permutation_counts) == bins, "Seeded shuffle omitted some permutations."
        )
        statistic = sum(
            (count - expected) ** 2 / expected for count in permutation_counts.values()
        )
        check(
            statistic <= 4 * (bins - 1) + 80,
            "Seeded shuffle permutations are biased across calls.",
        )
    if not shuffle:
        expected = samples / outcomes
        check(
            sum((c - expected) ** 2 / expected for c in counts[1:]) < 40,
            "Seeded die distribution is biased.",
        )
        for length, frequencies in ((2, pairs), (3, triples)):
            bins = outcomes**length
            expected = (samples - length + 1) / bins
            statistic = sum((count - expected) ** 2 / expected for count in frequencies)
            check(
                statistic < 4 * (bins - 1) + 80,
                f"Seeded adjacent {length}-draw outcomes are correlated.",
            )
    return True


def execute(raw):
    if Mode in ("queue", "stack", "trie", "temperature"):
        return state(raw)
    if Mode == "wordcloud":
        return typed_result(getattr(user, ClassName)(raw[0]).WordsToCounts, "map")
    if Mode in ("shuffle", "rand5", "rand7"):
        return random_check(raw)
    if Mode == "cycle":
        head = load(raw[0], "list")
        nodes = list_nodes(head)
        if raw[1] >= 0:
            nodes[-1].Next = nodes[raw[1]]
        before = [(n.Value, n.Next) for n in nodes]
        result = call(fresh(), Method, head)
        check(
            all((n.Value, n.Next) == v for n, v in zip(nodes, before)),
            "Cycle detection modified list.",
        )
        return typed_result(result, "b")
    if Mode == "delete":
        head = load(raw[0], "list")
        nodes = list_nodes(head)
        before = [(n.Value, n.Next) for n in nodes]
        index = raw[1]
        typed_result(call(fresh(), Method, nodes[index]), "void")
        check(
            all(
                (n.Value, n.Next) == before[index + 1 if i == index else i]
                for i, n in enumerate(nodes)
            ),
            "Deletion violated target/successor alias semantics.",
        )
        return dump(head, "list")
    if Mode == "reverse_list":
        head = load(raw[0], "list")
        nodes = list_nodes(head)
        values = [n.Value for n in nodes]
        result = call(fresh(), Method, head)
        after = list_nodes(result)
        check(
            len(after) == len(nodes)
            and all(x is y for x, y in zip(after, reversed(nodes)))
            and [n.Value for n in nodes] == values,
            "Reversal must reuse original nodes in reverse order.",
        )
        return dump(result, "list")
    args = [load(v, k) for v, k in zip(raw, Kinds)]
    if Mode in ("chars", "words"):
        a = args[0]
        typed_result(call(fresh(), Method, *args), "void")
        check(len(a) == len(raw[0]), "Array length changed.")
        check(
            all(type(char) is str and len(char) == 1 for char in a),
            "Return one character per array entry.",
        )
        return "".join(a)
    if Mode == "color":
        nodes, colors = args
        original_nodes = list(nodes)
        edge_objects = [n.Neighbors for n in nodes]
        edges = [set(n.Neighbors) for n in nodes]
        labels = [n.Label for n in nodes]
        palette = list(colors)
        typed_result(call(fresh(), Method, *args), "void")
        check(
            len(nodes) == len(original_nodes)
            and all(n is old for n, old in zip(nodes, original_nodes)),
            "Graph nodes and their order must remain unchanged.",
        )
        check(
            all(
                n.Label == label
                and n.Neighbors is edge_object
                and n.Neighbors == edge
                and n.Color in palette
                and all(n.Color != x.Color for x in n.Neighbors)
                for n, label, edge, edge_object in zip(
                    nodes, labels, edges, edge_objects
                )
            ),
            "Invalid coloring or graph mutation.",
        )
        check(colors == palette, "Palette was modified.")
        return True
    verify = preserve(args)
    files_before = fs_snapshot(args[0]) if Mode == "files" else None
    try:
        result = call(fresh(), Method, *args)
    except user.InfinityException:
        verify()
        return {"error": "infinite"}
    verify()
    if Mode == "files":
        check(fs_snapshot(args[0]) == files_before, "Filesystem must remain unchanged.")
        return dump(typed_result(result, "pairs"), "pairs")
    if Mode == "kth":
        nodes = list_nodes(args[1])
        index = next((i for i, n in enumerate(nodes) if n is result), -1)
        check(index >= 0, "Return original node reference.")
        return index
    typed_result(result, Result)
    if Mode == "meetings":
        check(
            result is not args[0]
            and all(all(n is not old for old in args[0]) for n in result),
            "Return new interval objects.",
        )
    if Mode == "rect":
        check(
            isinstance(result, user.Rectangle) and all(result is not v for v in args),
            "Return new rectangle.",
        )
    if Result == "ai":
        check(
            isinstance(result, list) and all(result is not v for v in args),
            "Return newly allocated result array.",
        )
    return dump(result, Result)


output = []
for raw in json.loads(pathlib.Path("cases.json").read_text()):
    start = time.perf_counter()
    actual = error = None
    validation = False
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            actual = execute(raw)
        # Keep malformed user output local to its case instead of aborting the
        # complete report when the final JSON file is serialized.
        json.dumps(actual, allow_nan=False)
    except ContractError as ex:
        validation = True
        error = str(ex)
    except Exception as ex:  # noqa: BLE001 - isolate arbitrary user exceptions per case.
        actual = None
        error = type(ex).__name__ + ": " + str(ex)
    output.append(
        {
            "Actual": actual,
            "Error": error,
            "ValidationFailed": validation,
            "ElapsedMs": (time.perf_counter() - start) * 1000,
        }
    )
pathlib.Path("results.json").write_text(json.dumps(output))
