using System.Text.Json;

namespace EpiJudge.Runner;

// Value, identity and mutation checks are separate from catalog shape checks.
// The observation protocol contains no expected answer in the submitted process.
public static class CtciStagingGrader
{
    private static bool Equal(JsonElement first, JsonElement second) => JsonElement.DeepEquals(first, second);
    private static JsonElement Encode<T>(T value) => JsonSerializer.SerializeToElement(value);
    private static int[] Integers(JsonElement value) => value.EnumerateArray().Select(v => v.GetInt32()).ToArray();

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

    public static string? FailureReason(CtciStagingDefinition definition, TestCase test, JsonElement observed)
    {
        try
        {
            if (observed.ValueKind != JsonValueKind.Object || observed.TryGetProperty("error", out var error) && error.ValueKind != JsonValueKind.Null)
                return "Your code did not finish this case successfully.";
            if (definition.Batch is 1 or 3 or 5)
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
            if (definition.Batch is 1 or 3 or 5) return observed.GetProperty("actual").Clone();
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
