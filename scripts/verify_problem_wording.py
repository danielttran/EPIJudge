"""Check wording provenance, example translations, and sensitive conventions.

Run: python scripts/verify_problem_wording.py
Reference functions are loaded from the original source without importing its
test runner or third party dependencies. This does not modify the test corpus.
"""
import ast
import collections
import functools
import heapq
import itertools
import json
import math
import operator
import string
from pathlib import Path

from generate_web_catalog import CUSTOM, ROOT, source_hash
from web_problem_examples import balanced_tree, custom_example


def rows(id, argument_count):
    lines = (ROOT/'test_data'/f'{id}.tsv').read_text(encoding='utf-8').splitlines()
    is_void = lines[0].split('\t')[-1] == 'void'
    for line in lines[1:]:
        fields = line.split('\t')
        yield [json.loads(x) for x in fields[:argument_count]], None if is_void else json.loads(fields[argument_count])


def reference(file, name, extras=None):
    namespace = dict(collections=collections, functools=functools, heapq=heapq,
                     itertools=itertools, math=math, operator=operator, string=string)
    namespace.update(extras or {})
    tree = ast.parse((ROOT/'epi_judge_python_solutions'/file).read_text(encoding='utf-8'))
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == name]
    assert len(nodes) == 1, (file, name)
    nodes[0].decorator_list = []
    module = ast.Module(body=nodes, type_ignores=[])
    exec('from __future__ import annotations\n' + ast.unparse(module), namespace)
    return namespace[name]


def matches(actual, expected):
    if isinstance(actual, (list, tuple)):
        return isinstance(expected, (list, tuple)) and len(actual) == len(expected) and all(matches(a, b) for a, b in zip(actual, expected))
    if isinstance(actual, float) or isinstance(expected, float):
        return math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
    return actual == expected


def main():
    provenance = json.loads((ROOT/'docs/problem-wording-sources.json').read_text(encoding='utf-8'))
    canonical = json.loads((ROOT/'scripts/problem_catalog.json').read_text(encoding='utf-8'))['problems']
    catalog = json.loads((ROOT/'EpiJudge.Runner/catalog.json').read_text(encoding='utf-8'))
    by_id = {p['Id']: p for p in catalog}
    assert len(provenance['problems']) == 218
    assert {p['id'] for p in provenance['problems']} == {p['id'] for p in canonical}
    for path, digest in provenance['statementFiles'].items():
        assert source_hash(ROOT/path) == digest, 'Regenerate stale statement provenance: ' + path
    for p in provenance['problems']:
        assert source_hash(ROOT/p['testDataFile']) == p['testDataSha256'], p['id']
        for f in p['referenceFiles']:
            assert source_hash(ROOT/f['path']) == f['sha256'], f['path']
            assert p['id']+'.tsv' in (ROOT/f['path']).read_text(), p['id']
    assert all(p['Difficulty'] == 'Unrated' for p in catalog)
    curated = (ROOT/'EpiJudge.Runner/ProblemCatalog.cs').read_text()
    assert '"Easy"' not in curated and '"Medium"' not in curated
    assert all(p['Examples'] for p in catalog)
    translated = 0
    for p in canonical:
        if p['id'] not in CUSTOM:
            continue
        count = len(p['argumentTypes'])
        lines = (ROOT/'test_data'/p['testDataFile']).read_text().splitlines()[1:]
        expected_examples = []
        for line in lines[:2]:
            fields = line.split('\t')
            if sum(map(len, fields[:count+1])) > 2500:
                continue
            expected_examples.append(custom_example(p['id'], fields[:count] if p['resultType']=='void' else fields[:count+1]))
        if expected_examples:
            assert expected_examples == by_id[p['id']]['Examples'], p['id']
            translated += len(expected_examples)
    print(f'PASS provenance for all 218 problems; {translated} translated C# examples')

    checked = 0
    def compare(id, arity, function, transform=None):
        nonlocal checked
        count = 0
        for args, expected in rows(id, arity):
            actual = function(*args) if transform is None else transform(function, args)
            assert matches(actual, expected), f'{id}: actual={str(actual)[:200]}, expected={str(expected)[:200]}'
            checked += 1
            count += 1
        print(f'PASS {id}: {count} reference cases')

    symbol = collections.namedtuple('CharWithFrequency', ['c', 'freq'])
    huffman = reference('huffman_coding.py', 'huffman_encoding', dict(CharWithFrequency=symbol))
    compare('huffman_coding', 1, huffman, lambda fn, args: fn([symbol(*x) for x in args[0]]))
    compare('left_right_justify_text', 2, reference('left_right_justify_text.py', 'justify_text'))
    compare('find_salary_threshold', 2, reference('find_salary_threshold.py', 'find_salary_cap'))
    compare('roman_to_integer', 1, reference('roman_to_integer.py', 'roman_to_integer'))
    compare('substring_match', 2, reference('substring_match.py', 'rabin_karp'))
    def reverse_words(fn, args):
        characters = list(args[0])
        fn(characters)
        return ''.join(characters)
    compare('reverse_words', 1, reference('reverse_words.py', 'reverse_words'), reverse_words)
    paired = collections.namedtuple('PairedTasks', ['task_1', 'task_2'])
    compare('task_pairing', 1, reference('task_pairing.py', 'optimum_task_assignment', dict(PairedTasks=paired)))
    queue = reference('queue_with_max_using_deque.py', 'QueueWithMax')
    traffic = reference('max_of_sliding_window.py', 'TrafficElement')
    window = reference('max_of_sliding_window.py', 'calculate_traffic_volumes', dict(QueueWithMax=queue, TrafficElement=traffic))
    compare('max_of_sliding_window', 2, window,
            lambda fn, args: [(v.time, v.volume) for v in fn([traffic(*x) for x in args[0]], args[1])])

    # A plain tree decoder lets the source's documented midpoint construction be
    # checked against every exact expected shape in the merge corpus.
    def inorder(values):
        if not values or values[0] is None:
            return []
        root = [values[0], None, None]
        queue = collections.deque([root])
        index = 1
        while queue and index < len(values):
            node = queue.popleft()
            for child in (1, 2):
                if index < len(values) and values[index] is not None:
                    node[child] = [values[index], None, None]
                    queue.append(node[child])
                index += 1
        def visit(node):
            return [] if node is None else visit(node[1]) + [node[0]] + visit(node[2])
        return visit(root)
    compare('bst_merge', 2, lambda a, b: balanced_tree(sorted(inorder(a)+inorder(b)))[0])

    for id in ('search_entry_equal_to_index', 'search_unknown_length_array'):
        arity = 1 if id == 'search_entry_equal_to_index' else 2
        for args, _ in rows(id, arity):
            assert all(x < y for x, y in zip(args[0], args[0][1:])), id
            checked += 1
    for args, _ in rows('smallest_subarray_covering_all_values', 2):
        assert len(set(args[1])) == len(args[1]), 'Repeated sequential keywords in corpus'
        checked += 1
    for args, _ in rows('two_sorted_arrays_merge', 4):
        assert len(args[0]) == args[1]+args[3]
        checked += 1
    for line in (ROOT/'test_data/is_array_dominated.tsv').read_text().splitlines()[1:]:
        fields = line.split('\t')
        assert len(json.loads(fields[0])) == len(json.loads(fields[1]))
        checked += 1
    # Verify the source's actual mapping rather than assuming a convention.
    tree = ast.parse((ROOT/'epi_judge_python_solutions/phone_number_mnemonic.py').read_text())
    mapping = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='MAPPING' for t in n.targets))
    assert mapping == ('0','1','ABC','DEF','GHI','JKL','MNO','PQRS','TUV','WXYZ')
    for args, expected in rows('phone_number_mnemonic', 1):
        digits = args[0]
        assert len(expected) == math.prod(len(mapping[int(d)]) for d in digits)
        assert len(set(expected)) == len(expected)
        assert all(len(word)==len(digits) and all(c in mapping[int(d)] for c, d in zip(word, digits)) for word in expected)
        checked += 1
    print(f'PASS wording-sensitive semantics and preconditions: {checked} corpus cases')
    transform = reference('string_transformability.py', 'transform_string')
    assert transform({'cat','cot','cog','dog'}, 'cat', 'dog') == 3
    rectangle = collections.namedtuple('Rect', ['left','right','height'])
    skyline = reference('drawing_skyline.py', 'compute_skyline', dict(Rect=rectangle))
    assert matches(skyline([rectangle(1,3,2),rectangle(2,4,3)]), [[1,1,2],[2,4,3]])
    assert min(max(values)-min(values) for values in itertools.product([1,4],[2,5],[3,6])) == 2
    assert 2 not in [0,1,3] and 0 <= 2 <= 2**31-1
    assert (-1 & 0xffffffff).bit_count() == 32
    normalize = reference('directory_path_normalization.py', 'shortest_equivalent_path')
    assert normalize('a/..') == '' and normalize('/a/..') == '/' and normalize('../../a') == '../../a'
    two_sum = reference('two_sum.py', 'has_two_sum')
    assert two_sum([-2,1,2,4,7,11],6) and two_sum([3],6)
    anagrams = reference('anagrams.py', 'find_anagrams')
    assert sorted(map(sorted, anagrams(['eat','tea','tan','ate']))) == [sorted(['eat','tea','ate'])]
    print('PASS the four illustrative examples and the curated examples')


if __name__ == '__main__':
    main()
