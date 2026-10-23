using System.Text.Json;

namespace EpiJudge.Runner;

// Value, identity and mutation checks are separate from catalog shape checks.
// The observation protocol contains no expected answer in the submitted process.
public static class CtciStagingGrader
{
    private static bool Equal(JsonElement first, JsonElement second) => JsonElement.DeepEquals(first, second);
    private static JsonElement Encode<T>(T value) => JsonSerializer.SerializeToElement(value);
    private static int[] Integers(JsonElement value) => value.EnumerateArray().Select(v =>
        v.ValueKind == JsonValueKind.Number && v.TryGetInt32(out int number) ? number : throw new ArgumentException("Return signed 32-bit integer members.")).ToArray();

    private static string[] Strings(JsonElement value) => value.EnumerateArray().Select(v =>
        v.ValueKind == JsonValueKind.String && v.GetString() is string word ? word : throw new ArgumentException("Return nonnull strings.")).ToArray();

    private static string? MinimalTreeFailure(TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve sortedValues and return a finite tree of provided TreeNode objects.";
        var actual = observed.GetProperty("actual");
        int root = actual.GetProperty("root").GetInt32();
        var rows = actual.GetProperty("nodes").EnumerateArray().Select(Integers).ToArray();
        var values = Integers(test.Arguments[0]);
        int count = values.Length;
        if (count == 0) return root == -1 && rows.Length == 0 ? null : "Empty input requires a null root.";
        if (rows.Length != count || root < 0 || root >= count || rows.Any(row => row.Length != 4 || row.Skip(1).Any(index => index < -1 || index >= count))) return "Return exactly one correctly linked node per input value.";
        var parents = Enumerable.Repeat(-1, count).ToArray();
        for (int i = 0; i < count; i++)
            foreach (int child in rows[i].Skip(1).Take(2))
                if (child != -1)
                {
                    if (parents[child] != -1) return "A child cannot be shared by two links.";
                    parents[child] = i;
                }
        if (parents[root] != -1 || Enumerable.Range(0, count).Any(i => rows[i][3] != parents[i] || i != root && parents[i] == -1)) return "Root.Parent must be null and every child.Parent must identify its actual parent.";
        var seen = new HashSet<int>();
        var queue = new List<(int Node, int Height)> { (root, 1) };
        int height = 0;
        for (int head = 0; head < queue.Count; head++)
        {
            var frame = queue[head];
            if (!seen.Add(frame.Node)) return "Return a proper tree without cycles or shared children.";
            height = Math.Max(height, frame.Height);
            foreach (int child in rows[frame.Node].Skip(1).Take(2)) if (child != -1) queue.Add((child, frame.Height + 1));
        }
        if (seen.Count != count) return "Every returned node must belong to the root's tree.";
        var ordered = new List<int>();
        var stack = new Stack<int>();
        int node = root;
        while (node != -1 || stack.Count > 0)
        {
            while (node != -1) { stack.Push(node); node = rows[node][1]; }
            node = stack.Pop(); ordered.Add(rows[node][0]); node = rows[node][2];
        }
        if (!ordered.SequenceEqual(values)) return "Inorder traversal must equal sortedValues exactly.";
        int minimum = 0, capacity = 0;
        while (capacity < count) { minimum++; capacity = 2 * capacity + 1; }
        return height == minimum ? null : "The returned BST must have the smallest possible height.";
    }

    private static string? MissingFileFailure(TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Use the provided readonly integer stream and return a nonnegative int.";
        var actual = observed.GetProperty("actual");
        if (actual.ValueKind != JsonValueKind.Number || !actual.TryGetInt32(out int value) || value < 0) return "Return an absent integer in 0..2147483647.";
        long length = 0;
        foreach (var pair in test.Arguments[0].EnumerateArray())
        {
            int start = pair[0].GetInt32(), end = pair[1].GetInt32();
            length += (long)end - start + 1;
            if (start <= value && value <= end) return "The returned integer is present in the file.";
        }
        bool small = test.Arguments[1].GetBoolean();
        if (!observed.GetProperty("reads").TryGetInt64(out long reads) || reads < 0 || reads > (small ? 2L : 1L) * (length + 1) || !observed.GetProperty("resets").TryGetInt32(out int resets) || resets < 0 || resets > (small ? 1 : 0)) return "Respect the stated stream pass/read/rewind limits.";
        return null;
    }

    private static string? GeometryFailure(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        const double tolerance = 0.000001;
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve all input arrays, rows and coordinates.";
        var value = observed.GetProperty("actual");
        if (value.ValueKind != JsonValueKind.Array) return "Return a numeric coordinate array.";
        var actual = new List<double>();
        foreach (var item in value.EnumerateArray())
        {
            if (item.ValueKind != JsonValueKind.Number || !item.TryGetDouble(out double coordinate) || !double.IsFinite(coordinate)) return "Return finite numeric coordinates.";
            actual.Add(coordinate);
        }
        bool Near(IEnumerable<double> expected) => actual.Zip(expected).All(pair => Math.Abs(pair.First - pair.Second) <= tolerance);
        var rows = test.Arguments[0].EnumerateArray().Select(Integers).ToArray();
        if (definition.Ref == "16.3")
        {
            if (test.Expected.GetArrayLength() == 0) return actual.Count == 0 ? null : "The closed segments are disjoint.";
            if (actual.Count != 2) return "Return exactly two coordinates of a common point.";
            var a = rows[0]; var b = rows[1]; var c = rows[2]; var d = rows[3];
            int denominator = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0]);
            if (a.SequenceEqual(b) || c.SequenceEqual(d) || denominator != 0) return Near(test.Expected.EnumerateArray().Select(v => v.GetDouble())) ? null : "Return the unique closed-segment intersection within the coordinate tolerance.";
            int axis = Math.Abs(b[0] - a[0]) >= Math.Abs(b[1] - a[1]) ? 0 : 1;
            double low = Math.Max(Math.Min(a[axis], b[axis]), Math.Min(c[axis], d[axis]));
            double high = Math.Min(Math.Max(a[axis], b[axis]), Math.Max(c[axis], d[axis]));
            double projected = Math.Clamp(actual[axis], low, high);
            double parameter = (projected - a[axis]) / (b[axis] - a[axis]);
            return Near(Enumerable.Range(0, 2).Select(i => a[i] + parameter * (b[i] - a[i]))) ? null : "Return a point in the actual collinear overlap.";
        }
        if (actual.Count != 4) return "Return both outer endpoints as four numeric coordinates.";
        double x = rows[0][0] + rows[0][2] / 2.0, y = rows[0][1] + rows[0][2] / 2.0;
        double otherX = rows[1][0] + rows[1][2] / 2.0, otherY = rows[1][1] + rows[1][2] / 2.0;
        if (x != otherX || y != otherY)
        {
            var expected = test.Expected.EnumerateArray().Select(v => v.GetDouble()).ToArray();
            return Near(expected) || Near(expected.Skip(2).Concat(expected.Take(2))) ? null : "Return the full outer boundary span through both square centers.";
        }
        double dx = actual[2] - actual[0], dy = actual[3] - actual[1], scale = Math.Max(Math.Abs(dx), Math.Abs(dy));
        if (scale <= 2 * tolerance) return "The returned endpoints must be distinct.";
        double radius = Math.Max(rows[0][2], rows[1][2]) / 2.0;
        return Near(new[] { x - radius * dx / scale, y - radius * dy / scale, x + radius * dx / scale, y + radius * dy / scale }) ? null : "For concentric squares, return the full outer boundary span of any line through the common center.";
    }

    private static string? NumericFailure(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve input values and return finite numeric results.";
        var actual = observed.GetProperty("actual");
        if (definition.Ref == "16.26")
        {
            if (actual.ValueKind != JsonValueKind.Number || !actual.TryGetDouble(out double value) || !double.IsFinite(value)) return "Return a finite numeric expression value.";
            double expected = test.Expected.GetDouble();
            return Math.Abs(value - expected) <= Math.Max(0.000001, 0.000000001 * Math.Abs(expected)) ? null : "Respect precedence, left associativity and real division within the stated tolerance.";
        }
        if (actual.ValueKind != JsonValueKind.Array || actual.GetArrayLength() != test.Expected.GetArrayLength()) return "Return one median per inserted stream value.";
        for (int i = 0; i < actual.GetArrayLength(); i++)
            if (actual[i].ValueKind != JsonValueKind.Number || !actual[i].TryGetDouble(out double median) || !double.IsFinite(median) || median != test.Expected[i].GetDouble()) return "Return the actual median of every prefix, including exact half-integer means.";
        return null;
    }

    private static string? GroupOrLineFailure(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve all input arrays, row identities and values.";
        var actual = observed.GetProperty("actual");
        if (definition.Ref == "16.14")
        {
            var points = test.Arguments[0].EnumerateArray().Select(Integers).ToArray();
            var line = Integers(actual);
            if (points.Length == 0) return line.Length == 0 ? null : "Empty input requires an empty result.";
            if (line.Length != 3 || line[0] == 0 && line[1] == 0) return "Return a nondegenerate integer line [A,B,C].";
            int Score(int[] coefficients) => points.Count(point => (long)coefficients[0] * point[0] + (long)coefficients[1] * point[1] + coefficients[2] == 0);
            return Score(line) == Score(Integers(test.Expected)) ? null : "The line must contain the maximum number of input occurrences, including duplicates.";
        }
        var frequencies = Integers(test.Arguments[1]);
        var parent = Enumerable.Range(0, frequencies.Length).ToArray();
        int Find(int node) { while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; } return node; }
        foreach (var edge in test.Arguments[2].EnumerateArray()) parent[Find(edge[0].GetInt32())] = Find(edge[1].GetInt32());
        var totals = new Dictionary<int, int>();
        for (int i = 0; i < frequencies.Length; i++) { int root = Find(i); totals[root] = totals.GetValueOrDefault(root) + frequencies[i]; }
        var seen = new HashSet<int>();
        foreach (var rowValue in actual.EnumerateArray())
        {
            var row = Integers(rowValue);
            if (row.Length != 2 || row[0] < 0 || row[0] >= frequencies.Length) return "Return [originalNameIndex,totalFrequency] rows.";
            int root = Find(row[0]);
            if (!seen.Add(root) || row[1] != totals[root]) return "Represent each synonym component once with its exact frequency total.";
        }
        return seen.Count == totals.Count ? null : "Include isolated names and zero-frequency components.";
    }

    private static string? StructuredHardFailure(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the required input arrays, original rows and values, and return the selected signature's concrete collection type.";
        var actual = observed.GetProperty("actual");
        if (definition.Ref == "17.26") return Equal(actual, test.Expected) ? null : "Return every positive pair in ID order with its actual intersection and union counts.";
        if (definition.Ref == "17.8")
        {
            var order = Integers(actual);
            var people = test.Arguments[0];
            if (order.Length != test.Expected.GetArrayLength() || order.Distinct().Count() != order.Length || order.Any(index => index < 0 || index >= people.GetArrayLength())) return "Return original person indices forming a maximum-length tower.";
            for (int i = 1; i < order.Length; i++)
                if (people[order[i - 1]][0].GetInt32() >= people[order[i]][0].GetInt32() || people[order[i - 1]][1].GetInt32() >= people[order[i]][1].GetInt32()) return "Height and weight must both increase strictly from top to bottom.";
            return null;
        }
        var result = Strings(actual);
        if (definition.Ref == "17.13")
        {
            string text = test.Arguments[0].GetString()!;
            var words = Strings(test.Arguments[1]).ToHashSet(StringComparer.Ordinal);
            if (result.Any(word => word.Length == 0) || string.Concat(result) != text) return "Return nonempty tokens that concatenate to the complete original text.";
            int cost = result.Where(word => !words.Contains(word)).Sum(word => word.Length);
            int optimum = Strings(test.Expected).Where(word => !words.Contains(word)).Sum(word => word.Length);
            return cost == optimum ? null : "Minimize the number of characters in unrecognized tokens.";
        }
        if (definition.Ref == "17.22")
        {
            if (result.Length == 0) return test.Expected.GetArrayLength() == 0 ? null : "A dictionary transformation path exists.";
            string start = test.Arguments[0].GetString()!, stop = test.Arguments[1].GetString()!;
            var words = Strings(test.Arguments[2]).ToHashSet(StringComparer.Ordinal);
            if (result[0] != start || result[^1] != stop || result.Distinct(StringComparer.Ordinal).Count() != result.Length || result.Any(word => !words.Contains(word))) return "Return both endpoints and a path of dictionary words without repeated vertices.";
            for (int i = 1; i < result.Length; i++)
            {
                if (result[i - 1].Length != result[i].Length) return "Each step changes one letter without insertion or deletion.";
                int changes = 0;
                for (int j = 0; j < result[i].Length; j++) if (result[i - 1][j] != result[i][j]) changes++;
                if (changes != 1) return "Each adjacent pair must differ at exactly one position.";
            }
            return null;
        }
        if (result.Length == 0) return test.Expected.GetArrayLength() == 0 ? null : "A nonempty word rectangle exists.";
        var vocabulary = Strings(test.Arguments[0]).ToHashSet(StringComparer.Ordinal);
        int maximum = vocabulary.Count == 0 ? 0 : vocabulary.Max(word => word.Length);
        int height = result.Length, width = result[0].Length;
        if (height > maximum || width == 0 || width > maximum || result.Any(row => row.Length != width || !vocabulary.Contains(row))) return "Return equal-length dictionary rows with positive valid dimensions.";
        for (int column = 0; column < width; column++)
        {
            var word = new System.Text.StringBuilder();
            foreach (string row in result) word.Append(row[column]);
            if (!vocabulary.Contains(word.ToString())) return "Every top-to-bottom column must also be a dictionary word.";
        }
        int expectedHeight = test.Expected.GetArrayLength();
        int area = expectedHeight == 0 ? 0 : expectedHeight * test.Expected[0].GetString()!.Length;
        return height * width == area ? null : "Return a maximum-area rectangle; every equal-area valid arrangement is accepted.";
    }

    private static string? SortingFailure(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the required input objects and readonly values, and perform the stated in-place changes.";
        var actual = observed.GetProperty("actual");
        if (definition.Ref == "10.4")
        {
            int probes = observed.GetProperty("probes").GetInt32();
            int size = test.Arguments[0].GetArrayLength(), power = 1, steps = 0;
            while (power < size + 2) { power <<= 1; steps++; }
            if (probes < 0 || probes > 4 * steps + 8) return "Use logarithmically many Listy.ElementAt queries.";
        }
        if (definition.Ref is "10.3" or "10.4" or "10.5")
        {
            if (actual.ValueKind != JsonValueKind.Number || !actual.TryGetInt32(out int index)) return "Return an integer index or -1.";
            if (definition.Ref == "10.5" && test.Arguments[1].GetString() == "") return index == -1 ? null : "Empty strings are gaps, not searchable targets.";
            if (index == -1) return test.Expected.GetInt32() == -1 ? null : "The target is present.";
            return index >= 0 && index < test.Arguments[0].GetArrayLength() && Equal(test.Arguments[0][index], test.Arguments[1]) ? null : "Return an original-array index containing target.";
        }
        if (definition.Ref == "10.2")
        {
            var words = Strings(actual);
            var originals = Strings(test.Arguments[0]);
            var remaining = originals.GroupBy(word => word, StringComparer.Ordinal).ToDictionary(group => group.Key, group => group.Count(), StringComparer.Ordinal);
            if (words.Length != originals.Length) return "Preserve every word occurrence.";
            var groups = new HashSet<string>(StringComparer.Ordinal);
            string? previous = null;
            foreach (string word in words)
            {
                if (!remaining.TryGetValue(word, out int count) || count == 0) return "Preserve the original word multiset, including duplicates.";
                remaining[word] = count - 1;
                string key = new(word.Order().ToArray());
                if (key != previous && !groups.Add(key)) return "Each complete anagram group must be contiguous.";
                previous = key;
            }
            return null;
        }
        if (definition.Ref == "10.9")
        {
            var coordinate = Integers(actual);
            if (coordinate.Length != 2) return "Return [row,column] or [-1,-1].";
            if (coordinate[0] == -1 && coordinate[1] == -1) return Equal(actual, test.Expected) ? null : "The target is present.";
            var matrix = test.Arguments[0];
            int row = coordinate[0], column = coordinate[1];
            return row >= 0 && row < matrix.GetArrayLength() && column >= 0 && column < matrix[row].GetArrayLength() && Equal(matrix[row][column], test.Arguments[1]) ? null : "Return a coordinate containing target.";
        }
        if (definition.Ref == "10.11")
        {
            var values = Integers(actual);
            if (!values.Order().SequenceEqual(Integers(test.Arguments[0]).Order())) return "Preserve every original integer occurrence.";
            for (int i = 1; i < values.Length; i += 2)
                if (values[i] < values[i - 1] || i + 1 < values.Length && values[i] < values[i + 1]) return "Every odd position must be a peak, allowing equality.";
            return null;
        }
        return Equal(actual, test.Expected) ? null : "The filled array does not match the stated merge.";
    }

    private static int?[][] InputGraph(CtciStagingDefinition definition, TestCase test)
    {
        var count = definition.Ref == "2.7" ? 3 : definition.Ref == "2.5" ? 2 : 1;
        var nodes = new List<int?[]>();
        var ends = new List<int?>();
        foreach (var segment in test.Arguments.Take(count))
        {
            var values = Integers(segment);
            int offset = nodes.Count;
            for (int i = 0; i < values.Length; i++)
                nodes.Add([values[i], i + 1 < values.Length ? offset + i + 1 : null]);
            ends.Add(values.Length == 0 ? null : nodes.Count - 1);
        }
        if (definition.Ref == "2.7")
        {
            int? common = test.Arguments[2].GetArrayLength() == 0 ? null : test.Arguments[0].GetArrayLength() + test.Arguments[1].GetArrayLength();
            foreach (var end in ends.Take(2)) if (end is int index) nodes[index][1] = common;
        }
        else if (definition.Ref == "2.8" && nodes.Count > 0 && test.Arguments[1].GetInt32() >= 0)
            nodes[^1][1] = test.Arguments[1].GetInt32();
        return nodes.ToArray();
    }

    private static string[] CanonicalCollection(string result, JsonElement values)
    {
        if (values.ValueKind != JsonValueKind.Array) throw new ArgumentException("Return a collection.");
        var canonical = new List<string>();
        foreach (var value in values.EnumerateArray())
        {
            if (result == "strings")
            {
                if (value.ValueKind != JsonValueKind.String) throw new ArgumentException("Return strings.");
                canonical.Add(value.GetString()!);
            }
            else
            {
                var members = Integers(value);
                if (result == "arrangements")
                {
                    if (members.Length != 8 || members.Any(v => v < 0 || v > 7)) throw new ArgumentException("Return eight board columns.");
                    canonical.Add(JsonSerializer.Serialize(members));
                }
                else
                {
                    if (members.Distinct().Count() != members.Length) throw new ArgumentException("A subset cannot repeat a member.");
                    canonical.Add(JsonSerializer.Serialize(members.Order().ToArray()));
                }
            }
        }
        return canonical.Order(StringComparer.Ordinal).ToArray();
    }

    private static string? RandomTreeFailure(TestCase test, JsonElement observed)
    {
        if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True || observed.GetProperty("uniformOk").ValueKind != JsonValueKind.True) return "Preserve node identity and readonly queries; select every current physical node uniformly.";
        var operations = Strings(test.Arguments[0]);
        var arguments = test.Arguments[1];
        var actual = observed.GetProperty("actual");
        var results = actual.GetProperty("results");
        var changes = observed.GetProperty("changes");
        if (results.GetArrayLength() != operations.Length || changes.GetArrayLength() != operations.Length) return "Return one observation for each operation.";
        var counts = new SortedDictionary<int, int>();
        int total = 0;
        for (int i = 0; i < operations.Length; ++i)
        {
            var result = results[i];
            int[] added = [], removed = [];
            int value = arguments[i].GetArrayLength() == 0 ? 0 : arguments[i][0].GetInt32();
            switch (operations[i])
            {
                case "RandomBst":
                    if (result.ValueKind != JsonValueKind.Null) return "Construct an empty independent tree.";
                    break;
                case "Insert":
                    if (result.ValueKind != JsonValueKind.Null) return "Insert returns void.";
                    counts[value] = counts.GetValueOrDefault(value) + 1; total++; added = [value];
                    break;
                case "Delete":
                    bool present = counts.GetValueOrDefault(value) > 0;
                    if (result.ValueKind is not (JsonValueKind.True or JsonValueKind.False) || result.GetBoolean() != present) return "Delete one matching occurrence and report whether it existed.";
                    if (present) { if (--counts[value] == 0) counts.Remove(value); total--; removed = [value]; }
                    break;
                case "Find":
                    int[] wanted = counts.GetValueOrDefault(value) > 0 ? [value] : [];
                    if (!Integers(result).SequenceEqual(wanted)) return "Find returns a current matching node or null when absent.";
                    break;
                case "GetRandomNode":
                    var projection = Integers(result);
                    if (total == 0 ? projection.Length != 0 : projection.Length != 1 || counts.GetValueOrDefault(projection[0]) == 0) return "Return a current node, or null only for an empty tree.";
                    break;
                default: return "Unknown tree operation.";
            }
            var change = changes[i];
            if (!Integers(change.GetProperty("added")).SequenceEqual(added) || !Integers(change.GetProperty("removed")).SequenceEqual(removed) || change.GetProperty("count").GetInt32() != total) return "Each mutation must make exactly its requested multiset change; queries preserve the tree.";
        }
        var finalValues = counts.SelectMany(pair => Enumerable.Repeat(pair.Key, pair.Value));
        return Integers(actual.GetProperty("finalValues")).SequenceEqual(finalValues) ? null : "Preserve all remaining occurrences in BST order.";
    }

    public static string? FailureReason(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        try
        {
            if (observed.ValueKind != JsonValueKind.Object || observed.TryGetProperty("error", out var error) && error.ValueKind != JsonValueKind.Null)
                return "Your code did not finish this case successfully.";
            if (definition.Ref == "4.11") return RandomTreeFailure(test, observed);
            if (definition.Ref is "17.2" or "17.3")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True || observed.GetProperty("uniformOk").ValueKind != JsonValueKind.True) return "Respect mutation contracts and use the supplied primitive to produce the required uniform distribution.";
                var actual = Integers(observed.GetProperty("actual"));
                var inputValues = Integers(test.Arguments[0]);
                int required = definition.Ref == "17.2" ? inputValues.Length : test.Arguments[1].GetInt32();
                var counts = inputValues.GroupBy(value => value).ToDictionary(group => group.Key, group => group.Count());
                if (actual.Length != required) return "Return the required number of original element occurrences.";
                foreach (int value in actual)
                {
                    if (counts.GetValueOrDefault(value) <= 0) return "Preserve original occurrence multiplicities; repeated values are not discarded.";
                    counts[value]--;
                }
                return null;
            }
            if (definition.Ref == "16.23")
            {
                var actual = observed.GetProperty("actual");
                return observed.GetProperty("mutationOk").ValueKind == JsonValueKind.True && observed.GetProperty("uniformOk").ValueKind == JsonValueKind.True && actual.ValueKind == JsonValueKind.Number && actual.TryGetInt32(out int outcome) && outcome >= 0 && outcome <= 6 ? null : "Use the uniform primitive to produce independent uniform integers in 0..6; a fixed source-prefix mapping is not required.";
            }
            if (definition.Ref == "10.7") return MissingFileFailure(test, observed);
            if (definition.Ref == "17.4")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True || !observed.GetProperty("probes").TryGetInt32(out int probes) || probes < 0 || probes > 4 * test.Arguments[0].GetArrayLength() + 32) return "Use the provided bit-only API within the linear query budget.";
                var actual = observed.GetProperty("actual");
                return actual.ValueKind == JsonValueKind.Number && actual.TryGetInt32(out int result) && result == test.Expected.GetInt32() ? null : "Return the omitted value from the hidden consecutive range.";
            }
            if (definition.Ref is "16.3" or "16.13") return GeometryFailure(definition, test, observed);
            if (definition.Ref is "16.26" or "17.20") return NumericFailure(definition, test, observed);
            if (definition.Ref is "16.14" or "17.7") return GroupOrLineFailure(definition, test, observed);
            if (definition.Batch == 10) return SortingFailure(definition, test, observed);
            if (definition.Batch == 17 && definition.Ref is ("17.8" or "17.13" or "17.22" or "17.25" or "17.26")) return StructuredHardFailure(definition, test, observed);
            if (definition.Batch == 4 && definition.Ref == "4.2") return MinimalTreeFailure(test, observed);
            if (definition.Batch == 4 && definition.Ref == "4.3")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the input tree and return proper, distinct, null-terminated DepthLink lists.";
                return Equal(observed.GetProperty("actual"), test.Expected) ? null : "Each depth list must contain the original TreeNode objects in left-to-right order.";
            }
            if (definition.Batch == 4 && definition.Ref == "4.9")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the tree and return concrete integer sequences.";
                var actualRows = observed.GetProperty("actual").EnumerateArray().Select(row => JsonSerializer.Serialize(Integers(row))).ToArray();
                var expectedRows = test.Expected.EnumerateArray().Select(row => JsonSerializer.Serialize(Integers(row))).Order(StringComparer.Ordinal);
                if (actualRows.Distinct(StringComparer.Ordinal).Count() != actualRows.Length) return "Return each insertion sequence once.";
                return actualRows.Order(StringComparer.Ordinal).SequenceEqual(expectedRows, StringComparer.Ordinal) ? null : "Return every valid insertion sequence; preserve the value order inside each row.";
            }
            if (definition.Batch == 4 && definition.Result == "tree")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve every original node's Data, Left, Right and Parent fields.";
                var nodeObservation = observed.GetProperty("actual");
                if (nodeObservation.ValueKind != JsonValueKind.Number || !nodeObservation.TryGetInt32(out int identity) || identity < -1) return "Return an original TreeNode object or null; a newly allocated equal-valued node is not the original node.";
                return Equal(nodeObservation, test.Expected) ? null : "Return the required original successor/common-ancestor node, or null when it does not exist.";
            }
            if (definition.Batch == 4 && definition.Ref == "4.7")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the dependency array and its original rows.";
                var order = Integers(observed.GetProperty("actual"));
                if (order.Length == 0) return test.Expected.GetArrayLength() == 0 ? null : "A full build order exists.";
                int count = test.Arguments[0].GetInt32();
                if (order.Length != count || order.Distinct().Count() != count || order.Any(project => project < 0 || project >= count)) return "Include every project exactly once.";
                var positions = new int[count];
                for (int i = 0; i < order.Length; i++) positions[order[i]] = i;
                foreach (var edge in test.Arguments[1].EnumerateArray())
                    if (positions[edge[0].GetInt32()] >= positions[edge[1].GetInt32()]) return "Build each prerequisite before its dependent project.";
                return null;
            }
            if (definition.Batch == 8 && definition.Ref == "8.2")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the grid and its original rows.";
                var path = observed.GetProperty("actual").EnumerateArray().Select(Integers).ToArray();
                if (path.Length == 0) return test.Expected.GetArrayLength() == 0 ? null : "A path exists; return one legal path.";
                var grid = test.Arguments[0];
                int rows = grid.GetArrayLength(), columns = rows == 0 ? 0 : grid[0].GetArrayLength();
                if (path.Any(p => p.Length != 2) || !path[0].SequenceEqual(new[] { 0, 0 }) || !path[^1].SequenceEqual(new[] { rows - 1, columns - 1 }))
                    return "Include the origin and destination in travel order.";
                for (int i = 0; i < path.Length; i++)
                {
                    int r = path[i][0], c = path[i][1];
                    if (r < 0 || r >= rows || c < 0 || c >= columns || grid[r][c].GetInt32() != 1) return "Visit only open cells within the grid.";
                    if (i > 0 && !((r == path[i - 1][0] + 1 && c == path[i - 1][1]) || (r == path[i - 1][0] && c == path[i - 1][1] + 1)))
                        return "Each move must be exactly one cell right or down.";
                }
                return null;
            }
            if (definition.Batch == 8 && definition.Ref == "8.3")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the sorted input array.";
                var value = observed.GetProperty("actual");
                if (value.ValueKind != JsonValueKind.Number || !value.TryGetInt32(out int index)) return "Return an integer index or -1.";
                var magicValues = Integers(test.Arguments[0]);
                return index == -1 ? magicValues.Where((v, i) => v == i).Any() ? "A magic index exists." : null
                    : index >= 0 && index < magicValues.Length && magicValues[index] == index ? null : "Return an index whose value equals that index.";
            }
            if (definition.Batch == 8 && definition.Result is "sets" or "strings" or "arrangements")
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True) return "Preserve the input and return the collection type in the selected signature.";
                return CanonicalCollection(definition.Result, observed.GetProperty("actual")).SequenceEqual(CanonicalCollection(definition.Result, test.Expected), StringComparer.Ordinal)
                    ? null : "Return every required subset or string exactly once. Output order is unrestricted.";
            }
            if (definition.Batch is 1 or 3 or 4 or 5 or 8 or 13 or 16 or 17)
            {
                if (observed.GetProperty("mutationOk").ValueKind != JsonValueKind.True)
                    return definition.Batch == 3 ? "Preserve the required stack and original Animal identities, fields and return types." : "Preserve the required input, row, or buffer identities.";
                return Equal(observed.GetProperty("actual"), test.Expected) ? null : "The returned or mutated result does not match the stated contract.";
            }
            var before = observed.GetProperty("before");
            var after = observed.GetProperty("after");
            var graph = InputGraph(definition, test);
            if (!Equal(before, Encode(graph))) return "The supplied node model or original input topology was changed.";
            if (after.ValueKind != JsonValueKind.Array || after.GetArrayLength() != graph.Length)
                return "Preserve every original node object.";
            var returned = observed.GetProperty("returnedId");
            var boolean = observed.GetProperty("returnedBool");
            var ids = Integers(observed.GetProperty("reachableIds"));
            var values = observed.GetProperty("reachableValues");
            bool cycle = observed.GetProperty("cycle").GetBoolean();
            if (values.ValueKind != JsonValueKind.Array || values.GetArrayLength() != ids.Length)
                return "The output list is incomplete.";
            bool payloadsPreserved = Enumerable.Range(0, graph.Length).All(i =>
                after[i].ValueKind == JsonValueKind.Array && after[i].GetArrayLength() == 2 && after[i][0].GetInt32() == graph[i][0]);
            bool allPreserved = Equal(before, after);
            switch (definition.Ref)
            {
                case "2.1":
                    if (!payloadsPreserved) return "Preserve every original node's Value.";
                    if (cycle) return "The output list must terminate; it contains a cycle.";
                    var seen = new HashSet<int>();
                    var kept = Enumerable.Range(0, graph.Length).Where(i => seen.Add(graph[i][0]!.Value)).ToArray();
                    if (!ids.SequenceEqual(kept)) return "Retain first occurrences as original nodes, in their input order.";
                    return Equal(values, test.Expected) ? null : "The retained value sequence is incorrect.";
                case "2.2":
                    if (!allPreserved) return "Preserve every input node's Value and Next fields.";
                    return Equal(returned, test.Expected) ? null : "The returned node is not the required original kth-to-last node.";
                case "2.3":
                    bool success = test.Expected.GetProperty("success").GetBoolean();
                    if (!Equal(boolean, Encode(success))) return "Return true exactly for a nonnull target with a successor.";
                    var desired = graph.Select(row => row.ToArray()).ToArray();
                    int selected = test.Arguments[1].GetInt32();
                    if (success) desired[selected] = graph[selected + 1].ToArray();
                    if (!Equal(after, Encode(desired))) return "Only target.Value and target.Next may change; successor aliases retain their original fields.";
                    var remaining = Enumerable.Range(0, graph.Length).Where(i => !success || i != selected + 1);
                    if (cycle || !ids.SequenceEqual(remaining)) return "Keep the original target object and bypass its successor.";
                    return Equal(values, test.Expected.GetProperty("values")) ? null : "The reachable value sequence is incorrect.";
                case "2.4":
                    if (!payloadsPreserved) return "Preserve every original node's Value.";
                    if (cycle) return "The partitioned list must terminate; it contains a cycle.";
                    if (!ids.Order().SequenceEqual(Enumerable.Range(0, graph.Length))) return "Return each original node exactly once, without copies.";
                    bool largeSeen = false;
                    int pivot = test.Arguments[1].GetInt32();
                    for (int i = 0; i < ids.Length; i++)
                    {
                        int value = values[i].GetInt32();
                        if (value != graph[ids[i]][0]) return "Preserve every original node's Value.";
                        if (value >= pivot) largeSeen = true;
                        else if (largeSeen) return "A value below pivot appears after a value at or above pivot.";
                    }
                    return null;
                case "2.5":
                    if (!allPreserved) return "Preserve both operand lists, including every Value and Next field.";
                    if (cycle) return "The sum list must terminate; it contains a cycle.";
                    if (ids.Any(id => id < graph.Length)) return "Allocate a new sum list; do not reuse operand nodes.";
                    if (ids.Distinct().Count() != ids.Length) return "The sum list must not repeat a node.";
                    if (!Equal(values, test.Expected)) return "The digit sequence does not encode the required sum in the selected order.";
                    return null;
                case "2.6":
                    if (!allPreserved) return "Preserve every input Value and Next field, including on a false result.";
                    return Equal(boolean, test.Expected) ? null : "Return whether the list's mirrored values match.";
                case "2.7":
                    if (!allPreserved) return "Preserve both lists and their shared suffix.";
                    int? shared = test.Arguments[2].GetArrayLength() > 0 ? test.Arguments[0].GetArrayLength() + test.Arguments[1].GetArrayLength() : null;
                    return Equal(returned, Encode(shared)) ? null : "Return the first shared original node; equal values and copied nodes do not establish intersection.";
                case "2.8":
                    if (!allPreserved) return "Preserve every original Value and Next field, including the cycle link.";
                    return Equal(returned, test.Expected) ? null : "Return the original cycle-entry node, not an arbitrary collision node or a boolean.";
                default:
                    return "Unknown staged grading contract.";
            }
        }
        catch (Exception error) when (error is JsonException or InvalidOperationException or ArgumentException or IndexOutOfRangeException or KeyNotFoundException or OverflowException)
        {
            return "Your code produced an incomplete or invalid result for the callable contract.";
        }
    }

    public static JsonElement Display(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        try
        {
            if (definition.Batch is 1 or 3 or 4 or 5 or 8 or 10 or 13 or 16 or 17) return observed.GetProperty("actual").Clone();
            if (definition.Ref is "2.1" or "2.4" or "2.5") return observed.GetProperty("reachableValues").Clone();
            if (definition.Ref == "2.3") return Encode(new { success = observed.GetProperty("returnedBool"), values = observed.GetProperty("reachableValues") });
            if (definition.Ref == "2.6") return observed.GetProperty("returnedBool").Clone();
            var returned = observed.GetProperty("returnedId");
            if (returned.ValueKind == JsonValueKind.Null) return Encode<object?>(null);
            int id = returned.GetInt32();
            if (definition.Ref == "2.7")
            {
                int first = test.Arguments[0].GetArrayLength(), second = test.Arguments[1].GetArrayLength();
                if (id >= first + second && id < first + second + test.Arguments[2].GetArrayLength()) return Encode(id - second);
                return id >= 0 && id < first ? Encode(id) : Encode("not an original node in the first list");
            }
            return Encode(id);
        }
        catch (Exception error) when (error is InvalidOperationException or KeyNotFoundException or JsonException or FormatException)
        {
            return Encode<object?>(null);
        }
    }
}
