"""Build reviewed practice guidance; never infer tags from titles or keywords.

Group assignments are explicit: they describe one supported approach, not every
possible solution. The final hint reuses the independently authored C# strategy
paragraph (without language-specific notes), not code or an upstream statement.
"""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
GROUPS = {
'Bit manipulation': '''count_bits parity swap_bits reverse_bits closest_int_same_weight primitive_multiply primitive_divide element_appearing_once gray_code blind75_missing_number blind75_number_of_1_bits blind75_reverse_bits blind75_sum_of_two_integers interviewcake_find-unique-int-among-duplicates ctci6_5_1 ctci6_5_4 ctci6_5_6 ctci6_5_7 ctci6_5_8 ctci6_16_1 ctci6_16_7 ctci6_17_1 ctci6_17_4 ctci6_17_19''',
'Two pointers': '''two_sum three_sum task_pairing max_trapped_water max_water_trappable intersect_sorted_arrays two_sorted_arrays_merge is_string_palindromic is_string_palindromic_punctuation reverse_words blind75_3sum blind75_container_with_most_water blind75_longest_palindromic_substring blind75_palindromic_substrings interviewcake_cafe-order-checker interviewcake_merge-sorted-arrays interviewcake_reverse-string-in-place interviewcake_reverse-words ctci6_1_3 ctci6_1_5 ctci6_2_6 ctci6_10_1 ctci6_16_6 ctci6_16_24 ctci6_17_21''',
'Hashing and counting': '''anagrams is_string_permutable_to_palindrome is_anonymous_letter_constructible nearest_repeated_entries longest_contained_interval search_frequent_items absent_value_array find_missing_and_duplicate remove_duplicates group_equal_entries h_index blind75_two_sum blind75_contains_duplicate blind75_top_k_frequent_elements blind75_longest_consecutive_sequence blind75_group_anagrams interviewcake_find-duplicate-files interviewcake_inflight-entertainment interviewcake_permutation-palindrome interviewcake_temperature-tracker interviewcake_top-scores interviewcake_word-cloud ctci6_1_1 ctci6_1_2 ctci6_1_4 ctci6_7_12 ctci6_16_2 ctci6_16_15 ctci6_16_21 ctci6_17_26''',
'Linked-list rewiring': '''reverse_list zip_list delete_from_list insert_in_list sorted_lists_merge reverse_sublist delete_node_from_list remove_duplicates_from_sorted_list list_cyclic_right_shift even_odd_list_merge is_list_palindromic pivot_list blind75_reverse_linked_list blind75_merge_two_sorted_lists blind75_reorder_list interviewcake_delete-node interviewcake_reverse-linked-list ctci6_2_1 ctci6_2_3 ctci6_2_4''',
'Fast and slow pointers': '''is_list_cyclic blind75_linked_list_cycle interviewcake_linked-list-cycles interviewcake_find-duplicate-optimize-for-space-beast-mode ctci6_2_8''',
'Pointer alignment': '''do_terminated_lists_overlap delete_kth_last_from_list blind75_remove_nth_node_from_end_of_list interviewcake_kth-to-last-node-in-singly-linked-list ctci6_2_2 ctci6_2_7 ctci6_4_8''',
'Identity mapping': '''do_lists_overlap copy_posting_list graph_clone blind75_clone_graph lowest_common_ancestor''',
'Tree traversal': '''tree_postorder tree_preorder is_tree_balanced is_tree_symmetric sum_root_to_leaf path_sum tree_inorder kth_node_in_tree successor_in_tree tree_with_parent_inorder tree_from_preorder_inorder tree_from_preorder_with_null tree_connect_leaves tree_exterior tree_right_sibling sorted_list_to_bst bst_to_sorted_list blind75_invert_binary_tree blind75_maximum_depth_of_binary_tree blind75_same_tree blind75_subtree_of_another_tree blind75_construct_binary_tree_from_preorder_and_inorder_traversal blind75_binary_tree_maximum_path_sum blind75_serialize_and_deserialize_binary_tree interviewcake_balanced-binary-tree ctci6_4_4 ctci6_4_6 ctci6_16_12 ctci6_17_12''',
'Binary search tree': '''search_in_bst is_tree_a_bst search_first_greater_value_in_bst k_largest_values_in_bst lowest_common_ancestor_in_bst bst_from_preorder bst_from_sorted_array descendant_and_ancestor_in_bst range_lookup_in_bst bst_merge blind75_lowest_common_ancestor_of_a_binary_search_tree blind75_validate_binary_search_tree blind75_kth_smallest_element_in_a_bst interviewcake_second-largest-item-in-bst interviewcake_bst-checker ctci6_4_2 ctci6_4_5 ctci6_10_10''',
'Partitioning': '''even_odd_array dutch_national_flag first_missing_positive_entry kth_largest_in_array''',
'Arithmetic and number theory': '''int_as_array_increment int_as_array_multiply prime_sieve binomial_coefficients gcd max_product_all_but_one int_as_list_add power_x_y reverse_digits is_number_palindromic string_integer_interconversion convert_base spreadsheet_encoding interviewcake_which-appears-twice ctci6_2_5 ctci6_5_2 ctci6_8_5 ctci6_16_5 ctci6_16_8 ctci6_16_9 ctci6_16_11 ctci6_17_6''',
'Greedy': '''advance_by_offsets buy_and_sell_stock alternating_array making_change minimum_waiting_time minimum_points_covering_intervals majority_element refueling_schedule left_right_justify_text bonus smallest_nonconstructible_value is_array_dominated find_salary_threshold blind75_best_time_to_buy_and_sell_stock blind75_non_overlapping_intervals blind75_jump_game interviewcake_stock-price interviewcake_graph-coloring ctci6_10_11 ctci6_17_10''',
'Array transformations': '''apply_permutation next_permutation spiral_ordering matrix_rotation rotate_array rook_attack blind75_rotate_image blind75_spiral_matrix blind75_set_matrix_zeroes ctci6_1_7 ctci6_1_8''',
'Randomized algorithms': '''offline_sampling online_sampling random_permutation random_subset nonuniform_random_number uniform_random_number interviewcake_shuffle interviewcake_simulate-5-sided-die interviewcake_simulate-7-sided-die ctci6_4_11 ctci6_13_8 ctci6_16_23 ctci6_17_2 ctci6_17_3''',
'Dynamic programming': '''ctci6_17_23 pascal_triangle fibonacci max_sum_subarray number_of_score_combinations levenshtein_distance number_of_traversals_matrix is_string_in_matrix knapsack is_string_decomposable_into_words minimum_weight_path_in_a_triangle picking_up_coins number_of_traversals_staircase pretty_printing longest_nondecreasing_subsequence buy_and_sell_stock_twice buy_and_sell_stock_k_times smallest_subarray_covering_all_values regular_expression defective_jugs maximum_subarray_in_circular_array max_safe_height max_square_submatrix blind75_climbing_stairs blind75_house_robber blind75_house_robber_ii blind75_decode_ways blind75_coin_change blind75_maximum_product_subarray blind75_word_break blind75_longest_increasing_subsequence blind75_unique_paths blind75_combination_sum_iv blind75_maximum_subarray blind75_counting_bits interviewcake_nth-fibonacci interviewcake_highest-product-of-3 interviewcake_coin interviewcake_cake-thief ctci6_8_1 ctci6_8_2 ctci6_8_11 ctci6_8_13 ctci6_8_14 ctci6_16_17 ctci6_17_8 ctci6_17_13 ctci6_17_15 ctci6_17_16 ctci6_17_24''',
'Breadth-first search': '''search_maze painting string_transformability tree_level_order blind75_binary_tree_level_order_traversal blind75_number_of_islands interviewcake_mesh-message ctci6_4_1 ctci6_4_3 ctci6_7_10 ctci6_17_7 ctci6_17_22''',
'Flood fill': '''matrix_enclosed_regions blind75_pacific_atlantic_water_flow ctci6_8_10 ctci6_16_19''',
'Topological sorting': '''deadlock_detection max_teams_in_photograph blind75_course_schedule blind75_alien_dictionary ctci6_4_7''',
'Graph algorithms': '''is_circuit_wirable road_network arbitrage ctci6_15_4''',
'Union-find': '''blind75_number_of_connected_components_in_an_undirected_graph blind75_graph_valid_tree''',
'Sliding window': '''smallest_subarray_covering_set longest_subarray_with_distinct_values string_decompositions_into_dictionary_words blind75_longest_substring_without_repeating_characters blind75_longest_repeating_character_replacement blind75_minimum_window_substring ctci6_5_3 ctci6_17_18''',
'Monotonic stack or deque': '''largest_rectangle_under_skyline max_of_sliding_window max_submatrix queue_with_max''',
'Heap': '''minimum_distance_3_sorted_arrays sorted_arrays_merge sort_increasing_decreasing_array sort_almost_sorted_array k_closest_stars online_median k_largest_in_heap kth_largest_element_in_long_array huffman_coding blind75_merge_k_sorted_lists blind75_find_median_from_data_stream ctci6_17_14 ctci6_17_20''',
'Merging sorted sequences': '''a_b_sqrt2 ctci6_17_9 ctci6_10_6''',
'Stack': '''longest_substring_with_matching_parentheses stack_with_max evaluate_rpn is_valid_parenthesization directory_path_normalization queue_from_stacks blind75_valid_parentheses interviewcake_queue-two-stacks interviewcake_largest-stack interviewcake_bracket-validator ctci6_3_1 ctci6_3_2 ctci6_3_3 ctci6_3_4 ctci6_3_5''',
'Data structure design': '''adding_credits lru_cache circular_queue ctci6_3_6 ctci6_7_9 ctci6_16_25 ctci6_12_1''',
'Monotone matrix search': '''search_row_col_sorted_matrix ctci6_10_9''',
'Binary search': '''search_unknown_length_array kth_largest_element_in_two_sorted_arrays longest_subarray_with_sum_constraint search_first_key search_entry_equal_to_index search_shifted_sorted_array int_square_root real_square_root blind75_find_minimum_in_rotated_sorted_array blind75_search_in_rotated_sorted_array interviewcake_find-duplicate-optimize-for-space interviewcake_find-rotation-point ctci6_8_3 ctci6_10_3 ctci6_10_4 ctci6_10_5''',
'Subset enumeration': '''power_set ctci6_8_4''',
'Backtracking': '''insert_operators_in_string phone_number_mnemonic n_queens permutations combinations enumerate_balanced_parentheses enumerate_palindromic_decompositions enumerate_trees sudoku_solve blind75_combination_sum blind75_word_search_ii blind75_word_search interviewcake_recursive-string-permutations ctci6_4_9 ctci6_7_6 ctci6_8_7 ctci6_8_8 ctci6_8_9 ctci6_8_12 ctci6_17_25''',
'Divide and conquer': '''hanoi count_inversions sort_list ctci6_8_6''',
'Sweep line': '''drawing_skyline calendar_rendering blind75_meeting_rooms_ii ctci6_16_10''',
'Intervals': '''interval_add intervals_union blind75_insert_interval blind75_merge_intervals blind75_meeting_rooms interviewcake_merging-ranges''',
'Geometry': '''line_through_most_points ctci6_16_14 rectangle_intersection interviewcake_rectangular-love ctci6_16_3 ctci6_16_13''',
'Prefix and suffix accumulation': '''blind75_product_of_array_except_self interviewcake_product-of-other-numbers ctci6_4_12 ctci6_17_5''',
'Trie': '''blind75_implement_trie_prefix_tree blind75_design_add_and_search_words_data_structure interviewcake_compress-url-list''',
'String processing': '''replace_and_remove look_and_say roman_to_integer valid_ip_addresses snake_string run_length_compression substring_match blind75_valid_anagram blind75_encode_and_decode_strings blind75_valid_palindrome interviewcake_matching-parens ctci6_1_6 ctci6_1_9 ctci6_4_10 ctci6_10_2 ctci6_16_18 ctci6_16_20 ctci6_16_26 ctci6_17_17''',
'Simulation': '''is_valid_sudoku collatz_checker ctci6_7_8 ctci6_16_4 ctci6_16_22''',
'Linear scan': '''ctci6_16_16 sorted_array_remove_dups longest_increasing_subarray search_in_list search_for_min_max_in_array sunset_view ctci6_13_7 ctci6_17_11''',
'Bitset': '''ctci6_10_7 ctci6_10_8''',
'Concurrency': '''ctci6_15_3 ctci6_15_5 ctci6_15_7''',
}
# Observation prompts deliberately precede the concrete strategy and contain no code.
PROMPTS = {
'Bit manipulation': 'Which bit positions matter independently, and what happens to them when equal bits cancel or a mask selects a subset?',
'Two pointers': 'Can two positions delimit the candidates still worth considering? What fact would justify moving one position without losing an answer?',
'Hashing and counting': 'What information about earlier occurrences would let you answer a lookup without scanning those occurrences again?',
'Linked-list rewiring': 'Before changing a link, which references must you save so every required original node remains reachable?',
'Fast and slow pointers': 'If two walkers follow the same links at different speeds, how does their relative position behave after entering a cycle?',
'Pointer alignment': 'Can you align two traversals by the distance each has left to travel, rather than repeatedly searching from the beginning?',
'Identity mapping': 'How will you distinguish the same object reached twice from two different objects with equal values?',
'Tree traversal': 'What information does a node need from its ancestors or children? Use that dependency to choose the order in which you visit nodes.',
'Binary search tree': 'Which candidates can you rule out using the ordering of a node and its subtrees? Check this problem’s exact rule for duplicate keys.',
'Partitioning': 'Can you maintain regions of values that are already classified, leaving only one region still to inspect?',
'Arithmetic and number theory': 'Can you work with digits, place values, or a smaller arithmetic identity instead of constructing every possible candidate?',
'Greedy': 'What can you settle now without making a later choice worse? Try to justify that choice before committing to it.',
'Array transformations': 'Track where an original element must end up. Which boundaries or saved observations prevent a write from destroying information you still need?',
'Randomized algorithms': 'Think about individual occurrences, not just distinct values. What probability must each eligible choice have, and can your random range introduce bias?',
'Dynamic programming': 'What smaller state would summarize all relevant earlier choices? Define that state before deciding how to update it.',
'Breadth-first search': 'What should the initial frontier contain, and when should an item be marked discovered so it cannot be processed repeatedly?',
'Flood fill': 'Which neighboring positions belong to the same reachable region? Decide when to mark them so cycles cannot repeat work.',
'Topological sorting': 'Which items can be processed before any others, and what becomes available after you remove one of them?',
'Graph algorithms': 'What should vertices and edges represent? Identify the graph property that would certify success or failure.',
'Union-find': 'Does an edge connect two previously separate groups, or stay within a group that is already connected?',
'Sliding window': 'What makes a contiguous window valid? Identify the smallest summary you need when one entry enters or leaves it.',
'Monotonic stack or deque': 'When does a new entry make an older candidate permanently unnecessary? Can you discard that candidate instead of reconsidering it later?',
'Heap': 'Do you need every candidate in sorted order, or only repeated access to an extreme among the current candidates?',
'Merging sorted sequences': 'If each source is already ordered, which unconsumed entries can possibly be next in the combined order?',
'Stack': 'Which unfinished operation or earlier state must be resumed first? Consider whether the most recent one is the relevant one.',
'Data structure design': 'List the operations that must be efficient. What extra state would avoid rescanning or moving all stored entries after each operation?',
'Monotone matrix search': 'Which corner has smaller candidates along one direction and larger candidates along the other? Can one comparison rule out a whole row or column?',
'Binary search': 'What ordering lets a comparison eliminate candidates? Be careful: gaps, duplicates, or unknown length may require extra work before that comparison is useful.',
'Subset enumeration': 'For one new member, how do subsets that include it relate to the subsets that do not? Avoid modifying an earlier subset while creating a new one.',
'Backtracking': 'Build a partial candidate. Which choices can extend it, which conditions already make it impossible, and what state must be restored after trying a choice?',
'Divide and conquer': 'Can a smaller version of the same task solve each part? Work out how the partial results combine before choosing a base case.',
'Sweep line': 'At which positions can the answer change? Decide how simultaneous events must be ordered under the stated endpoint rules.',
'Intervals': 'What does touching at an endpoint mean in this contract? Ordering intervals can make the only possible next overlap easier to identify.',
'Geometry': 'Separate coordinate relationships from drawing intuition. Explicitly consider touching boundaries, coincident points, and degenerate shapes allowed by the contract.',
'Prefix and suffix accumulation': 'What can you precompute or carry about prefixes and suffixes so each candidate does not require recomputing its entire range?',
'Trie': 'Which words share the work of matching an initial sequence of characters? How will you distinguish a complete word from a prefix?',
'String processing': 'What makes a segment, token, or match unambiguous in this contract? Try tracking boundaries rather than repeatedly rebuilding the whole string.',
'Simulation': 'Write down the state before and after one legal step. Which observations must be completed before you mutate that state?',
'Linear scan': 'What small summary of the entries already visited is enough to process the next entry?',
'Bitset': 'How many possible values are there? Could one bit per value record the fact you need within the memory budget?',
'Concurrency': 'Which actions must finish before another action starts? Encode those ordering constraints without relying on thread launch order or sleep durations.',
}
def build():
    solutions = {x['problemId']: x for x in json.loads((ROOT/'solutions/catalog.json').read_text()) if x['language']=='csharp'}
    assignments = {}
    for tag, ids in GROUPS.items():
        for pid in ids.split():
            if pid in assignments: raise ValueError(f'duplicate {pid}')
            assignments[pid] = tag
    missing = set(solutions)-set(assignments)
    extra = set(assignments)-set(solutions)
    if missing or extra: raise ValueError(f'Missing: {sorted(missing)}; extra: {sorted(extra)}')
    overrides = json.loads((ROOT/'scripts/guidance/overrides.json').read_text())
    for kind, entries in overrides.items():
        if kind not in ('observations', 'approaches') or set(entries)-set(solutions):
            raise ValueError(f'Unknown guidance override: {kind}')
        if any(not text.strip() for text in entries.values()):
            raise ValueError(f'Empty guidance override: {kind}')
    result = {}
    for pid, solution in solutions.items():
        tag = assignments[pid]
        approach = solution['explanation'].split(' C#')[0].split(' The\n')[0].strip()
        if approach.endswith(' The'): approach = approach[:-4]
        if pid == 'evaluate_rpn': approach = approach.replace('C# integer division supplies', 'Integer division must use')
        result[pid] = {'tags':[tag], 'hints':[
            overrides['observations'].get(pid, PROMPTS[tag]),
            overrides['approaches'].get(pid, approach),
        ]}
    return result
if __name__ == '__main__':
    target = ROOT/'epijudge.client/src/problemGuidance.json'
    document = build()
    if '--check' in sys.argv:
        if json.loads(target.read_text()) != document:
            raise SystemExit('Guidance is stale; run scripts/guidance/build_catalog.py')
        print(f'PASS: {len(document)} reviewed identities, tags and hint pairs match sources')
    else:
        target.write_text(json.dumps(document,ensure_ascii=False,indent=2)+'\n')
        print(f'Wrote {target}')
