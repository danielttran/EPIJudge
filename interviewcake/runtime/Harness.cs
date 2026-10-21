using System.Diagnostics;
using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text;
internal sealed class ContractError(string message) : Exception(message);
internal sealed class NeedChoice(int lower, int upper) : Exception { public int Lower = lower, Upper = upper; }
internal static class Harness
{
    static readonly JsonSerializerOptions Json = new() { IncludeFields = true };
    // CONFIGURATION
    static void Check(bool condition, string message = "The result violates the bank contract.") { if (!condition) throw new ContractError(message); }
    static object Fresh() => Activator.CreateInstance(Assembly.GetExecutingAssembly().GetType(ClassName)!)!;
    static object? Call(object instance, string name, params object?[] args)
    {
        try { return instance.GetType().GetMethod(name)!.Invoke(instance, args); }
        catch (TargetInvocationException ex) { throw ex.InnerException ?? ex; }
    }
    static object? Load(JsonElement value, string kind)
    {
        switch (kind)
        {
            case "tree":
                {
                    var a = value.EnumerateArray().ToArray(); if (a.Length == 0) return null;
                    var root = new BinaryTreeNode(a[0].GetInt32()); var q = new Queue<BinaryTreeNode>(); q.Enqueue(root); int i = 1;
                    while (q.TryDequeue(out var n)) { if (i < a.Length && a[i].ValueKind != JsonValueKind.Null) { n.Left = new(a[i].GetInt32()); q.Enqueue(n.Left); } i++; if (i < a.Length && a[i].ValueKind != JsonValueKind.Null) { n.Right = new(a[i].GetInt32()); q.Enqueue(n.Right); } i++; }
                    return root;
                }
            case "list": { LinkedListNode? head = null; foreach (var v in value.EnumerateArray().Reverse()) head = new(v.GetInt32(), head); return head; }
            case "graph": { var a = value.EnumerateArray().ToArray(); var nn = a.Select((_, i) => new GraphNode("v" + i)).ToArray(); for (int i = 0; i < nn.Length; i++) foreach (var j in a[i].EnumerateArray()) nn[i].Neighbors.Add(nn[j.GetInt32()]); return nn; }
            case "meetings": return value.EnumerateArray().Select(a => new Meeting(a[0].GetInt32(), a[1].GetInt32())).ToList();
            case "rect": return new Rectangle(value[0].GetInt32(), value[1].GetInt32(), value[2].GetInt32(), value[3].GetInt32());
            case "cakes": return value.EnumerateArray().Select(a => new CakeType(a[0].GetInt32(), a[1].GetInt64())).ToArray();
            case "chars": return value.GetString()!.ToCharArray();
            case "i": return value.GetInt32();
            case "l": return value.GetInt64();
            case "s": case "files": return value.GetString()!;
            case "ai": return value.Deserialize<int[]>();
            case "as": return value.Deserialize<string[]>();
            case "map": return value.Deserialize<Dictionary<string, string[]>>();
            default: throw new InvalidOperationException("Unknown parameter kind " + kind);
        }
    }
    static List<LinkedListNode> ListNodes(LinkedListNode? head)
    {
        var nodes = new List<LinkedListNode>(); var seen = new HashSet<LinkedListNode>();
        while (head is not null) { Check(seen.Add(head), "Output list contains a cycle."); nodes.Add(head); head = head.Next; }
        return nodes;
    }
    static List<BinaryTreeNode> TreeNodes(BinaryTreeNode? root)
    {
        var result = new List<BinaryTreeNode>(); var seen = new HashSet<BinaryTreeNode>(); var q = new Stack<BinaryTreeNode>(); if (root is not null) q.Push(root);
        while (q.TryPop(out var n)) { Check(seen.Add(n), "Input must remain a tree."); result.Add(n); if (n.Left is not null) q.Push(n.Left); if (n.Right is not null) q.Push(n.Right); }
        return result;
    }
    static object? Dump(object? v, string kind = "")
    {
        if (kind == "list" && v is null) return Array.Empty<int>();
        if (v is null) return null;
        return kind switch
        {
            "tree" => TreeNodes((BinaryTreeNode)v).Select(n => new object?[] { n.Value, n.Left?.Value, n.Right?.Value }).ToArray(),
            "list" => ListNodes((LinkedListNode)v).Select(n => n.Value).ToArray(),
            "meetings" => ((IEnumerable<Meeting>)v).Select(n => new[] { n.StartTime, n.EndTime }).ToArray(),
            "rect" => new[] { ((Rectangle)v).LeftX, ((Rectangle)v).BottomY, ((Rectangle)v).Width, ((Rectangle)v).Height },
            "cakes" => ((CakeType[])v).Select(n => new long[] { n.Weight, n.Value }).ToArray(),
            "chars" => new string((char[])v),
            "pairs" => ((IEnumerable<FilePaths>)v).Select(n => new[] { n.OriginalPath, n.DuplicatePath }).ToArray(),
            _ => v
        };
    }
    static string Serialize(object? value) => JsonSerializer.Serialize(value, Json);
    static Action Preserve(object?[] args)
    {
        var tree = args.OfType<BinaryTreeNode>().SelectMany(TreeNodes).ToArray();
        var tv = tree.Select(n => (n.Value, n.Left, n.Right)).ToArray();
        var lists = args.OfType<LinkedListNode>().SelectMany(ListNodes).ToArray();
        var lv = lists.Select(n => (n.Value, n.Next)).ToArray();
        var before = args.Select((v, i) => Serialize(Dump(v, Kinds[i]))).ToArray();
        var meetings = args.OfType<List<Meeting>>().Select(v => (Container: v, Elements: v.ToArray(), Fields: v.Select(n => (n.StartTime, n.EndTime)).ToArray())).ToArray();
        var cakes = args.OfType<CakeType[]>().Select(v => (Container: v, Elements: v.ToArray(), Fields: v.Select(n => (n.Weight, n.Value)).ToArray())).ToArray();
        var maps = args.OfType<Dictionary<string, string[]>>().Select(v => (Container: v, Elements: v.ToDictionary(pair => pair.Key, pair => pair.Value))).ToArray();
        return () =>
        {
            for (int i = 0; i < tree.Length; i++) Check((tree[i].Value, tree[i].Left, tree[i].Right) == tv[i], "Tree values and links must remain unchanged.");
            for (int i = 0; i < lists.Length; i++) Check((lists[i].Value, lists[i].Next) == lv[i], "List values and links must remain unchanged.");
            foreach (var item in meetings) Check(item.Container.Count == item.Elements.Length && item.Container.Select((n, i) => ReferenceEquals(n, item.Elements[i]) && (n.StartTime, n.EndTime) == item.Fields[i]).All(v => v), "Meeting objects and their order must remain unchanged.");
            foreach (var item in cakes) Check(item.Container.Length == item.Elements.Length && item.Container.Select((n, i) => ReferenceEquals(n, item.Elements[i]) && (n.Weight, n.Value) == item.Fields[i]).All(v => v), "Cake objects and their order must remain unchanged.");
            foreach (var item in maps) Check(item.Container.Count == item.Elements.Count && item.Elements.All(pair => item.Container.TryGetValue(pair.Key, out var a) && ReferenceEquals(a, pair.Value)), "Neighbor arrays must retain their identities.");
            for (int i = 0; i < args.Length; i++) Check(Serialize(Dump(args[i], Kinds[i])) == before[i], "Read-only input was modified.");
        };
    }
    static string FilesSnapshot(string root)
    {
        var entries = Directory.EnumerateFileSystemEntries(root, "*", SearchOption.AllDirectories).Order(StringComparer.Ordinal).Select(p => Directory.Exists(p) ? "D:" + Path.GetRelativePath(root, p) : "F:" + Path.GetRelativePath(root, p) + ":" + File.GetLastWriteTimeUtc(p).Ticks + ":" + Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(p)))); return string.Join("\n", entries);
    }
    static object? State(JsonElement raw)
    {
        object obj = Fresh(); var ops = raw[0].EnumerateArray().Select(v => v.GetString()!).ToArray(); var values = raw[1].EnumerateArray().ToArray(); var output = new List<object?>(); int count = 0;
        for (int i = 0; i < ops.Length; i++)
        {
            var method = ops[i]; var args = values[i].EnumerateArray().Select(v => (object?)(v.ValueKind == JsonValueKind.String ? v.GetString() : v.GetInt32())).ToArray();
            bool empty = count == 0 && (Mode == "queue" && method == "Dequeue" || Mode == "stack" && (method is "Pop" or "GetMax"));
            try { var result = Call(obj, method, args); Check(!empty, "Empty-state operation must signal an error."); output.Add(result); }
            catch (Exception ex) when (empty && ex is not ContractError && ex is not NeedChoice) { output.Add(new { error = "empty" }); }
            if (method is "Enqueue" or "Push") count++; else if ((method is "Dequeue" or "Pop") && !empty) count--;
        }
        return output;
    }
    static object RandomCheck(JsonElement raw)
    {
        bool shuffle = Mode == "shuffle"; int maximum = Mode == "rand5" ? 7 : 5; int outcomes = Mode == "rand5" ? 5 : 7;
        int[] original = shuffle ? raw[0].Deserialize<int[]>()! : [];
        var probabilities = new Dictionary<string, double>(StringComparer.Ordinal); double unresolved = 0; int branches = 0;
        var pending = new Stack<(int[] prefix, double weight)>(); pending.Push(([], 1));
        while (pending.TryPop(out var item))
        {
            Check(++branches <= 100000, "Randomized algorithm used too many decision branches."); int position = 0, draws = 0;
            RandomSource.Draw = (lower, upper) => { Check(++draws <= 128, "Randomized algorithm exceeded the draw budget."); Check(lower <= upper && (shuffle ? lower >= 0 && upper < Math.Max(1, original.Length) : lower == 1 && upper == maximum), "Unexpected random-source bounds."); if (position >= item.prefix.Length) throw new NeedChoice(lower, upper); int result = item.prefix[position++]; Check(result >= lower && result <= upper, "Invalid injected choice."); return result; };
            var array = (int[])original.Clone(); try
            {
                var result = shuffle ? Call(Fresh(), Method, array) : Call(Fresh(), Method);
                if (shuffle) { Check(array.Length == original.Length && array.Order().SequenceEqual(original.Order()), "Shuffle changed element multiplicities."); result = string.Join(",", array); } else { Check(draws > 0 && (Mode != "rand7" || draws % 2 == 0), "Use the supplied random source with two Rand5 draws per attempt."); Check(result is int n && n >= 1 && n <= outcomes, "Die result is outside its range."); }
                var key = Convert.ToString(result, System.Globalization.CultureInfo.InvariantCulture)!; probabilities[key] = probabilities.GetValueOrDefault(key) + item.weight;
            }
            catch (NeedChoice next)
            {
                int limit = shuffle ? Math.Max(8, original.Length * 2) : 8;
                if (item.prefix.Length >= limit) { unresolved += item.weight; continue; }
                for (int choice = next.Lower; choice <= next.Upper; choice++) pending.Push((item.prefix.Append(choice).ToArray(), item.weight / (next.Upper - next.Lower + 1)));
            }
        }
        if (shuffle)
        {
            if (original.Distinct().Count() == original.Length && original.Length <= 5) { int factorial = 1; for (int i = 2; i <= original.Length; i++) factorial *= i; Check(unresolved < 1e-10 && probabilities.Count == factorial && probabilities.Values.All(p => Math.Abs(p - 1.0 / factorial) < 1e-9), "Shuffle is biased over full permutations."); }
        }
        else
        {
            Check(unresolved < 0.02, "Rejection probability exceeds the bounded judge exploration.");
            for (int i = 1; i <= outcomes; i++) { double p = probabilities.GetValueOrDefault(i.ToString()); Check(p <= 1.0 / outcomes + 1e-9 && p + unresolved >= 1.0 / outcomes - 1e-9, "Die transformation is biased over injected choices."); }
        }
        // A separate deterministic stream catches stale instance state and ignores no random output.
        int[] forced = shuffle ? [] : raw[0].Deserialize<int[]>()!; uint seed = 0x85ebca6bu; var counts = new int[outcomes + 1]; var pairs = new int[outcomes * outcomes]; var triples = new int[outcomes * outcomes * outcomes]; int previous = -1, previousTwo = -1; int samples = 4096; var seededInstance = Fresh(); var seededPermutations = new Dictionary<string, int>(StringComparer.Ordinal);
        for (int trial = 0; trial < samples; trial++)
        {
            int draws = 0; RandomSource.Draw = (lower, upper) => { Check(++draws <= 128, "Too many random draws."); Check(lower <= upper && (shuffle ? lower >= 0 && upper < Math.Max(1, original.Length) : lower == 1 && upper == maximum), "Unexpected random bounds."); seed = unchecked(seed * 1664525u + 1013904223u); if (trial == 0 && draws <= forced.Length) { Check(forced[draws - 1] >= lower && forced[draws - 1] <= upper, "Forced source value outside bounds."); return forced[draws - 1]; } return lower + (int)((ulong)seed * (uint)(upper - lower + 1) >> 32); };
            var a = (int[])original.Clone(); var result = shuffle ? Call(seededInstance, Method, a) : Call(seededInstance, Method);
            if (shuffle) { Check(a.Order().SequenceEqual(original.Order()), "Shuffle changed elements."); if (a.Length > 1) Check(draws > 0, "Use the supplied random source."); var key = string.Join(",", a); seededPermutations[key] = seededPermutations.GetValueOrDefault(key) + 1; }
            else { Check(draws > 0 && (Mode != "rand7" || draws % 2 == 0) && result is int n && n >= 1 && n <= outcomes, "Invalid die result/source usage."); int current = (int)result! - 1; counts[current + 1]++; if (previous >= 0) pairs[previous * outcomes + current]++; if (previousTwo >= 0) triples[(previousTwo * outcomes + previous) * outcomes + current]++; previousTwo = previous; previous = current; }
        }
        if (!shuffle) { double expected = (double)samples / outcomes; Check(counts.Skip(1).Sum(c => (c - expected) * (c - expected) / expected) < 40, "Seeded die distribution is biased."); }
        if (shuffle && original.Length <= 5 && original.Distinct().Count() == original.Length) { int factorial = 1; for (int i = 2; i <= original.Length; i++) factorial *= i; double expected = (double)samples / factorial; Check(seededPermutations.Count == factorial && seededPermutations.Values.Sum(c => (c - expected) * (c - expected) / expected) <= 4 * (factorial - 1) + 80, "Repeated shuffles are biased or cached."); }
        if (!shuffle) { double pairExpected = (double)(samples - 1) / pairs.Length; double tripleExpected = (double)(samples - 2) / triples.Length; Check(pairs.Sum(c => (c - pairExpected) * (c - pairExpected) / pairExpected) < 4 * (pairs.Length - 1) + 80, "Successive die pairs are correlated."); Check(triples.Sum(c => (c - tripleExpected) * (c - tripleExpected) / tripleExpected) < 4 * (triples.Length - 1) + 80, "Successive die triples are correlated."); }
        return true;
    }
    static object? Execute(JsonElement raw)
    {
        if (Mode is "queue" or "stack" or "trie" or "temperature") return State(raw);
        if (Mode == "wordcloud") { var instance = Activator.CreateInstance(Assembly.GetExecutingAssembly().GetType(ClassName)!, raw[0].GetString())!; return instance.GetType().GetProperty("WordsToCounts")!.GetValue(instance); }
        if (Mode is "shuffle" or "rand5" or "rand7") return RandomCheck(raw);
        if (Mode == "cycle")
        {
            var head = (LinkedListNode?)Load(raw[0], "list"); var nodes = ListNodes(head); int index = raw[1].GetInt32(); if (index >= 0) nodes[^1].Next = nodes[index]; var before = nodes.Select(n => (n.Value, n.Next)).ToArray(); var cycleActual = Call(Fresh(), Method, head);
            Check(nodes.Select((n, i) => (n.Value, n.Next) == before[i]).All(v => v), "Cycle detection modified the list."); return cycleActual;
        }
        if (Mode == "delete")
        {
            var head = (LinkedListNode?)Load(raw[0], "list"); var nodes = ListNodes(head); var before = nodes.Select(n => (n.Value, n.Next)).ToArray(); int index = raw[1].GetInt32(); var target = nodes[index]; Call(Fresh(), Method, target);
            for (int i = 0; i < nodes.Count; i++) Check((nodes[i].Value, nodes[i].Next) == (i == index ? before[index + 1] : before[i]), "Deletion violated target/successor alias semantics."); return Dump(head, "list");
        }
        if (Mode == "reverse_list")
        {
            var head = (LinkedListNode?)Load(raw[0], "list"); var nodes = ListNodes(head); var values = nodes.Select(n => n.Value).ToArray(); var result = (LinkedListNode?)Call(Fresh(), Method, head); var after = ListNodes(result);
            Check(after.SequenceEqual(nodes.AsEnumerable().Reverse()) && nodes.Select((n, i) => n.Value == values[i]).All(v => v), "Reversal must reuse the original nodes in reverse order."); return Dump(result, "list");
        }
        var args = Kinds.Select((kind, i) => Load(raw[i], kind)).ToArray();
        if (Mode is "chars" or "words") { var a = (char[])args[0]!; Call(Fresh(), Method, args); Check(a.Length == raw[0].GetString()!.Length, "Array length changed."); return new string(a); }
        if (Mode == "color")
        {
            var nodes = (GraphNode[])args[0]!; var originals = nodes.ToArray(); var sets = nodes.Select(n => n.Neighbors).ToArray(); var edges = nodes.Select(n => n.Neighbors.ToHashSet()).ToArray(); var labels = nodes.Select(n => n.Label).ToArray(); var colors = (string[])args[1]!; var palette = colors.ToArray(); Call(Fresh(), Method, args);
            for (int i = 0; i < nodes.Length; i++) Check(ReferenceEquals(nodes[i], originals[i]) && ReferenceEquals(nodes[i].Neighbors, sets[i]) && nodes[i].Label == labels[i] && nodes[i].Neighbors.SetEquals(edges[i]) && nodes[i].Color is not null && palette.Contains(nodes[i].Color) && nodes[i].Neighbors.All(n => n.Color != nodes[i].Color), "Invalid coloring or graph mutation."); Check(colors.SequenceEqual(palette), "Palette was modified."); return true;
        }
        var preserve = Preserve(args);
        string? filesBefore = Mode == "files" ? FilesSnapshot((string)args[0]!) : null;
        object? actual;
        try { actual = Call(Fresh(), Method, args); }
        catch (InfinityException) { preserve(); return new { error = "infinite" }; }
        preserve();
        if (Mode == "files") { Check(FilesSnapshot((string)args[0]!) == filesBefore, "Filesystem must remain unchanged."); return Dump(actual, "pairs"); }
        if (Mode == "kth") { var nodes = ListNodes((LinkedListNode?)args[1]); int index = nodes.FindIndex(n => ReferenceEquals(n, actual)); Check(index >= 0, "Return an original node reference."); return index; }
        if (Mode == "meetings") { var result = (IEnumerable<Meeting>)actual!; var originals = (List<Meeting>)args[0]!; Check(!ReferenceEquals(actual, args[0]) && result.All(n => !originals.Contains(n)), "Return new interval objects."); }
        if (Mode == "rect") Check(actual is Rectangle && !args.Any(v => ReferenceEquals(v, actual)), "Return a new rectangle.");
        if (Result == "ai") Check(actual is int[] && !args.Any(v => ReferenceEquals(v, actual)), "Return a newly allocated result array.");
        return Dump(actual, Result);
    }
    public static void Main()
    {
        var rows = JsonDocument.Parse(File.ReadAllText("cases.json")).RootElement; var output = new List<object>();
        foreach (var raw in rows.EnumerateArray()) { var clock = Stopwatch.StartNew(); object? actual = null; string? error = null; bool validation = false; try { actual = Execute(raw); _ = Serialize(actual); } catch (ContractError ex) { validation = true; error = ex.Message; } catch (Exception ex) { error = ex.GetType().Name + ": " + ex.Message; } output.Add(new { Actual = actual, Error = error, ElapsedMs = clock.Elapsed.TotalMilliseconds, ValidationFailed = validation }); }
        File.WriteAllText("results.json", Serialize(output));
    }
}
