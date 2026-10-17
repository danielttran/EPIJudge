"""Generate the web catalog from the repository's canonical TSV catalog.

Run with Python from any directory. No third party modules are required.
Descriptions describe the C# API (some Python wrapper records are C# tuples).
"""
import ast
import importlib.util
import hashlib
import json
import re
from pathlib import Path
from web_problem_examples import custom_example

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stubs', ROOT / 'epi_judge_csharp/generate_problem_stubs.py')
stubs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stubs)

NOTES = """
a_b_sqrt2|Return the first k distinct numbers of the form a + b√2 in increasing order, where a and b are nonnegative integers. Include zero.
absent_value_array|Find a nonnegative integer that does not occur in the input stream. This C# API returns int, so choose a value between 0 and int.MaxValue. Any missing value in that range is accepted.
adding_credits|Implement a client credit database: insert replaces a client's credit, remove reports whether a client existed, lookup returns -1 for a missing client, AddAll adjusts every credit, and Max returns the ID with greatest credit (empty string if empty). Initialize resets the database.
advance_by_offsets|Each entry is the maximum distance you can advance from that position. Determine whether the last position is reachable from the first.
alternating_array|Rearrange the array in place so A[0] ≤ A[1] ≥ A[2] ≤ A[3] and so on. Preserve all elements.
apply_permutation|Apply the permutation to the input values: the element originally at index i moves to index perm[i]. Return the permuted values.
arbitrage|Given a matrix of currency exchange rates, determine whether a cycle of exchanges can produce a profit.
binomial_coefficients|Compute the binomial coefficient n choose k.
bonus|Assign positive integer bonuses to employees in a line. An employee with higher productivity than an adjacent employee must receive a larger bonus. Return the minimum total bonus.
bst_from_preorder|Reconstruct a binary search tree from its preorder traversal.
bst_from_sorted_array|Build a binary search tree of minimum height from the sorted input. Return the root. The judge checks its inorder contents and height (height counts nodes).
bst_merge|Merge the two BSTs' sorted inorder sequences, preserving duplicates, and build a balanced BST from the merged sequence. The corpus compares tree structure: for each half-open range [start, end), choose index start + (end - start) / 2 as its root and recurse on the two remaining ranges. Return the root.
bst_to_sorted_list|Convert the BST into a sorted doubly linked list in place. Use Left as the previous link and Right as the next link. Return the head; its Left must be null.
buy_and_sell_stock|Return the greatest profit from at most one buy followed by one sell. Return zero if no profitable transaction exists.
buy_and_sell_stock_k_times|Return the greatest profit from at most k buy/sell transactions. You may hold at most one share at a time.
buy_and_sell_stock_twice|Return the greatest profit from at most two buy/sell transactions, holding at most one share at a time.
calendar_rendering|Each tuple is an event (start, finish). Return the maximum number of simultaneous events. Events touching at an endpoint overlap.
circular_queue|Implement an integer queue using a resizable circular buffer. Initialize(capacity) resets it, Enqueue appends, Dequeue removes the oldest value, and Size reports its count. Grow the buffer when full.
closest_int_same_weight|Return a different nonnegative integer with the same number of set bits as x, minimizing the absolute difference from x.
collatz_checker|Check the Collatz conjecture for every integer from 1 through n: repeatedly halve even values and replace odd values by 3x+1, eventually reaching 1.
combinations|Return every k-element subset of integers 1 through n. Order of subsets does not matter.
convert_base|Convert the integer string from base b1 to base b2, where both bases are between 2 and 16. Preserve a leading minus sign when the number is negative. Output digits above 9 use uppercase A through F.
copy_posting_list|Deep-copy a posting list with Next and Jump references. Preserve Order and all links, and return the copied head. No node in the copy may reference an original node.
count_inversions|Count pairs of indices i < j for which A[i] > A[j].
deadlock_detection|A directed graph is given by a vertex count and (from, to) edges. Return whether it contains a directed cycle.
defective_jugs|Each jug measures an uncertain volume in [low, high]. Determine whether some sequence of jug uses guarantees a total entirely within the requested [l, h] interval. A jug may be reused.
delete_from_list|Delete the node at zero-based position node_idx from the singly linked list and return its head. This exercise deletes through the preceding node, so the supplied position is at least 1; the head is not selected.
delete_kth_last_from_list|Remove the kth node from the end of a singly linked list (k = 1 removes the last node). Return the head.
delete_node_from_list|Delete the node at zero-based position node_to_delete_idx and return the head. The selected node is not the tail. The C# API supplies head and the position to locate the node; once located, practice deleting it using only that node and its successor, without using its predecessor.
descendant_and_ancestor_in_bst|The three integers identify nodes by Data. Determine whether one candidate is a proper ancestor of the middle node and the other is its proper descendant in the BST.
directory_path_normalization|Normalize a Unix path by resolving '.', '..', and repeated slashes while respecting absolute versus relative paths. Preserve unresolved leading '..' components of a relative path. A relative path that cancels completely becomes the empty string; the absolute root remains '/'.
do_lists_overlap|Find an overlapping node in two lists that may contain cycles. Return an actual shared node, or null if disjoint. The judge constructs shared tails and cycles before calling your method.
do_terminated_lists_overlap|Find the first shared node of two acyclic singly linked lists. Return that node by reference, or null if disjoint. Equal values alone do not imply overlap.
drawing_skyline|Buildings are (left, right, height) rectangles with inclusive integer endpoints. Return the skyline as maximal constant-height (left, right, height) spans, including zero-height gaps.
dutch_national_flag|Partition the array in place into values less than, equal to, and greater than the value originally at pivotIndex. Preserve every element.
element_appearing_once|Every integer appears three times except one that appears once. Return that unique integer.
enumerate_balanced_parentheses|Return all balanced strings containing num_pairs pairs of parentheses. Output order does not matter.
enumerate_palindromic_decompositions|Return every partition of the text into palindromic substrings. Preserve substring order within each partition; partition order does not matter.
enumerate_trees|Return all distinct binary tree shapes with num_nodes nodes. Encode each shape by breadth-first traversal: 1 for a node and 0 for null, including every null child of each real node. The empty tree is [0]. Shape order does not matter.
evaluate_rpn|Evaluate a comma-separated reverse Polish expression using integer arithmetic and +, -, *, /. Division truncates toward zero.
even_odd_array|Reorder the array in place so every even value precedes every odd value. Preserve all elements; internal group order is unrestricted.
even_odd_list_merge|Reorder a singly linked list by putting nodes at even zero-based positions first, followed by nodes at odd positions. Preserve relative order within each group.
fibonacci|Return the nth Fibonacci number, with F(0) = 0 and F(1) = 1.
find_missing_and_duplicate|An array of length n should contain 0 through n-1, but one value is missing and another is duplicated. Return (duplicate, missing).
find_salary_threshold|Cap every salary at one common threshold so the total equals target_payroll. Return the smallest cap achieving that total, or -1 if the target exceeds the existing payroll. When the target equals the current total, the cap is the largest current salary.
first_missing_positive_entry|Return the smallest positive integer absent from the array.
gcd|Compute the greatest common divisor of two nonnegative integers.
graph_clone|Deep-copy the directed graph reachable from the supplied vertex. Preserve labels, duplicate edges, cycles, and sharing. No original vertex may appear in the copy.
gray_code|Return all 2^numBits distinct numBits-bit integers in an order where consecutive values differ in exactly one bit.
group_equal_entries|Rearrange (age, name) people in place so entries of the same age are contiguous. Preserve every person; group order is unrestricted.
h_index|Return the largest h such that at least h papers have at least h citations each.
hanoi|Return a legal sequence of moves transferring all rings from peg 0 to peg 1 or peg 2. A move is [sourcePeg, destinationPeg]. Never place a larger ring on a smaller ring.
huffman_coding|Given (character, frequency) pairs, build an optimal binary Huffman code and return sum(frequency × codewordLength) / 100. This is the corpus's exact weighting convention: divide by 100, not by the sum of the supplied frequencies, even when that sum is near 1. A single symbol may have an empty codeword of length 0.
insert_in_list|Insert a node containing the new value after the node selected by the repository's 1-based node position (position 1 is the head). Return the resulting head.
insert_operators_in_string|Determine whether inserting multiplication and addition operators between digits, with optional digit concatenation, can produce the target. Multiplication has its usual precedence.
int_as_array_increment|Increment a nonnegative integer represented by a most-significant-digit-first array of decimal digits.
int_as_array_multiply|Multiply two integers represented by most-significant-digit-first decimal arrays. A negative first digit encodes the sign. Return the product in the same format.
int_as_list_add|Add two nonnegative integers represented by singly linked lists of decimal digits, least significant digit first. Return the sum in that format.
int_square_root|Return the floor of the square root of a nonnegative integer.
intersect_sorted_arrays|Return the distinct values present in both sorted arrays, in increasing order.
interval_add|Insert a closed interval into sorted disjoint closed intervals, merging overlaps. Tuples are (start, end).
intervals_union|Return the union of intervals as sorted disjoint intervals. Each tuple is (leftValue, leftClosed, rightValue, rightClosed), so open and closed endpoints matter.
is_anonymous_letter_constructible|Determine whether the letter can be constructed from the magazine's characters, using each character at most as often as it appears. Case and whitespace are significant.
is_array_dominated|Two equally sized teams are given as player heights. Determine whether their players can be reordered so every member of team0 stands in front of a strictly taller member of team1. The judge checks both directions.
is_circuit_wirable|Given vertices and graph edges, determine whether the circuit is bipartite: every edge must connect opposite groups.
is_list_cyclic|Return the first node in a list's cycle, or null if acyclic. The judge adds the cycle before the call. Node identity is checked.
is_list_palindromic|Return whether a singly linked list reads the same forward and backward.
is_number_palindromic|Return whether the decimal representation is palindromic. Negative numbers are not palindromes.
is_string_decomposable_into_words|Split the domain into dictionary words whose concatenation exactly equals the input. Return an empty list if impossible. Any valid decomposition is accepted.
is_string_in_matrix|Determine whether the sequence can be traced through horizontally or vertically adjacent matrix cells. Cells may be reused.
is_string_palindromic|Return whether the string equals its reversal, comparing every character exactly.
is_string_palindromic_punctuation|Return whether the string is palindromic after ignoring non-alphanumeric characters and letter case.
is_string_permutable_to_palindrome|Return whether some permutation of the string is a palindrome.
is_tree_a_bst|Determine whether the binary tree satisfies the binary search tree property. Equal keys are permitted at either side according to this corpus.
is_tree_balanced|Return whether every node's left and right subtree heights differ by at most one.
is_tree_symmetric|Return whether the binary tree is a mirror image of itself around its root.
is_valid_parenthesization|Validate properly nested (), [], and {} brackets.
is_valid_sudoku|Determine whether a partially filled Sudoku grid has any conflicting rows, columns, or subgrids. Zero denotes an empty cell.
k_closest_stars|Stars are (x, y, z) coordinates. Return the Euclidean distances of the k stars nearest the origin. Output order does not matter.
k_largest_in_heap|The array represents a max heap. Return its k largest values in any order, preserving multiplicities. As an efficiency goal, avoid sorting the entire heap.
k_largest_values_in_bst|Return the k largest keys in the BST. Output order does not matter.
knapsack|Items are (weight, value) pairs. Choose each item at most once and maximize total value without exceeding capacity. Return the maximum value.
kth_largest_element_in_long_array|Return the kth largest value in the stream, counting duplicates. k is 1-based.
kth_largest_element_in_two_sorted_arrays|Return the kth smallest value in the combined sorted arrays, counting duplicates. k is 1-based despite the repository filename.
kth_largest_in_array|Return the kth largest element, counting duplicates. k is 1-based.
kth_node_in_tree|Return the Data of the kth node in inorder traversal, with k starting at 1.
largest_rectangle_under_skyline|Given unit-width histogram heights, return the area of its largest axis-aligned rectangle.
left_right_justify_text|Pack each line greedily with as many consecutive words as fit within width L, allowing at least one space between words. Fully justify every nonfinal line: distribute spaces evenly between words, with extra spaces in the leftmost gaps. Pad single-word lines on the right. Left-justify the last line with single inter-word spaces and pad its right side to width L.
levenshtein_distance|Return the minimum number of single-character insertions, deletions, and substitutions needed to transform one string into the other.
line_through_most_points|Return the largest number of supplied (x, y) point entries that lie on one straight line. Count duplicate coordinate entries separately.
list_cyclic_right_shift|Cyclically shift the list right by k positions and return its head.
longest_contained_interval|Return the size of the longest interval of consecutive integer values contained in the input array, regardless of their positions.
longest_increasing_subarray|Return the length of the longest contiguous strictly increasing subarray.
longest_nondecreasing_subsequence|Return the length of the longest subsequence whose values never decrease. Elements need not be contiguous.
longest_subarray_with_distinct_values|Return the length of the longest contiguous subarray containing no duplicate values.
longest_subarray_with_sum_constraint|Return the maximum length of a contiguous subarray whose sum is at most k. Negative values are allowed.
longest_substring_with_matching_parentheses|Return the length of the longest contiguous substring of balanced parentheses.
look_and_say|Return the nth term of the look-and-say sequence, starting with '1'. Describe each run of identical digits by its count and digit.
lowest_common_ancestor|The integer arguments identify two nodes by Data. Return the Data of their lowest common ancestor. Parent pointers are available.
lowest_common_ancestor_in_bst|The integers s and b identify existing nodes by Data, with s ≤ b. Return the Data of their lowest common ancestor in the BST.
lru_cache|Implement a least-recently-used cache. Initialize(capacity) resets it. Lookup returns -1 if missing and refreshes recency. Insert refreshes existing keys while preserving their old price; new insertions evict the least recent entry when full. Erase reports whether a key existed.
majority_element|Return the string appearing in more than half of the stream's entries. Such an entry is guaranteed to exist.
making_change|Return the minimum number of coins needed for the amount, using US denominations 100, 50, 25, 10, 5, and 1.
matrix_enclosed_regions|Change every enclosed white region ('W') into black ('B'). A white cell connected to a boundary by horizontal or vertical steps remains white. Return the updated board.
matrix_rotation|Rotate a square matrix 90 degrees clockwise and return it.
max_of_sliding_window|Process chronological (time, volume) readings in input order. For each current reading at time t, return (t, maximumVolume) among the current and previously processed readings whose times lie in the inclusive interval [t-w, t].
max_product_all_but_one|Return the greatest product obtainable by multiplying all array entries except one.
max_safe_height|Given cases identical breakable objects and at most drops tests, return the greatest number of floors for which a critical height can always be determined. Dropping an object above the critical height breaks it; otherwise it survives and can be reused. A broken object cannot be reused.
max_square_submatrix|Return the area of the largest square submatrix consisting entirely of true cells.
max_submatrix|Return the area of the largest rectangular submatrix consisting entirely of true cells.
max_sum_subarray|Return the maximum sum of a contiguous subarray. The empty subarray is permitted, giving zero when all values are negative.
max_teams_in_photograph|Given a directed acyclic graph of compatible team orderings, return the greatest number of teams on a path (count vertices).
max_trapped_water|Choose two vertical lines at array positions to hold the greatest amount of water. Return (index distance) × (smaller height) for the best pair.
max_water_trappable|Return the total water trapped between unit-width histogram bars after rain.
maximum_subarray_in_circular_array|Return the maximum contiguous subarray sum when the array is circular. The empty subarray is allowed.
minimum_distance_3_sorted_arrays|Given nonempty sorted arrays, choose one entry from each and minimize the difference between the largest and smallest chosen values. Return that difference. The C# input can contain more than three arrays despite the repository filename.
minimum_points_covering_intervals|Return the minimum number of points needed to intersect every closed interval (start, end).
minimum_waiting_time|Order the queries to minimize their total waiting time before execution. Return that total, excluding each query's own processing time.
minimum_weight_path_in_a_triangle|Return the minimum sum along a path from the top to the bottom of the triangle. From column i, move to column i or i+1 in the next row.
n_queens|Return all placements of n nonattacking queens on an n×n board. Each placement lists the zero-based column of the queen in each row, from row 0 through n-1. Placement order does not matter.
nearest_repeated_entries|Return the minimum index distance between equal words, or -1 if no word repeats.
next_permutation|Return the next lexicographic permutation. Return an empty list if the input is already the last permutation.
nonuniform_random_number|Return one entry from values, choosing values[i] with probabilities[i]. Repeated calls must follow that distribution. Random.Shared is available as a randomness source.
number_of_score_combinations|Count unordered combinations of allowed play scores that sum to the final score. Each play may be repeated.
number_of_traversals_matrix|Count paths from the upper-left corner to the lower-right corner of an n×m grid, moving only right or down.
number_of_traversals_staircase|Count ways to climb from stair 0 to stair top when each step advances between 1 and maximum_step stairs. The order of step sizes matters; there is one way to stay at stair 0 without taking a step.
offline_sampling|Rearrange A in place so its first k entries form a uniformly random k-element subset. Preserve the entire array's multiset.
online_median|Return the median after each successive stream entry. For an even prefix length, average its two central entries.
online_sampling|Return a uniformly random k-element sample of the stream without replacement. Every k-element subset must be equally likely.
painting|The image contains 0 and 1 cells. Starting at row x, column y, find the component of cells with the same original value connected by horizontal or vertical steps. Flip those cells (0 to 1 and 1 to 0) and return the updated image.
parity|Return 1 if the 64-bit integer has an odd number of set bits, otherwise 0.
pascal_triangle|Return the first n rows of Pascal's triangle, starting with [1]. Return an empty list when n is 0.
path_sum|Determine whether a root-to-leaf path has the requested sum of node values.
permutations|Return every permutation of the input values. Preserve each permutation's order; the order of permutations does not matter.
phone_number_mnemonic|Return all mnemonics using uppercase telephone letters: 2→ABC, 3→DEF, 4→GHI, 5→JKL, 6→MNO, 7→PQRS, 8→TUV, 9→WXYZ. Digits 0 and 1 map to themselves. Choose one mapped character for every input digit. Output order does not matter.
picking_up_coins|Two players alternately take a coin from either end of the row, both playing optimally. Return the maximum total the first player can guarantee.
pivot_list|Partition the list into nodes less than, equal to, and greater than x. Preserve all values and return the head of an acyclic result.
power_set|Return every subset of the input set, including the empty subset. Subset order and element order within a subset do not matter.
power_x_y|Compute x raised to integer power y, including negative powers.
pretty_printing|Wrap words without exceeding the line width. Minimize the sum, over all lines including the last, of squared unused spaces. Return that minimum messiness.
prime_sieve|Return every prime integer from 2 through n, in increasing order.
primitive_divide|Compute the integer quotient of two nonnegative integers without using division, multiplication, or remainder.
primitive_multiply|Multiply two nonnegative integers using bitwise operations, without using arithmetic multiplication or addition.
queue_from_stacks|Implement an integer FIFO queue using stacks. Initialize resets it. Enqueue appends and Dequeue removes the oldest value.
queue_with_max|Implement a FIFO queue supporting Enqueue, Dequeue, and Max. Initialize resets it; Max returns its greatest entry.
random_permutation|Return a uniformly random permutation of 0 through n-1. Successive calls must be independent.
random_subset|Return a uniformly random k-element subset of integers 0 through n-1, without duplicates. Output order is unrestricted.
range_lookup_in_bst|Return all keys in the BST within the inclusive interval (left, right), in sorted order.
real_square_root|Compute the square root of a nonnegative real number. Floating-point results are compared with a relative tolerance.
rectangle_intersection|Rectangles are (x, y, width, height). Return their intersection in the same format, or (0, 0, -1, -1) when disjoint. Touching edges can have zero width or height.
refueling_schedule|Return the zero-based index of any city from which the circular trip can finish without running out of fuel. Start with an empty tank, collect gallons[i] at each city, and then travel distances[i] miles to the next city. Each gallon permits 20 miles; tank capacity is unlimited.
regular_expression|Return whether regex matches s under these rules: '.' matches any single character; '*' repeats the preceding character or '.' zero or more times; a leading '^' anchors the start; and a trailing '$' anchors the end. Other ordinary characters match themselves. Without anchors, the pattern may match a substring.
remove_duplicates|Names are (firstName, lastName) pairs. Eliminate duplicates by first name and return the distinct first names. Output order does not matter.
remove_duplicates_from_sorted_list|Remove repeated values from a sorted singly linked list, keeping one node per distinct value.
replace_and_remove|Process only the first size characters: delete each 'b' and replace each 'a' with two 'd' characters. Return the transformed characters, excluding unused buffer capacity.
reverse_bits|Reverse all 64 bits of the integer and return the resulting bit pattern.
reverse_digits|Reverse the decimal digits of the integer, preserving its sign.
reverse_list|Reverse a singly linked list and return its new head.
reverse_sublist|Reverse the list segment from start through finish, using inclusive 1-based positions. Return the head.
reverse_words|Reverse the order of words separated by literal spaces, preserving each word's characters. Do not collapse repeated spaces or trim the string: reverse the order of the intervening space runs as well, exchanging leading and trailing spaces.
road_network|Existing undirected highways H and candidate proposals P are (city0, city1, distance). Choose one proposal whose addition most reduces the sum of all-pairs shortest path distances among n cities. Return that proposal tuple; when savings tie, choose the first proposal in P. If P is empty, return (-1, -1, 0).
roman_to_integer|Convert a string of Roman symbols I, V, X, L, C, D, and M to an integer. Subtract a symbol's value when it is smaller than the immediately following symbol; otherwise add it. Apply this arithmetic rule without validating canonical Roman-numeral spelling.
rook_attack|If a matrix cell is zero, clear its entire row and column. Base the decision on the original matrix and return the updated matrix.
rotate_array|Cyclically rotate the array right by rotate_amount positions and return it.
run_length_compression|Implement both run-length Encoding and Decoding for strings of nondigit characters. Each encoded run is a positive decimal count followed by its character; counts may contain several digits. For example, '3a2b' represents 'aaabb'.
search_entry_equal_to_index|Given a strictly increasing array of distinct integers, find any zero-based index i for which A[i] equals i. Return -1 only when no such index exists.
search_first_greater_value_in_bst|Return the smallest BST key strictly greater than k, or -1 if none exists.
search_first_key|Return the first index of k in the sorted array, or -1 if absent.
search_for_min_max_in_array|Return (minimum, maximum) for the array using as few comparisons as possible.
search_frequent_items|Return each string occurring more than streamLength/k times. Output order does not matter.
search_in_bst|Search the BST for key and return its value, or -1 when absent.
search_in_list|Search the linked list for key and return its value, or -1 when absent.
search_maze|Return a path of (row, column) coordinates from start to end, moving horizontally or vertically through white cells (0). Black cells (1) are blocked. Include both endpoints; return an empty list when unreachable.
search_row_col_sorted_matrix|Determine whether the target occurs in a matrix whose rows and columns are each sorted in nondecreasing order.
search_shifted_sorted_array|Return the index of the smallest value in a cyclically shifted sorted array of distinct values.
search_unknown_length_array|Return the zero-based index of k in a strictly increasing array, or -1 if absent. As the exercise's practice goal, search using indexed access and out-of-range detection rather than relying on the array length.
smallest_nonconstructible_value|Return the smallest positive sum that cannot be formed from a subset of the nonnegative input values, each used at most once.
smallest_subarray_covering_all_values|Return inclusive zero-based (start, end) indices of a shortest paragraph slice containing the distinct keywords in the given order. Other paragraph entries may occur between keywords. The corpus supplies a covering slice; the judge validates coverage and minimum length.
smallest_subarray_covering_set|Return inclusive zero-based (start, end) indices of a shortest paragraph slice containing every keyword. Keyword order does not matter. The corpus supplies a covering slice; the judge validates coverage and minimum length.
snake_string|Arrange the characters on three alternating rows in a sinusoidal pattern, then read the rows from top to bottom. The top row starts at input index 1, middle at 0, bottom at 3.
sort_almost_sorted_array|Sort an array in which every entry is at most k positions from its final sorted location.
sort_increasing_decreasing_array|Sort an array composed of alternating increasing and decreasing runs.
sort_list|Stably sort a singly linked list in nondecreasing order and return its head. Equal-valued nodes should keep their original relative order.
sorted_array_remove_dups|Return the distinct entries of the sorted array in increasing order.
sorted_arrays_merge|Merge all sorted arrays into one sorted array, preserving duplicates.
sorted_list_to_bst|Convert a sorted doubly linked list into a BST. BinaryTreeNode.Left is the previous link and Right is the next link on input; those fields become tree children on output. Return a tree with the original inorder contents.
sorted_lists_merge|Merge two sorted singly linked lists into one sorted list, preserving duplicates.
spiral_ordering|Return the square matrix's entries in clockwise spiral order, starting at its top-left corner.
spreadsheet_encoding|Convert a spreadsheet column label to its 1-based number: A = 1, Z = 26, AA = 27.
stack_with_max|Implement an integer stack supporting Push, Pop, Empty, and Max. Initialize resets it. Max returns its greatest entry.
string_decompositions_into_dictionary_words|Return all starting indices where concatenating every supplied word exactly once produces a substring. All words have equal length and may repeat.
string_integer_interconversion|Implement decimal IntToString and StringToInt. Parsing accepts a leading '+' or '-' sign; formatting uses '-' only for negative values and represents zero as '0'. As a practice goal, implement the conversions without built-in parsing or formatting routines.
string_transformability|Return the minimum number of single-character substitutions needed to transform source s into target t through words in dictionary D, or -1 if impossible. Substitutions use lowercase letters a through z and do not change word length. Return 0 when s equals t.
substring_match|In RabinKarp(t, s), t is the text and s is the pattern. Return the zero-based index of the first occurrence of s in t, or -1 if absent. Character comparisons are case-sensitive.
successor_in_tree|The argument node_idx identifies an existing node by its Data value, not its traversal position. Return the Data of its inorder successor, or -1 when it has no successor. Parent pointers are available.
sudoku_solve|Fill the Sudoku board in place. Preserve every original clue; every row, column, and subgrid must contain each digit exactly once. Zero denotes an empty cell.
sum_root_to_leaf|Node values are binary digits. Interpret each root-to-leaf path as a binary integer and return the sum of those integers.
sunset_view|Buildings arrive east to west. Return indices of buildings that can see the sunset to the west, from west to east. A building is blocked by an equal or taller building to its west.
swap_bits|Swap bits at zero-based positions i and j in a 64-bit integer, leaving every other bit unchanged.
task_pairing|Given an even number of task durations, pair them to minimize the maximum pair sum. The corpus expects the following canonical result: sort durations and pair smallest with largest, then second-smallest with second-largest, and so on. Return each pair with the smaller duration first, in ascending order of that duration.
three_sum|Determine whether three values sum to the target. This EPI variant permits reusing the same element more than once.
tree_connect_leaves|Return leaf Data values from left to right.
tree_exterior|Return the tree's boundary Data values counterclockwise: root, left boundary, leaves from left to right, then right boundary from bottom to top. Do not repeat nodes.
tree_from_preorder_inorder|Reconstruct the binary tree from its preorder and inorder traversals. Node values are distinct.
tree_from_preorder_with_null|Reconstruct a binary tree from preorder tokens. The string 'null' marks an absent child; other tokens are integer values.
tree_inorder|Return the binary tree's inorder traversal (left, root, right).
tree_level_order|Return the binary tree's values grouped by level, from top to bottom and left to right.
tree_postorder|Return the binary tree's postorder traversal (left, right, root).
tree_preorder|Return the binary tree's preorder traversal (root, left, right).
tree_right_sibling|Populate each node's Next pointer with the immediate node to its right on the same level, even when they have different parents. Use null at the end of each level. The input is a perfect binary tree. The judge verifies the Next chains.
tree_with_parent_inorder|Return the inorder traversal of a tree with Parent pointers. The practice goal is constant auxiliary space, excluding the returned traversal list.
two_sorted_arrays_merge|Merge the first m sorted entries of A and the first n sorted entries of B. A has m+n slots; its entries after the first m are unused buffer space. Return the m+n merged values in nondecreasing order.
uniform_random_number|Return a uniformly distributed random integer in the inclusive range [lower, upper]. Successive calls must be independent. You may use Random.Shared.Next(2) as a fair random bit source.
valid_ip_addresses|Insert three dots into the digit string to produce all valid IPv4 addresses. Parts must be 0 through 255 and must not have leading zeros unless exactly '0'.
zip_list|Reorder a list L0,L1,…,Ln into L0,Ln,L1,Ln-1,… and return its head.
"""
notes = dict(line.split('|', 1) for line in NOTES.strip().splitlines())
COMPACT_EXAMPLES = {
 'absent_value_array': ('stream = [0, 1, 3]', '2', 'Verified illustrative example: 2 is absent. Any missing nonnegative int is accepted.'),
 'minimum_distance_3_sorted_arrays': ('sorted_arrays = [[1, 4], [2, 5], [3, 6]]', '2', 'Verified illustrative example: choosing 1, 2, and 3 gives the minimum range of 2.'),
 'string_transformability': ('D = ["cat", "cot", "cog", "dog"], s = "cat", t = "dog"', '3', 'Verified illustrative example: cat → cot → cog → dog requires three single-character changes.'),
 'drawing_skyline': ('buildings = [[1, 3, 2], [2, 4, 3]]', '[[1, 1, 2], [2, 4, 3]]', 'Verified illustrative example: the taller building controls the height from coordinate 2 through 4.'),
}

# Algorithms with non-value protocols expose real operations, never a bool that
# lets a submission certify its own correctness.
CUSTOM = {
 'absent_value_array': [('int','FindMissingElement','List<int> stream')],
 'alternating_array': [('void','Rearrange','List<int> values')],
 'even_odd_array': [('void','EvenOdd','List<int> values')],
 'dutch_national_flag': [('void','DutchFlagPartition','int pivotIndex, List<int> values')],
 'group_equal_entries': [('void','GroupByAge','List<(int Age, string Name)> people')],
 'gray_code': [('List<int>','GrayCode','int numBits')],
 'hanoi': [('List<List<int>>','ComputeTowerHanoi','int numRings')],
 'is_array_dominated': [('bool','ValidPlacementExists','List<int> team0, List<int> team1')],
 'is_string_decomposable_into_words': [('List<string>','DecomposeIntoDictionaryWords','string domain, HashSet<string> dictionary')],
 'search_entry_equal_to_index': [('int','SearchEntryEqualToItsIndex','List<int> values')],
 'refueling_schedule': [('int','FindAmpleCity','List<int> gallons, List<int> distances')],
 'run_length_compression': [('string','Encoding','string text'),('string','Decoding','string encoded')],
 'string_integer_interconversion': [('string','IntToString','int value'),('int','StringToInt','string text')],
 'pivot_list': [('ListNode<int>?','ListPivoting','ListNode<int>? head, int x')],
 'is_list_cyclic': [('ListNode<int>?','HasCycle','ListNode<int>? head')],
 'do_lists_overlap': [('ListNode<int>?','OverlappingLists','ListNode<int>? first, ListNode<int>? second')],
 'do_terminated_lists_overlap': [('ListNode<int>?','OverlappingLists','ListNode<int>? first, ListNode<int>? second')],
 'copy_posting_list': [('PostingListNode?','CopyPostingsList','PostingListNode? head')],
 'graph_clone': [('GraphVertex','CloneGraph','GraphVertex graph')],
 'sorted_list_to_bst': [('BinaryTreeNode<int>?','BuildBstFromSortedDoublyList','BinaryTreeNode<int>? head, int count')],
 'sudoku_solve': [('void','SolveSudoku','List<List<int>> board')],
 'nonuniform_random_number': [('int','NonuniformRandomNumberGeneration','List<int> values, List<double> probabilities')],
 'uniform_random_number': [('int','UniformRandom','int lower, int upper')],
 'random_permutation': [('List<int>','ComputeRandomPermutation','int n')],
 'random_subset': [('List<int>','RandomSubset','int n, int k')],
 'offline_sampling': [('void','RandomSampling','int k, List<int> values')],
 'online_sampling': [('List<int>','OnlineRandomSample','List<int> stream, int k')],
 'bst_from_sorted_array': [('BinaryTreeNode<int>?','BuildMinHeightBstFromSortedArray','List<int> values')],
 'bst_to_sorted_list': [('BinaryTreeNode<int>?','BstToDoublyLinkedList','BinaryTreeNode<int>? tree')],
 'tree_right_sibling': [('void','ConstructRightSibling','BinaryTreeNode<int>? tree')],
 'search_maze': [('List<(int Row, int Column)>','SearchMaze','List<List<int>> maze, (int Row, int Column) start, (int Row, int Column) end')],
 'smallest_subarray_covering_set': [('(int Start, int End)','FindSmallestSubarrayCoveringSet','List<string> paragraph, HashSet<string> keywords')],
 'smallest_subarray_covering_all_values': [('(int Start, int End)','FindSmallestSequentiallyCoveringSubset','List<string> paragraph, List<string> keywords')],
}
CUSTOM['adding_credits'] = [('void','Initialize',''),('void','Insert','string clientId, int credit'),('bool','Remove','string clientId'),('int','Lookup','string clientId'),('void','AddAll','int amount'),('string','Max','')]
CUSTOM['lru_cache'] = [('void','Initialize','int capacity'),('int','Lookup','int isbn'),('void','Insert','int isbn, int price'),('bool','Erase','int isbn')]
CUSTOM['circular_queue'] = [('void','Initialize','int capacity'),('void','Enqueue','int value'),('int','Dequeue',''),('int','Size','')]
CUSTOM['queue_from_stacks'] = [('void','Initialize',''),('void','Enqueue','int value'),('int','Dequeue','')]
CUSTOM['queue_with_max'] = CUSTOM['queue_from_stacks'] + [('int','Max','')]
CUSTOM['stack_with_max'] = [('void','Initialize',''),('void','Push','int value'),('int','Pop',''),('bool','Empty',''),('int','Max','')]

def pascal(s):
    return ''.join(w[:1].upper()+w[1:] for w in s.split('_'))

def source_hash(path):
    # Stable across Git checkouts that use LF or CRLF.
    return hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()

def main():
    mapping = json.loads((ROOT/'problem_mapping.js').read_text().split('=',1)[1].strip().rstrip(';'))
    locations = {}
    for chapter, rows in mapping.items():
        for title, langs in rows.items():
            for entry in langs:
                if entry.startswith(('Python: ', 'C++: ')):
                    locations.setdefault(Path(entry.split(': ',1)[1]).stem, (chapter, title))
    problems = json.loads((ROOT/'epi_judge_csharp/problem_catalog.json').read_text())['problems']
    sources = {}
    for file in sorted((ROOT/'epi_judge_python').glob('*.py')):
        text = file.read_text()
        for testfile in re.findall(r"['\"]([a-z0-9_]+)\.tsv['\"]", text):
            sources[testfile] = file
    # These two LCA variants share one TSV. Keep the existing with-parent C#
    # exercise deliberate and stable rather than relying on directory order.
    sources['lowest_common_ancestor'] = ROOT/'epi_judge_python/lowest_common_ancestor_with_parent.py'
    reference_sources = {}
    for file in sorted((ROOT/'epi_judge_python_solutions').glob('*.py')):
        for testfile in re.findall(r"['\"]([a-z0-9_]+)\.tsv['\"]", file.read_text()):
            reference_sources.setdefault(testfile, []).append(file)
    result = []
    provenance = []
    for p in problems:
        id = p['id']
        references = reference_sources.get(id, [])
        if not references:
            raise ValueError('No reference implementation for ' + id)
        provenance.append(dict(id=id, statementFile='EpiJudge.Runner/ProblemCatalog.cs' if id in {'count_bits','two_sum','anagrams'} else 'EpiJudge.Runner/catalog.json',
            referenceFiles=[dict(path=str(f.relative_to(ROOT)).replace('\\','/'),sha256=source_hash(f)) for f in references],
            testDataFile='test_data/'+p['testDataFile'],testDataSha256=source_hash(ROOT/'test_data'/p['testDataFile'])))
        if id in {'count_bits','two_sum','anagrams'}: continue
        if id not in notes: raise ValueError('Missing description: '+id)
        source = sources.get(id, ROOT/'epi_judge_python'/f'{id}.py')
        functions = []
        target = None
        if source.exists():
            tree = ast.parse(source.read_text())
            functions = [n for n in tree.body if isinstance(n,ast.FunctionDef)]
            for n in ast.walk(tree):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr == 'generic_test_main':
                    target = n.args[2].id if len(n.args)>2 and isinstance(n.args[2],ast.Name) else None
        function = next((n for n in functions if n.name==target), functions[0] if functions else None)
        argnames = [x.arg for x in function.args.args if x.arg!='executor'] if function else ['head']
        if len(argnames) != len(p['argumentTypes']): argnames = ['arg'+str(i) for i in range(len(p['argumentTypes']))]
        argnames = ['@'+x if x in {'string','params','base','event','new','ref','out','in','is','object'} else x for x in argnames]
        method = pascal(re.sub(r'_(wrapper|test)$','',target or id))
        methods = CUSTOM.get(id, [(stubs.csharp_type(p['resultType']), method, ', '.join(stubs.csharp_type(t)+' '+name for t,name in zip(p['argumentTypes'], argnames)))])
        invocation = f'JudgeAdapters.Invoke("{id}", arguments, new Solution())' if id in CUSTOM else 'new Solution().'+method+'('+', '.join(f'JudgeAdapters.Arg<{stubs.csharp_type(t)}>(arguments, {i})' for i,t in enumerate(p['argumentTypes']))+')'
        code = 'using EpiJudge.TestFramework;\n\npublic class Solution\n{\n'
        for typ,name,args in methods:
            code += f'    public {typ} {name}({args})\n    {{\n        // Write your solution here.\n        throw new NotImplementedException();\n    }}\n\n'
        code = code.rstrip()+'\n}\n'
        topic,title = locations.get(source.stem, locations.get(id, ('Additional problems', id.replace('_',' ').title())))
        disambiguate = {
            'even_odd_array': 'Even/Odd Partition', 'fibonacci': 'Fibonacci', 'max_sum_subarray': 'Maximum Subarray Sum',
            'delete_from_list': 'Delete After a Node', 'insert_in_list': 'Insert After a Node', 'search_in_list': 'Search a List',
            'is_string_palindromic': 'Exact Palindrome Check', 'search_in_bst': 'Search a BST',
            'max_square_submatrix': 'Largest True Square', 'max_submatrix': 'Largest True Rectangle',
        }
        if id in disambiguate:
            title += ' — ' + disambiguate[id]
        topic = re.sub(r'^(?:Chapter\s+)?\d+[.:]?\s*','',topic).capitalize()
        if topic == 'C# Additional Problems': topic = 'Additional problems'
        constraints = ['Use the public C# signatures shown below. Run checks three visible corpus cases; Submit checks the complete corpus.']
        if any('binary_tree' in t or 'linked_list' in t for t in p['argumentTypes']) or any('Node' in m[0]+m[2] for m in methods):
            constraints += ['Shared types: ListNode<T> has Data and Next. BinaryTreeNode<T> has Data, Left, Right, Parent, Next, and Size. Constructors take the data value. Tree inputs use compact level-order JSON with null children; linked lists use JSON arrays.']
        if id == 'copy_posting_list': constraints += ['PostingListNode has Order, Next, and Jump; its constructor takes Order.']
        if id == 'graph_clone': constraints += ['GraphVertex has Label and List<GraphVertex> Edges; its constructor takes Label.']
        if p['resultType']=='void': constraints += ['The judge validates the displayed API result or mutation, including node links or repeated random samples when applicable. Do not implement a separate function that simply reports whether the test passed.']
        if any('tuple' in t for t in p['argumentTypes']+[p['resultType']]): constraints += ['Record values use C# value tuples. Tuple elements are available as Item1, Item2, and so on in the order described.']
        lines=(ROOT/'test_data'/p['testDataFile']).read_text().splitlines()[1:]
        examples=[]
        for line in lines[:2]:
            fields=line.split('\t'); count=len(p['argumentTypes'])
            if sum(map(len, fields[:count+1]))>2500: continue
            if id in CUSTOM:
                examples.append(custom_example(id, fields[:count] if p['resultType']=='void' else fields[:count+1]))
            else:
                examples.append(dict(Input=', '.join(f'{name} = {value}' for name,value in zip(argnames,fields)),Output=fields[count],Explanation='One case from the shared EPI test corpus, expressed using the displayed C# signature.'))
        if not examples and id in COMPACT_EXAMPLES:
            value, output, explanation = COMPACT_EXAMPLES[id]
            examples.append(dict(Input=value, Output=output, Explanation=explanation))
        comparison = 'ordered'
        if id in {'combinations','power_set'}: comparison='nested'
        elif id in {'enumerate_balanced_parentheses','enumerate_palindromic_decompositions','enumerate_trees','k_closest_stars','k_largest_in_heap','k_largest_values_in_bst','n_queens','permutations','phone_number_mnemonic','remove_duplicates','search_frequent_items','valid_ip_addresses'}: comparison='unordered'
        result.append(dict(Id=id,Title=title,Topic=topic,Difficulty='Unrated',Description=notes[id],Constraints=constraints,Signature='\n'.join(f'{t} {n}({a})' for t,n,a in methods),StarterCode=code,Examples=examples,Invocation=invocation,ArgumentCount=len(p['argumentTypes']),TestCount=len(lines),Comparison=comparison,ResultType=p['resultType']))
    result.sort(key=lambda p: (p['Topic'],p['Title'],p['Id']))
    (ROOT/'EpiJudge.Runner/catalog.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (ROOT/'docs/problem-wording-sources.json').write_text(json.dumps(dict(basis='Repository reference implementations and TSV corpus; statements are C# paraphrases, not book quotations.',hashConvention='SHA-256 of UTF-8 text with LF line endings.',
        statementFiles={p:source_hash(ROOT/p) for p in ['EpiJudge.Runner/ProblemCatalog.cs','EpiJudge.Runner/catalog.json']}, problems=provenance),indent=2)+'\n',encoding='utf-8')
    print(f'Generated {len(result)} entries; 3 existing curated entries are retained ({len(result)+3} total).')

if __name__=='__main__': main()
