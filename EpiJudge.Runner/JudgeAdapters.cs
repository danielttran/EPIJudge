using System.Text.Json;
using EpiJudge.TestFramework;

namespace EpiJudge.Runner;

public sealed class JudgeValidationException(string message) : Exception(message);

// These adapters implement the protocols that have no single expected output.
// They run in the submission process, retaining node identity and mutations.
public static class JudgeAdapters
{
    public static T Arg<T>(JsonElement[] a, int i) => a[i].Deserialize<T>(JudgeJson.Options)!;
    private static void Check(bool condition, string message = "The result violates the problem contract.")
    {
        if (!condition) throw new JudgeValidationException(message);
    }
    private static bool Same<T>(IEnumerable<T> a, IEnumerable<T> b) where T : notnull
    {
        var left = a.GroupBy(x => x).ToDictionary(g => g.Key, g => g.Count());
        var right = b.GroupBy(x => x).ToDictionary(g => g.Key, g => g.Count());
        return left.Count == right.Count && left.All(pair => right.GetValueOrDefault(pair.Key) == pair.Value);
    }
    public static List<ListNode<int>> Nodes(ListNode<int>? head)
    {
        var nodes = new List<ListNode<int>>();
        var seen = new HashSet<ListNode<int>>(ReferenceEqualityComparer.Instance);
        while (head is not null && seen.Add(head)) { nodes.Add(head); head = head.Next; }
        return nodes;
    }
    private static List<int> Inorder(BinaryTreeNode<int>? root)
    {
        var output = new List<int>();
        var seen = new HashSet<BinaryTreeNode<int>>(ReferenceEqualityComparer.Instance);
        void Visit(BinaryTreeNode<int>? n)
        {
            if (n is null) return;
            Check(seen.Add(n), "The tree contains a cycle or a shared child.");
            Visit(n.Left); output.Add(n.Data); Visit(n.Right);
        }
        Visit(root); return output;
    }
    public static object? Invoke(string id, JsonElement[] a, dynamic s)
    {
        switch (id)
        {
            case "absent_value_array":
            {
                int missing = s.FindMissingElement(Arg<List<int>>(a, 0));
                Check(missing >= 0 && !Arg<List<int>>(a, 0).Contains(missing)); return true;
            }
            case "alternating_array":
            case "even_odd_array":
            case "dutch_national_flag":
            {
                var values = Arg<List<int>>(a, 0); var original = values.ToArray();
                if (id == "alternating_array") s.Rearrange(values);
                else if (id == "even_odd_array") s.EvenOdd(values);
                else s.DutchFlagPartition(Arg<int>(a, 1), values);
                Check(Same(original, values), "Preserve every input element.");
                if (id == "alternating_array")
                    for (var i = 1; i < values.Count; i++) Check(i % 2 == 1 ? values[i-1] <= values[i] : values[i-1] >= values[i]);
                else if (id == "even_odd_array") Check(values.Select(x => (x & 1)).SequenceEqual(values.Select(x => x & 1).Order()));
                else
                {
                    var pivot = original[Arg<int>(a, 1)];
                    var partitions = values.Select(x => x.CompareTo(pivot)).ToArray();
                    Check(partitions.SequenceEqual(partitions.Order()));
                }
                return true;
            }
            case "group_equal_entries":
            {
                var people = Arg<List<(int, string)>>(a, 0); var original = people.ToArray();
                s.GroupByAge(people); Check(Same(original, people));
                var completed = new HashSet<int>(); int? previous = null;
                foreach (var person in people)
                {
                    if (person.Item1 != previous) { Check(completed.Add(person.Item1)); previous = person.Item1; }
                }
                return true;
            }
            case "gray_code":
            {
                int n = Arg<int>(a, 0); List<int> result = s.GrayCode(n);
                Check(result.Count == (1 << n) && result.Distinct().Count() == result.Count);
                Check(result.All(x => x >= 0 && x < (1 << n)));
                for (int i = 1; i < result.Count; i++) { int x = result[i] ^ result[i-1]; Check(x != 0 && (x & (x-1)) == 0); }
                return true;
            }
            case "hanoi":
            {
                int n = Arg<int>(a, 0); List<List<int>> moves = s.ComputeTowerHanoi(n);
                var pegs = new[] { new Stack<int>(Enumerable.Range(1, n).Reverse()), new Stack<int>(), new Stack<int>() };
                foreach (var move in moves)
                {
                    Check(move.Count == 2 && move[0] is >= 0 and < 3 && move[1] is >= 0 and < 3 && move[0] != move[1]);
                    var from = pegs[move[0]]; var to = pegs[move[1]];
                    Check(from.Count > 0 && (to.Count == 0 || from.Peek() < to.Peek())); to.Push(from.Pop());
                }
                Check(pegs[0].Count == 0 && (pegs[1].Count == n || pegs[2].Count == n)); return true;
            }
            case "is_array_dominated":
                Check((bool)s.ValidPlacementExists(Arg<List<int>>(a, 0), Arg<List<int>>(a, 1)) == Arg<bool>(a, 2));
                Check((bool)s.ValidPlacementExists(Arg<List<int>>(a, 1), Arg<List<int>>(a, 0)) == Arg<bool>(a, 3)); return true;
            case "is_string_decomposable_into_words":
            {
                var domain = Arg<string>(a, 0); var dictionary = Arg<HashSet<string>>(a, 1);
                List<string> words = s.DecomposeIntoDictionaryWords(domain, new HashSet<string>(dictionary));
                Check(Arg<bool>(a, 2) ? string.Concat(words) == domain && words.All(dictionary.Contains) : words.Count == 0); return true;
            }
            case "search_entry_equal_to_index":
            {
                var values = Arg<List<int>>(a, 0); int index = s.SearchEntryEqualToItsIndex(new List<int>(values));
                Check(index == -1 ? !values.Where((x, i) => x == i).Any() : index >= 0 && index < values.Count && values[index] == index); return true;
            }
            case "refueling_schedule":
            {
                var gallons = Arg<List<int>>(a, 0); var distances = Arg<List<int>>(a, 1);
                int start = s.FindAmpleCity(new List<int>(gallons), new List<int>(distances));
                Check(start >= 0 && start < gallons.Count); long tank = 0;
                for (int i = 0; i < gallons.Count; i++) { int city = (start+i)%gallons.Count; tank += gallons[city]*20L-distances[city]; Check(tank >= 0); }
                return true;
            }
            case "run_length_compression":
                Check((string)s.Decoding(Arg<string>(a, 0)) == Arg<string>(a, 1));
                Check((string)s.Encoding(Arg<string>(a, 1)) == Arg<string>(a, 0)); return true;
            case "string_integer_interconversion":
                Check(int.TryParse((string)s.IntToString(Arg<int>(a, 0)), out var parsed) && parsed == Arg<int>(a, 0));
                Check((int)s.StringToInt(Arg<string>(a, 1)) == Arg<int>(a, 0)); return true;
            case "pivot_list":
            {
                var head = Arg<ListNode<int>?>(a, 0); int pivot = Arg<int>(a, 1);
                var original = Nodes(head).Select(node => node.Data).ToArray();
                ListNode<int>? result = s.ListPivoting(head, pivot); var nodes = Nodes(result);
                Check(nodes.Count == 0 || nodes[^1].Next is null, "Output must not contain a cycle.");
                Check(Same(original, nodes.Select(x => x.Data)));
                var groups = nodes.Select(x => x.Data.CompareTo(pivot)).ToArray(); Check(groups.SequenceEqual(groups.Order())); return true;
            }
            case "is_list_cyclic":
            {
                var head = Arg<ListNode<int>?>(a, 0); var nodes = Nodes(head); int value = Arg<int>(a, 1);
                var start = value == -1 ? null : nodes.First(x => x.Data == value);
                if (start is not null) nodes[^1].Next = start;
                ListNode<int>? result = s.HasCycle(head);
                Check(ReferenceEquals(result, start), "Return the node at the beginning of the cycle, or null."); return true;
            }
            case "do_terminated_lists_overlap":
            case "do_lists_overlap":
            {
                var first = Arg<ListNode<int>?>(a, 0); var second = Arg<ListNode<int>?>(a, 1); var common = Arg<ListNode<int>?>(a, 2);
                var firstNodes = Nodes(first); var secondNodes = Nodes(second);
                if (firstNodes.Count == 0) first = common; else firstNodes[^1].Next = common;
                if (secondNodes.Count == 0) second = common; else secondNodes[^1].Next = common;
                if (id == "do_lists_overlap")
                {
                    var n0 = Nodes(first); var n1 = Nodes(second); int c0 = Arg<int>(a, 3), c1 = Arg<int>(a, 4);
                    if (c0 >= 0) n0[^1].Next = n0[c0];
                    if (c1 >= 0) n1[^1].Next = n1[c1];
                }
                var overlap = Nodes(first).Intersect(Nodes(second)).ToHashSet();
                ListNode<int>? result = s.OverlappingLists(first, second);
                Check(id == "do_terminated_lists_overlap" ? ReferenceEquals(result, common) : overlap.Count == 0 ? result is null : result is not null && overlap.Contains(result)); return true;
            }
            case "copy_posting_list":
            {
                var input = Arg<List<(int,int)>>(a, 0); var nodes = input.Select(x => new PostingListNode(x.Item1)).ToArray();
                for (int i = 0; i < nodes.Length; i++)
                {
                    nodes[i].Next = i+1 < nodes.Length ? nodes[i+1] : null;
                    nodes[i].Jump = input[i].Item2 == -1 ? null : nodes.First(x => x.Order == input[i].Item2);
                }
                PostingListNode? copy = s.CopyPostingsList(nodes.FirstOrDefault());
                var copies = new List<PostingListNode>(); var seen = new HashSet<PostingListNode>();
                while (copy is not null) { Check(seen.Add(copy) && !nodes.Contains(copy)); copies.Add(copy); copy = copy.Next; }
                Check(copies.Count == nodes.Length);
                for (int i = 0; i < nodes.Length; i++)
                {
                    Check(copies[i].Order == input[i].Item1);
                    int j = input.FindIndex(x => x.Item1 == input[i].Item2);
                    Check(ReferenceEquals(copies[i].Jump, input[i].Item2 == -1 ? null : copies[j]));
                }
                return true;
            }
            case "graph_clone":
            {
                var graph = Enumerable.Range(0, Arg<int>(a, 0)).Select(x => new GraphVertex(x)).ToArray();
                foreach (var (from, to) in Arg<List<(int,int)>>(a, 1)) graph[from].Edges.Add(graph[to]);
                var adjacency = graph.Select(node => node.Edges.Select(edge => edge.Label).ToArray()).ToArray();
                var reachable = new HashSet<int>(); var originals = new Queue<GraphVertex>(); originals.Enqueue(graph[0]);
                while (originals.TryDequeue(out var node)) if (reachable.Add(node.Label)) foreach (var edge in node.Edges) originals.Enqueue(edge);
                GraphVertex result = s.CloneGraph(graph[0]); Check(result is not null && result.Label == 0);
                var copies = new Dictionary<int,GraphVertex>(); var queue = new Queue<GraphVertex>(); queue.Enqueue(result!);
                while (queue.TryDequeue(out var node))
                {
                    Check(node.Label >= 0 && node.Label < graph.Length && !graph.Contains(node));
                    if (copies.TryGetValue(node.Label, out var previous)) { Check(ReferenceEquals(previous, node)); continue; }
                    copies[node.Label] = node;
                    Check(Same(node.Edges.Select(x => x.Label), adjacency[node.Label]));
                    foreach (var edge in node.Edges) queue.Enqueue(edge);
                }
                Check(reachable.SetEquals(copies.Keys)); return true;
            }
            case "sorted_list_to_bst":
            {
                var values = Arg<List<int>>(a, 0); BinaryTreeNode<int>? head = null, tail = null;
                foreach (int x in values) { var node = new BinaryTreeNode<int>(x) { Left = tail }; if (tail is null) head = node; else tail.Right = node; tail = node; }
                BinaryTreeNode<int>? tree = s.BuildBstFromSortedDoublyList(head, values.Count);
                Check(Inorder(tree).SequenceEqual(values)); return true;
            }
            case "sudoku_solve":
            {
                var original = Arg<List<List<int>>>(a, 0); var board = Arg<List<List<int>>>(a, 0);
                s.SolveSudoku(board); int n = original.Count, width = (int)Math.Sqrt(n);
                Check(board.Count == n && board.All(row => row.Count == n));
                for (int r = 0; r < n; r++) for (int c = 0; c < n; c++)
                    Check(board[r][c] >= 1 && board[r][c] <= n && (original[r][c] == 0 || original[r][c] == board[r][c]));
                for (int i = 0; i < n; i++)
                {
                    Check(board[i].Distinct().Count() == n && board.Select(row => row[i]).Distinct().Count() == n);
                    var block = new List<int>(); for (int r = 0; r < width; r++) for (int c = 0; c < width; c++) block.Add(board[(i/width)*width+r][(i%width)*width+c]);
                    Check(block.Distinct().Count() == n);
                }
                return true;
            }
            case "adding_credits":
                foreach (var (op, text, value) in Arg<List<(string,string,int)>>(a, 0))
                    switch (op)
                    {
                        case "ClientsCreditsInfo": s.Initialize(); break;
                        case "insert": s.Insert(text, value); break;
                        case "remove": Check((bool)s.Remove(text) == (value == 1)); break;
                        case "lookup": Check((int)s.Lookup(text) == value); break;
                        case "add_all": s.AddAll(value); break;
                        case "max": Check((string)s.Max() == text); break;
                        default: throw new InvalidDataException(op);
                    }
                return true;
            case "lru_cache":
                foreach (var (op, key, value) in Arg<List<(string,int,int)>>(a, 0))
                    switch (op)
                    {
                        case "LruCache": s.Initialize(key); break;
                        case "lookup": Check((int)s.Lookup(key) == value); break;
                        case "insert": s.Insert(key, value); break;
                        case "erase": Check((bool)s.Erase(key) == (value == 1)); break;
                        default: throw new InvalidDataException(op);
                    }
                return true;
            case "circular_queue": case "queue_from_stacks": case "queue_with_max": case "stack_with_max":
                if (id == "circular_queue") s.Initialize(1); else s.Initialize();
                foreach (var (op, value) in Arg<List<(string,int)>>(a, 0))
                    switch (op)
                    {
                        case "Queue": if (id == "circular_queue") s.Initialize(value); else s.Initialize(); break;
                        case "Stack": case "QueueWithMax": s.Initialize(); break;
                        case "enqueue": s.Enqueue(value); break;
                        case "dequeue": Check((int)s.Dequeue() == value); break;
                        case "size": Check((int)s.Size() == value); break;
                        case "push": s.Push(value); break;
                        case "pop": Check((int)s.Pop() == value); break;
                        case "max": Check((int)s.Max() == value); break;
                        case "empty": Check((bool)s.Empty() == (value == 1)); break;
                        default: throw new InvalidDataException(op);
                    }
                return true;
            case "nonuniform_random_number": case "uniform_random_number": case "random_permutation":
            case "random_subset": case "offline_sampling": case "online_sampling":
                return RandomJudge.Validate(id, a, s);
            case "bst_from_sorted_array":
            {
                var values = Arg<List<int>>(a, 0); BinaryTreeNode<int>? tree = s.BuildMinHeightBstFromSortedArray(new List<int>(values));
                Check(Inorder(tree).SequenceEqual(values));
                int Height(BinaryTreeNode<int>? n) => n is null ? 0 : 1+Math.Max(Height(n.Left), Height(n.Right));
                return Height(tree);
            }
            case "bst_to_sorted_list":
            {
                var input = Arg<BinaryTreeNode<int>?>(a, 0); var expected = Inorder(input);
                BinaryTreeNode<int>? head = s.BstToDoublyLinkedList(input);
                Check(head is null || head.Left is null);
                var visited = new HashSet<BinaryTreeNode<int>>(); var output = new List<int>();
                BinaryTreeNode<int>? previous = null;
                while (head is not null)
                {
                    Check(visited.Add(head) && ReferenceEquals(head.Left, previous)); output.Add(head.Data); previous = head; head = head.Right;
                }
                Check(output.SequenceEqual(expected)); return output;
            }
            case "tree_right_sibling":
            {
                var root = Arg<BinaryTreeNode<int>?>(a, 0); var levels = new List<List<BinaryTreeNode<int>>>();
                var level = root is null ? new List<BinaryTreeNode<int>>() : new List<BinaryTreeNode<int>> { root };
                while (level.Count > 0)
                {
                    levels.Add(level); var next = new List<BinaryTreeNode<int>>();
                    foreach (var node in level) { if (node.Left is not null) next.Add(node.Left); if (node.Right is not null) next.Add(node.Right); }
                    level = next;
                }
                s.ConstructRightSibling(root);
                foreach (var nodes in levels) for (int i = 0; i < nodes.Count; i++) Check(ReferenceEquals(nodes[i].Next, i+1 < nodes.Count ? nodes[i+1] : null));
                return levels.Select(nodes => nodes.Select(node => node.Data).ToList()).ToList();
            }
            case "search_maze":
            {
                var maze = Arg<List<List<int>>>(a, 0); var start = Arg<(int,int)>(a, 1); var end = Arg<(int,int)>(a, 2);
                List<(int,int)> path = s.SearchMaze(Arg<List<List<int>>>(a, 0), start, end);
                if (path.Count == 0) return start == end;
                Check(path[0] == start && path[^1] == end);
                for (int i = 0; i < path.Count; i++)
                {
                    var (r,c) = path[i]; Check(r >= 0 && r < maze.Count && c >= 0 && c < maze[r].Count && maze[r][c] == 0);
                    if (i > 0) Check(Math.Abs(r-path[i-1].Item1)+Math.Abs(c-path[i-1].Item2) == 1);
                }
                return true;
            }
            case "smallest_subarray_covering_set": case "smallest_subarray_covering_all_values":
            {
                var paragraph = Arg<List<string>>(a, 0); var keywords = Arg<List<string>>(a, 1);
                (int,int) range = id == "smallest_subarray_covering_set"
                    ? ((int,int))s.FindSmallestSubarrayCoveringSet(new List<string>(paragraph), new HashSet<string>(keywords))
                    : ((int,int))s.FindSmallestSequentiallyCoveringSubset(new List<string>(paragraph), new List<string>(keywords));
                Check(range.Item1 >= 0 && range.Item2 >= range.Item1 && range.Item2 < paragraph.Count);
                var slice = paragraph.Skip(range.Item1).Take(range.Item2-range.Item1+1).ToList();
                if (id == "smallest_subarray_covering_set") Check(new HashSet<string>(keywords).IsSubsetOf(slice));
                else { int k = 0; foreach (var word in slice) if (k < keywords.Count && word == keywords[k]) k++; Check(k == keywords.Count); }
                return range.Item2-range.Item1+1;
            }
            default: throw new InvalidOperationException("Missing judge adapter: " + id);
        }
    }
}
