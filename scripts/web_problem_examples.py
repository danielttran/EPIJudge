"""Examples expressed in the public C# API, not internal tester return values.

Only 39 custom adapters need this translation. Derived outputs are checked
against their TSV property (where one exists) during catalog generation.
"""
import collections
import json


def compact(value):
    return json.dumps(value, ensure_ascii=False)


def example(value, output, explanation):
    return dict(Input=value, Output=output, Explanation=explanation)


def balanced_tree(values):
    def build(start, end):
        if start >= end:
            return None
        middle = start + (end - start) // 2
        return values[middle], build(start, middle), build(middle + 1, end)
    root = build(0, len(values))
    queue = collections.deque([root])
    result = []
    while queue:
        node = queue.popleft()
        result.append(None if node is None else node[0])
        if node is not None:
            queue.extend(node[1:])
    while result and result[-1] is None:
        result.pop()
    def height(node):
        return 0 if node is None else 1 + max(height(node[1]), height(node[2]))
    return result, height(root)


def custom_example(problem_id, fields):
    # Void TSV rows end in a description, not a JSON expected result.
    a = [json.loads(value) for value in fields]
    id = problem_id
    possible = 'One possible valid result is shown; other results satisfying the statement are accepted.'
    random_note = 'One possible output is shown. It must not be returned deterministically on every call: the judge checks repeated random samples.'
    if id == 'absent_value_array':
        present = set(a[0])
        result = next(i for i in range(len(present) + 1) if i not in present)
        return example('stream = ' + compact(a[0]), str(result), possible)
    if id in {'alternating_array', 'even_odd_array', 'dutch_national_flag', 'group_equal_entries'}:
        values = a[0]
        if id == 'alternating_array':
            output = sorted(values)
            for i in range(1, len(output) - 1, 2):
                output[i], output[i+1] = output[i+1], output[i]
            assert all(output[i-1] <= output[i] if i % 2 else output[i-1] >= output[i] for i in range(1, len(output)))
        elif id == 'even_odd_array':
            output = [v for v in values if v % 2 == 0] + [v for v in values if v % 2]
        elif id == 'group_equal_entries':
            output = sorted(values, key=lambda p: p[0])
        else:
            pivot = values[a[1]]
            output = [v for v in values if v < pivot] + [v for v in values if v == pivot] + [v for v in values if v > pivot]
        assert collections.Counter(map(compact, output)) == collections.Counter(map(compact, values))
        argument = 'people' if id == 'group_equal_entries' else 'values'
        prefix = f'pivotIndex = {a[1]}, ' if id == 'dutch_national_flag' else ''
        return example(prefix + argument + ' = ' + compact(values), argument + ' becomes ' + compact(output), 'The method returns void. ' + possible)
    if id == 'gray_code':
        output = [i ^ (i >> 1) for i in range(1 << a[0])]
        return example('numBits = ' + str(a[0]), compact(output), possible)
    if id == 'hanoi':
        if a[0] > 8:
            return example('numRings = ' + str(a[0]), 'A legal sequence of [sourcePeg, destinationPeg] moves.', 'Move every ring from peg 0 to peg 1 or peg 2.')
        output = []
        def move(n, start, finish, spare):
            if n:
                move(n-1, start, spare, finish)
                output.append([start, finish])
                move(n-1, spare, finish, start)
        move(a[0], 0, 1, 2)
        return example('numRings = ' + str(a[0]), compact(output), 'Each pair is a move, not a pair of ring sizes. ' + possible)
    if id == 'is_array_dominated':
        assert all(x < y for x, y in zip(sorted(a[0]), sorted(a[1]))) == a[2]
        return example('team0 = ' + compact(a[0]) + ', team1 = ' + compact(a[1]), compact(a[2]), 'This is ValidPlacementExists(team0, team1). The judge also calls the method with the teams reversed.')
    if id == 'is_string_decomposable_into_words':
        domain, dictionary, expected = a
        previous = [-1] * (len(domain) + 1)
        previous[0] = 0
        dictionary = set(dictionary)
        for end in range(1, len(domain)+1):
            for start in range(end):
                if previous[start] >= 0 and domain[start:end] in dictionary:
                    previous[end] = start
                    break
        result, end = [], len(domain)
        if previous[end] >= 0:
            while end:
                result.append(domain[previous[end]:end])
                end = previous[end]
            result.reverse()
        assert (''.join(result) == domain and all(w in dictionary for w in result)) == expected
        return example('domain = ' + compact(domain) + ', dictionary = ' + compact(a[1]), compact(result), possible if expected else 'No decomposition exists, so return an empty list. The test-data boolean is an expected property, not an argument to your method.')
    if id == 'search_entry_equal_to_index':
        result = next((i for i, x in enumerate(a[0]) if x == i), -1)
        return example('values = ' + compact(a[0]), str(result), possible)
    if id == 'refueling_schedule':
        gallons, distances = a
        tank, start = 0, 0
        for i in range(len(gallons)):
            tank += 20*gallons[i]-distances[i]
            if tank < 0:
                tank, start = 0, i+1
        start %= len(gallons)
        tank = 0
        for i in range(len(gallons)):
            city = (start+i) % len(gallons)
            tank += 20*gallons[city]-distances[city]
            assert tank >= 0
        return example('gallons = ' + compact(gallons) + ', distances = ' + compact(distances), str(start), possible)
    if id == 'run_length_compression':
        return example('encoded = ' + compact(a[0]) + ', decoded = ' + compact(a[1]), 'Decoding(encoded) = ' + compact(a[1]) + '; Encoding(decoded) = ' + compact(a[0]), 'The judge checks both methods. These are two calls, not one method with two arguments.')
    if id == 'string_integer_interconversion':
        return example('value = ' + str(a[0]) + ', text = ' + compact(a[1]), 'IntToString(value) = ' + compact(str(a[0])) + '; StringToInt(text) = ' + str(a[0]), 'The judge checks both methods independently.')
    if id == 'pivot_list':
        values, pivot = a
        output = [x for x in values if x < pivot] + [x for x in values if x == pivot] + [x for x in values if x > pivot]
        return example('head = ' + compact(values) + ', x = ' + str(pivot), compact(output), 'The output lists node Data values in the returned linked list. ' + possible)
    if id == 'is_list_cyclic':
        output = 'null' if a[1] == -1 else f'Reference to the node whose Data is {a[1]}.'
        setup = 'No cycle is added.' if a[1] == -1 else f'The tail links back to the node whose Data is {a[1]} (a value, not a position).'
        return example('head values = ' + compact(a[0]) + '; ' + setup, output, 'Return a node reference, not a value or a boolean.')
    if id in {'do_lists_overlap', 'do_terminated_lists_overlap'}:
        value = 'first prefix = ' + compact(a[0]) + ', second prefix = ' + compact(a[1]) + ', shared tail = ' + compact(a[2])
        if id == 'do_lists_overlap':
            value += f'; cycle positions = ({a[3]}, {a[4]})'
        output = 'null' if not a[2] else f'Reference to the shared-tail head (Data = {a[2][0]}).'
        return example(value, output, 'The judge attaches the shared tail by reference before calling OverlappingLists(first, second). For cyclic tests, positions are zero-based in the combined lists; -1 means no added cycle. Other shared nodes are also valid for the cyclic exercise.')
    if id == 'copy_posting_list':
        return example('posting list (Order, Jump target Order) = ' + compact(a[0]), 'A new list with the same structure: ' + compact(a[0]), 'Next follows the displayed sequence; Jump target -1 means null. Return the copied head. Every copied node and link must belong to the copy.')
    if id == 'graph_clone':
        return example('vertices = ' + str(a[0]) + ', directed edges = ' + compact(a[1]) + '; root = vertex 0', 'A distinct copy of every vertex and edge reachable from vertex 0.', 'The method receives the root GraphVertex. The vertex count and edge pairs describe how the judge builds that input graph.')
    if id in {'bst_from_sorted_array', 'sorted_list_to_bst'}:
        output, height = balanced_tree(a[0])
        if id == 'bst_from_sorted_array':
            assert height == a[1]
            value = 'values = ' + compact(a[0])
            explanation = f'One valid returned tree is shown in level order. Its height is {height}; the method returns its root, not the height.'
        else:
            value = 'head = doubly linked sequence ' + compact(a[0]) + ', count = ' + str(len(a[0]))
            explanation = 'One valid returned tree is shown in level order. Input Left/Right links represent previous/next; output links represent tree children.'
        return example(value, compact(output), explanation)
    if id == 'sudoku_solve':
        return example('board = ' + compact(a[0]), 'Fill all zeros with a valid Sudoku completion without changing any nonzero clue.', 'The C# method returns void; the judge examines the mutated board.')
    if id in {'adding_credits', 'lru_cache', 'circular_queue', 'queue_from_stacks', 'queue_with_max', 'stack_with_max'}:
        return example('command sequence = ' + compact(a[0]), 'All recorded operation results match their expected values.', 'This is a sequence of calls to the displayed API. Constructor commands mean Initialize. For query/removal commands, the extra command fields record expected return values; they are not additional method arguments.')
    if id in {'nonuniform_random_number', 'uniform_random_number', 'random_permutation', 'random_subset', 'offline_sampling', 'online_sampling'}:
        if id == 'nonuniform_random_number':
            return example('values = ' + compact(a[0]) + ', probabilities = ' + compact(a[1]), 'A randomly chosen values[i], with probability probabilities[i].', 'There is no single fixed expected sample. The judge checks repeated draws against the supplied distribution.')
        if id == 'uniform_random_number':
            return example(f'lower = {a[0]}, upper = {a[1]}', f'Any integer from {a[0]} through {a[1]}, inclusive.', 'There is no single fixed expected sample; repeated calls must be uniform and independent.')
        if id == 'random_permutation':
            note = 'Only one permutation exists for this input, so every call returns it.' if a[0] <= 1 else random_note
            return example('n = ' + str(a[0]), compact(list(range(a[0]))), note)
        if id == 'random_subset':
            note = 'Only one subset exists for this input, so its membership is fixed.' if a[1] in (0, a[0]) else random_note
            return example(f'n = {a[0]}, k = {a[1]}', compact(list(range(a[1]))), note)
        if id == 'online_sampling':
            note = 'Only one subset exists for this input, so its membership is fixed.' if a[1] in (0, len(a[0])) else random_note
            return example('stream = ' + compact(a[0]) + ', k = ' + str(a[1]), compact(a[0][:a[1]]), note)
        return example('k = ' + str(a[0]) + ', values = ' + compact(a[1]), 'values may become ' + compact(a[1]), 'The method returns void. In this possible arrangement, the first k entries are the selected sample. Every k-element subset must be equally likely across repeated calls.')
    if id == 'bst_to_sorted_list':
        return example('tree = ' + compact(a[0]), 'List head with forward Data sequence ' + compact(a[1]), 'Right follows the sorted sequence; Left links to the previous node. The returned head has Left = null.')
    if id == 'tree_right_sibling':
        return example('tree = ' + compact(a[0]), 'Next chains by level: ' + compact(a[1]), 'The method returns void. These lists show the Data values reached by following Next on each level after the mutation.')
    if id == 'search_maze':
        maze, start, end, expected = a
        start, end = tuple(start), tuple(end)
        previous = {start: None} if maze[start[0]][start[1]] == 0 else {}
        queue = collections.deque(previous)
        while queue and end not in previous:
            r, c = queue.popleft()
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                point = r+dr, c+dc
                rr, cc = point
                if 0 <= rr < len(maze) and 0 <= cc < len(maze[rr]) and maze[rr][cc] == 0 and point not in previous:
                    previous[point] = r,c
                    queue.append(point)
        path = []
        if end in previous:
            point = end
            while point is not None:
                path.append(point)
                point = previous[point]
            path.reverse()
        assert (bool(path) or start == end) == expected
        return example('maze = ' + compact(maze) + ', start = ' + compact(start) + ', end = ' + compact(end), compact(path), 'Return coordinates, not a path-existence boolean. ' + possible)
    if id in {'smallest_subarray_covering_set', 'smallest_subarray_covering_all_values'}:
        paragraph, keywords, expected_length = a
        best = None
        for start in range(len(paragraph)):
            needed, k = set(keywords), 0
            for end in range(start, len(paragraph)):
                needed.discard(paragraph[end])
                if k < len(keywords) and paragraph[end] == keywords[k]:
                    k += 1
                if (not needed if id.endswith('_set') else k == len(keywords)):
                    if best is None or end-start < best[1]-best[0]:
                        best = start,end
                    break
        assert best is not None and best[1]-best[0]+1 == expected_length
        return example('paragraph = ' + compact(paragraph) + ', keywords = ' + compact(keywords), compact(best), f'These are inclusive zero-based indices. The covered slice has length {expected_length}; your method returns the pair, not that length. ' + possible)
    raise ValueError('Missing C# example translation: ' + id)
