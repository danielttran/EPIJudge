"""Generate the web catalog from the repository's canonical TSV catalog.

Run with Python from any directory. No third party modules are required.
Descriptions describe the C# API (some Python wrapper records are C# tuples).
"""
import ast
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stubs', ROOT / 'epi_judge_csharp/generate_problem_stubs.py')
stubs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stubs)

NOTES = """
a_b_sqrt2|Return the first k distinct numbers of the form a + b√2 in increasing order, where a and b are nonnegative integers. Include zero.
absent_value_array|Find a nonnegative 32-bit integer that does not occur in the input stream. Any missing value is accepted.
adding_credits|Implement a client credit database: insert replaces a client's credit, remove reports whether a client existed, lookup returns -1 for a missing client, AddAll adjusts every credit, and Max returns the ID with greatest credit (empty string if empty). Initialize resets the database.
advance_by_offsets|Each entry is the maximum distance you can advance from that position. Determine whether the last position is reachable from the first.
alternating_array|Rearrange the array in place so A[0] ≤ A[1] ≥ A[2] ≤ A[3] and so on. Preserve all elements.
apply_permutation|Apply the permutation to the input values: the element originally at index i moves to index perm[i]. Return the permuted values.
arbitrage|Given a matrix of currency exchange rates, determine whether a cycle of exchanges can produce a profit.
binomial_coefficients|Compute the binomial coefficient n choose k.
bonus|Assign positive integer bonuses to employees in a line. An employee with higher productivity than an adjacent employee must receive a larger bonus. Return the minimum total bonus.
bst_from_preorder|Reconstruct a binary search tree from its preorder traversal.
bst_from_sorted_array|Build a binary search tree of minimum height from the sorted input. Return the root. The judge checks its inorder contents and height (height counts nodes).
bst_merge|Merge two binary search trees into one balanced binary search tree containing their combined elements.
bst_to_sorted_list|Convert the BST into a sorted doubly linked list in place. Use Left as the previous link and Right as the next link. Return the head; its Left must be null.
buy_and_sell_stock|Return the greatest profit from at most one buy followed by one sell. Return zero if no profitable transaction exists.
buy_and_sell_stock_k_times|Return the greatest profit from at most k buy/sell transactions. You may hold at most one share at a time.
buy_and_sell_stock_twice|Return the greatest profit from at most two buy/sell transactions, holding at most one share at a time.
calendar_rendering|Each tuple is an event (start, finish). Return the maximum number of simultaneous events. Events touching at an endpoint overlap.
circular_queue|Implement an integer queue using a resizable circular buffer. Initialize(capacity) resets it, Enqueue appends, Dequeue removes the oldest value, and Size reports its count. Grow the buffer when full.
closest_int_same_weight|Return the closest different nonnegative integer with the same number of set bits as the input.
collatz_checker|Check the Collatz conjecture for every integer from 1 through n: repeatedly halve even values and replace odd values by 3x+1, eventually reaching 1.
combinations|Return every k-element subset of integers 1 through n. Order of subsets does not matter.
convert_base|Convert the signed integer string from base b1 to base b2. Digits above 9 use uppercase A through F.
copy_posting_list|Deep-copy a posting list with Next and Jump references. Preserve Order and all links, and return the copied head. No node in the copy may reference an original node.
count_inversions|Count pairs of indices i < j for which A[i] > A[j].
deadlock_detection|A directed graph is given by a vertex count and (from, to) edges. Return whether it contains a directed cycle.
defective_jugs|Each jug measures an uncertain volume in [low, high]. Determine whether some sequence of jug uses guarantees a total entirely within the requested [l, h] interval. A jug may be reused.
delete_from_list|Delete the node at the supplied zero-based position from a singly linked list. Return the resulting head.
delete_kth_last_from_list|Remove the kth node from the end of a singly linked list (k = 1 removes the last node). Return the head.
delete_node_from_list|Delete the node at the supplied zero-based position without access to its predecessor. The selected node is not the tail. Return the head.
descendant_and_ancestor_in_bst|The three integers identify nodes by Data. Determine whether one candidate is a proper ancestor of the middle node and the other is its proper descendant in the BST.
directory_path_normalization|Normalize a Unix path by resolving '.', '..', and repeated slashes while respecting absolute versus relative paths.
do_lists_overlap|Find an overlapping node in two lists that may contain cycles. Return an actual shared node, or null if disjoint. The judge constructs shared tails and cycles before calling your method.
do_terminated_lists_overlap|Find the first shared node of two acyclic singly linked lists. Return that node by reference, or null if disjoint. Equal values alone do not imply overlap.
drawing_skyline|Buildings are (left, right, height) rectangles with inclusive integer endpoints. Return the skyline as maximal constant-height (left, right, height) spans, including zero-height gaps.
dutch_national_flag|Partition the array in place into values less than, equal to, and greater than the value originally at pivotIndex. Preserve every element.
element_appearing_once|Every integer appears three times except one that appears once. Return that unique integer.
enumerate_balanced_parentheses|Return all balanced strings containing numPairs pairs of parentheses. Output order does not matter.
enumerate_palindromic_decompositions|Return every partition of the text into palindromic substrings. Preserve substring order within each partition; partition order does not matter.
enumerate_trees|Return all distinct binary tree shapes with numNodes nodes. Encode each shape by breadth-first traversal: 1 for a node and 0 for null, including every null child of each real node. Shape order does not matter.
evaluate_rpn|Evaluate a comma-separated reverse Polish expression using integer arithmetic and +, -, *, /. Division truncates toward zero.
even_odd_array|Reorder the array in place so every even value precedes every odd value. Preserve all elements; internal group order is unrestricted.
even_odd_list_merge|Reorder a singly linked list by putting nodes at even zero-based positions first, followed by nodes at odd positions. Preserve relative order within each group.
fibonacci|Return the nth Fibonacci number, with F(0) = 0 and F(1) = 1.
find_missing_and_duplicate|An array of length n should contain 0 through n-1, but one value is missing and another is duplicated. Return (duplicate, missing).
find_salary_threshold|Cap every salary at one common threshold so the total equals the target payroll. Return that threshold, or -1 if the target exceeds the existing payroll.
first_missing_positive_entry|Return the smallest positive integer absent from the array.
gcd|Compute the greatest common divisor of two nonnegative integers.
graph_clone|Deep-copy the directed graph reachable from the supplied vertex. Preserve labels, duplicate edges, cycles, and sharing. No original vertex may appear in the copy.
gray_code|Return all 2^numBits distinct numBits-bit integers in an order where consecutive values differ in exactly one bit.
group_equal_entries|Rearrange (age, name) people in place so entries of the same age are contiguous. Preserve every person; group order is unrestricted.
h_index|Return the largest h such that at least h papers have at least h citations each.
hanoi|Return a legal sequence of moves transferring all rings from peg 0 to peg 1 or peg 2. A move is [sourcePeg, destinationPeg]. Never place a larger ring on a smaller ring.
huffman_coding|Given (character, frequency) pairs, return the minimum average code length achievable with a binary prefix code. Frequencies are probabilities.
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
is_array_dominated|Two teams can be reordered for a photograph. Determine whether every member of team0 can stand strictly in front of a taller member of team1. The judge checks both directions.
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
k_largest_in_heap|The array represents a max heap. Return its k largest values in any order without sorting the entire heap.
k_largest_values_in_bst|Return the k largest keys in the BST. Output order does not matter.
knapsack|Items are (weight, value) pairs. Choose each item at most once and maximize total value without exceeding capacity. Return the maximum value.
kth_largest_element_in_long_array|Return the kth largest value in the stream, counting duplicates. k is 1-based.
kth_largest_element_in_two_sorted_arrays|Return the kth smallest value in the combined sorted arrays, counting duplicates. k is 1-based despite the repository filename.
kth_largest_in_array|Return the kth largest element, counting duplicates. k is 1-based.
kth_node_in_tree|Return the Data of the kth node in inorder traversal, with k starting at 1.
largest_rectangle_under_skyline|Given unit-width histogram heights, return the area of its largest axis-aligned rectangle.
left_right_justify_text|Wrap words to the specified line width and fully justify each line by distributing spaces from the left. The last line is left justified and padded to the width.
levenshtein_distance|Return the minimum number of single-character insertions, deletions, and substitutions needed to transform one string into the other.
line_through_most_points|Return the largest number of supplied (x, y) points that lie on one straight line.
list_cyclic_right_shift|Cyclically shift the list right by k positions and return its head.
longest_contained_interval|Return the size of the longest interval of consecutive integer values contained in the input array, regardless of their positions.
longest_increasing_subarray|Return the length of the longest contiguous strictly increasing subarray.
longest_nondecreasing_subsequence|Return the length of the longest subsequence whose values never decrease. Elements need not be contiguous.
longest_subarray_with_distinct_values|Return the length of the longest contiguous subarray containing no duplicate values.
longest_subarray_with_sum_constraint|Return the maximum length of a contiguous subarray whose sum is at most k. Negative values are allowed.
longest_substring_with_matching_parentheses|Return the length of the longest contiguous substring of balanced parentheses.
look_and_say|Return the nth term of the look-and-say sequence, starting with '1'. Describe each run of identical digits by its count and digit.
lowest_common_ancestor|The integer arguments identify two nodes by Data. Return the Data of their lowest common ancestor. Parent pointers are available.
lowest_common_ancestor_in_bst|The integer arguments identify two nodes by Data. Return the Data of their lowest common ancestor in the BST.
lru_cache|Implement a least-recently-used cache. Initialize(capacity) resets it. Lookup returns -1 if missing and refreshes recency. Insert refreshes existing keys while preserving their old price; new insertions evict the least recent entry when full. Erase reports whether a key existed.
majority_element|Return the string appearing in more than half of the stream's entries. Such an entry is guaranteed to exist.
making_change|Return the minimum number of coins needed for the amount, using US denominations 100, 50, 25, 10, 5, and 1.
matrix_enclosed_regions|Change every enclosed white region ('W') into black ('B'). A white cell connected to a boundary by horizontal or vertical steps remains white. Return the updated board.
matrix_rotation|Rotate a square matrix 90 degrees clockwise and return it.
max_of_sliding_window|Traffic readings are (time, volume). For each reading, return (time, maximumVolume) over readings within the inclusive preceding time window of width w.
max_product_all_but_one|Return the greatest product obtainable by multiplying all array entries except one.
max_safe_height|Given a number of identical eggs and a maximum number of drops, return the greatest number of floors for which the highest safe floor can always be determined.
max_square_submatrix|Return the area of the largest square submatrix consisting entirely of true cells.
max_submatrix|Return the area of the largest rectangular submatrix consisting entirely of true cells.
max_sum_subarray|Return the maximum sum of a contiguous subarray. The empty subarray is permitted, giving zero when all values are negative.
max_teams_in_photograph|Given a directed acyclic graph of compatible team orderings, return the greatest number of teams on a path (count vertices).
max_trapped_water|Choose two vertical lines at array positions to hold the greatest amount of water. Return (index distance) × (smaller height) for the best pair.
max_water_trappable|Return the total water trapped between unit-width histogram bars after rain.
maximum_subarray_in_circular_array|Return the maximum contiguous subarray sum when the array is circular. The empty subarray is allowed.
minimum_distance_3_sorted_arrays|Choose one entry from each sorted array and minimize the difference between the largest and smallest chosen values. Return that difference.
minimum_points_covering_intervals|Return the minimum number of points needed to intersect every closed interval (start, end).
minimum_waiting_time|Order the queries to minimize their total waiting time before execution. Return that total, excluding each query's own processing time.
minimum_weight_path_in_a_triangle|Return the minimum sum along a path from the top to the bottom of the triangle. From column i, move to column i or i+1 in the next row.
n_queens|Return all placements of n nonattacking queens on an n×n board. Each placement lists the queen's column for every row. Placement order does not matter.
nearest_repeated_entries|Return the minimum index distance between equal words, or -1 if no word repeats.
next_permutation|Return the next lexicographic permutation. Return an empty list if the input is already the last permutation.
nonuniform_random_number|Return one of values with its corresponding probability. Repeated calls must follow that distribution; use Random.Shared as your randomness source.
number_of_score_combinations|Count unordered combinations of allowed play scores that sum to the final score. Each play may be repeated.
number_of_traversals_matrix|Count paths from the upper-left corner to the lower-right corner of an n×m grid, moving only right or down.
number_of_traversals_staircase|Count ways to climb to the top stair when each step can advance 1 through maximumStep stairs.
offline_sampling|Rearrange A in place so its first k entries form a uniformly random k-element subset. Preserve the entire array's multiset.
online_median|Return the median after each successive stream entry. For an even prefix length, average its two central entries.
online_sampling|Return a uniformly random k-element sample of the stream without replacement. Every k-element subset must be equally likely.
painting|Flip the color of the connected component containing (x, y), using horizontal and vertical adjacency. Return the updated image.
parity|Return 1 if the 64-bit integer has an odd number of set bits, otherwise 0.
pascal_triangle|Return the first numRows rows of Pascal's triangle, starting with [1].
path_sum|Determine whether a root-to-leaf path has the requested sum of node values.
permutations|Return every permutation of the input values. Preserve each permutation's order; the order of permutations does not matter.
phone_number_mnemonic|Return all letter mnemonics for a digit string using the standard telephone mapping. Digits 0 and 1 map to themselves.
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
refueling_schedule|Return any city from which a circular trip can finish without running out of fuel. Each gallon permits 20 miles; distances[i] is the distance to the next city.
regular_expression|Match the string against a simplified regular expression with '.', '*', '^', and '$'. An unanchored pattern may match a substring.
remove_duplicates|Names are (firstName, lastName) pairs. Eliminate duplicates by first name and return the distinct first names. Output order does not matter.
remove_duplicates_from_sorted_list|Remove repeated values from a sorted singly linked list, keeping one node per distinct value.
replace_and_remove|Process only the first size characters: delete each 'b' and replace each 'a' with two 'd' characters. Return the transformed characters, excluding unused buffer capacity.
reverse_bits|Reverse all 64 bits of the integer and return the resulting bit pattern.
reverse_digits|Reverse the decimal digits of the integer, preserving its sign.
reverse_list|Reverse a singly linked list and return its new head.
reverse_sublist|Reverse the list segment from start through finish, using inclusive 1-based positions. Return the head.
reverse_words|Reverse word order in a space-separated string. Preserve the characters within each word.
road_network|Existing highways and candidate proposals are (city0, city1, distance). Return the proposal that most reduces the total of all-pairs shortest path distances among n cities.
roman_to_integer|Convert a Roman numeral into its integer value using subtractive notation.
rook_attack|If a matrix cell is zero, clear its entire row and column. Base the decision on the original matrix and return the updated matrix.
rotate_array|Cyclically rotate the array right by rotateAmount positions and return it.
run_length_compression|Implement both run-length Encoding and Decoding. Encoded runs contain a decimal count followed by a character, for example '3a2b' represents 'aaabb'.
search_entry_equal_to_index|Find any index i for which sorted A[i] equals i. Return -1 only when no such index exists.
search_first_greater_value_in_bst|Return the smallest BST key strictly greater than k, or -1 if none exists.
search_first_key|Return the first index of k in the sorted array, or -1 if absent.
search_for_min_max_in_array|Return (minimum, maximum) for the array using as few comparisons as possible.
search_frequent_items|Return each string occurring more than streamLength/k times. Output order does not matter.
search_in_bst|Search the BST for key and return its value, or -1 when absent.
search_in_list|Search the linked list for key and return its value, or -1 when absent.
search_maze|Return a path of (row, column) coordinates from start to end, moving horizontally or vertically through white cells (0). Black cells (1) are blocked. Include both endpoints; return an empty list when unreachable.
search_row_col_sorted_matrix|Determine whether the target occurs in a matrix whose rows and columns are each sorted in nondecreasing order.
search_shifted_sorted_array|Return the index of the smallest value in a cyclically shifted sorted array of distinct values.
search_unknown_length_array|Return the index of k in a sorted array, or -1 if absent. Practice searching using indexed access without relying on the array length.
smallest_nonconstructible_value|Return the smallest positive sum that cannot be formed from a subset of the nonnegative input values, each used at most once.
smallest_subarray_covering_all_values|Return inclusive (start, end) indices of a shortest paragraph slice containing the keyword sequence in order. Keywords may repeat. The judge validates coverage and minimum length.
smallest_subarray_covering_set|Return inclusive (start, end) indices of a shortest paragraph slice containing every keyword. Keyword order does not matter. The judge validates coverage and minimum length.
snake_string|Arrange the characters on three alternating rows in a sinusoidal pattern, then read the rows from top to bottom. The top row starts at input index 1, middle at 0, bottom at 3.
sort_almost_sorted_array|Sort an array in which every entry is at most k positions from its final sorted location.
sort_increasing_decreasing_array|Sort an array composed of alternating increasing and decreasing runs.
sort_list|Sort a singly linked list in nondecreasing order and return its head.
sorted_array_remove_dups|Return the distinct entries of the sorted array in increasing order.
sorted_arrays_merge|Merge all sorted arrays into one sorted array, preserving duplicates.
sorted_list_to_bst|Convert a sorted doubly linked list into a BST. BinaryTreeNode.Left is the previous link and Right is the next link on input; those fields become tree children on output. Return a tree with the original inorder contents.
sorted_lists_merge|Merge two sorted singly linked lists into one sorted list, preserving duplicates.
spiral_ordering|Return the square matrix's entries in clockwise spiral order, starting at its top-left corner.
spreadsheet_encoding|Convert a spreadsheet column label to its 1-based number: A = 1, Z = 26, AA = 27.
stack_with_max|Implement an integer stack supporting Push, Pop, Empty, and Max. Initialize resets it. Max returns its greatest entry.
string_decompositions_into_dictionary_words|Return all starting indices where concatenating every supplied word exactly once produces a substring. All words have equal length and may repeat.
string_integer_interconversion|Implement decimal IntToString and StringToInt, including negative integers. Do not use built-in numeric/string conversion routines.
string_transformability|Return the minimum number of one-character substitutions needed to transform the source into the target using only dictionary words, or -1 if impossible.
substring_match|Return the first index of the pattern in the text, or -1 if absent.
successor_in_tree|Return the Data of the inorder successor of the node identified by nodeIdx (a Data value), or -1 when absent. Parent pointers are available.
sudoku_solve|Fill the Sudoku board in place. Preserve every original clue; every row, column, and subgrid must contain each digit exactly once. Zero denotes an empty cell.
sum_root_to_leaf|Node values are binary digits. Interpret each root-to-leaf path as a binary integer and return the sum of those integers.
sunset_view|Buildings arrive east to west. Return indices of buildings that can see the sunset to the west, from west to east. A building is blocked by an equal or taller building to its west.
swap_bits|Swap bits at zero-based positions i and j in a 64-bit integer, leaving every other bit unchanged.
task_pairing|Pair task durations to minimize the maximum pair sum. Return pairs produced by sorting durations and pairing smallest with largest, in ascending order of the smaller member.
three_sum|Determine whether three values sum to the target. This EPI variant permits reusing the same element more than once.
tree_connect_leaves|Return leaf Data values from left to right.
tree_exterior|Return the tree's boundary Data values counterclockwise: root, left boundary, leaves from left to right, then right boundary from bottom to top. Do not repeat nodes.
tree_from_preorder_inorder|Reconstruct the binary tree from its preorder and inorder traversals. Node values are distinct.
tree_from_preorder_with_null|Reconstruct a binary tree from preorder tokens. The string 'null' marks an absent child; other tokens are integer values.
tree_inorder|Return the binary tree's inorder traversal (left, root, right).
tree_level_order|Return the binary tree's values grouped by level, from top to bottom and left to right.
tree_postorder|Return the binary tree's postorder traversal (left, right, root).
tree_preorder|Return the binary tree's preorder traversal (root, left, right).
tree_right_sibling|Populate each node's Next pointer with its right sibling on the same level, or null at the end. The input is a perfect binary tree. The judge traverses the Next chains to verify them.
tree_with_parent_inorder|Return the inorder traversal of a tree with Parent pointers, using constant auxiliary space.
two_sorted_arrays_merge|Merge the first m sorted entries of A and first n sorted entries of B into A's buffer. Return the merged array.
uniform_random_number|Return a uniformly distributed random integer in the inclusive range [lower, upper]. Successive calls must be independent. You may use Random.Shared.Next(2) as a fair random bit source.
valid_ip_addresses|Insert three dots into the digit string to produce all valid IPv4 addresses. Parts must be 0 through 255 and must not have leading zeros unless exactly '0'.
zip_list|Reorder a list L0,L1,…,Ln into L0,Ln,L1,Ln-1,… and return its head.
"""
notes = dict(line.split('|', 1) for line in NOTES.strip().splitlines())
COMPACT_EXAMPLES = {
 'absent_value_array': ('stream = [0, 1, 3]', 'All contract checks pass', 'Returning 2 is valid; any nonnegative missing integer is accepted.'),
 'minimum_distance_3_sorted_arrays': ('sortedArrays = [[1, 4], [2, 5], [3, 6]]', '2', 'Choosing 1, 2, and 3 gives a range of 2.'),
 'string_transformability': ('dictionary = ["cat", "cot", "cog", "dog"], source = "cat", target = "dog"', '3', 'cat → cot → cog → dog requires three single-character changes.'),
 'drawing_skyline': ('buildings = [[1, 3, 2], [2, 4, 3]]', '[[1, 1, 2], [2, 4, 3]]', 'The taller building controls the height from coordinate 2 through 4.'),
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
    for file in (ROOT/'epi_judge_python').glob('*.py'):
        text = file.read_text()
        for testfile in re.findall(r"['\"]([a-z0-9_]+)\.tsv['\"]", text):
            sources[testfile] = file
    result = []
    for p in problems:
        id = p['id']
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
        topic = re.sub(r'^(?:Chapter\s+)?\d+[.:]?\s*','',topic).capitalize()
        if topic == 'C# Additional Problems': topic = 'Additional problems'
        constraints = ['Use the public C# signatures shown below. Run checks three visible corpus cases; Submit checks the complete corpus.']
        if any('binary_tree' in t or 'linked_list' in t for t in p['argumentTypes']) or any('Node' in m[0]+m[2] for m in methods):
            constraints += ['Shared types: ListNode<T> has Data and Next. BinaryTreeNode<T> has Data, Left, Right, Parent, Next, and Size. Constructors take the data value. Tree inputs use compact level-order JSON with null children; linked lists use JSON arrays.']
        if id == 'copy_posting_list': constraints += ['PostingListNode has Order, Next, and Jump; its constructor takes Order.']
        if id == 'graph_clone': constraints += ['GraphVertex has Label and List<GraphVertex> Edges; its constructor takes Label.']
        if p['resultType']=='void': constraints += ['The judge validates behavior, mutations, node identity, or repeated random samples. You do not return a pass/fail flag.']
        if any('tuple' in t for t in p['argumentTypes']+[p['resultType']]): constraints += ['Record values use C# value tuples. Tuple elements are available as Item1, Item2, and so on in the order described.']
        lines=(ROOT/'test_data'/p['testDataFile']).read_text().splitlines()[1:]
        examples=[]
        for line in lines[:2]:
            fields=line.split('\t'); count=len(p['argumentTypes'])
            if sum(map(len, fields[:count+1]))>2500: continue
            examples.append(dict(Input=', '.join(f'{name} = {value}' for name,value in zip(argnames,fields)),Output='All contract checks pass' if p['resultType']=='void' else fields[count],Explanation='Serialized test protocol. For a custom adapter, the output is the validated property (such as path existence, interval length, or tree height), rather than your raw return object.' if id in CUSTOM else 'One case from the shared EPI test corpus.'))
        if not examples and id in COMPACT_EXAMPLES:
            value, output, explanation = COMPACT_EXAMPLES[id]
            examples.append(dict(Input=value, Output=output, Explanation=explanation))
        comparison = 'ordered'
        if id in {'combinations','power_set'}: comparison='nested'
        elif id in {'enumerate_balanced_parentheses','enumerate_palindromic_decompositions','enumerate_trees','k_closest_stars','k_largest_in_heap','k_largest_values_in_bst','n_queens','permutations','phone_number_mnemonic','remove_duplicates','search_frequent_items','valid_ip_addresses'}: comparison='unordered'
        result.append(dict(Id=id,Title=title,Topic=topic,Difficulty='Unrated',Description=notes[id],Constraints=constraints,Signature='\n'.join(f'{t} {n}({a})' for t,n,a in methods),StarterCode=code,Examples=examples,Invocation=invocation,ArgumentCount=len(p['argumentTypes']),TestCount=len(lines),Comparison=comparison,ResultType=p['resultType']))
    result.sort(key=lambda p: (p['Topic'],p['Title'],p['Id']))
    (ROOT/'EpiJudge.Runner/catalog.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Generated {len(result)} entries; 3 existing curated entries are retained ({len(result)+3} total).')

if __name__=='__main__': main()
