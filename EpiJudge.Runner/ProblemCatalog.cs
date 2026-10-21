using System.Text.Json;

namespace EpiJudge.Runner;

public sealed record Example(string Input, string Output, string Explanation);
public sealed record Problem(string Id, string Title, string Topic, string Difficulty,
    string Description, string[] Constraints, string Signature, string StarterCode,
    Example[] Examples, string Invocation, bool Unordered = false,
    int ArgumentCount = 1, int TestCount = 0, string Comparison = "ordered", string ResultType = "",
    string? JsSignature = null, string? JsStarterCode = null, string? JsInvocation = null,
    string[]? ArgumentTypes = null,
    string? PySignature = null, string? PyStarterCode = null, string? PyInvocation = null,
    string? PySourceFile = null, string Collection = "epi", int Position = 0,
    string? Diagram = null, string? DiagramAlt = null,
    string? SourceUrl = null, string? SourceAttribution = null);
public sealed record TestCase(JsonElement[] Arguments, JsonElement Expected);

public sealed class ProblemCatalog
{
    private static readonly IReadOnlyList<Problem> Additional = LoadCatalog();
    public IReadOnlyList<Problem> Problems { get; }

    public ProblemCatalog()
    {
        Problems = Curated.Concat(Additional).Concat(Blind75Catalog.Problems).Concat(InterviewCakeCatalog.Problems).ToArray();
    }

    private static readonly Problem[] Curated =
    [
        new("count_bits", "Count Bits", "Primitive types", "Unrated",
            "Count the number of bits set to 1 in the 32-bit binary representation of an integer. Return the count. Treat negative inputs as their 32-bit two's-complement representation.",
            ["Input is a signed 32-bit integer.", "Return an integer from 0 to 32.", "Try solving it without converting the input to a string."],
            "int CountBits(int x)",
            "public class Solution\n{\n    public int CountBits(int x)\n    {\n        // Write your solution here.\n        return 0;\n    }\n}\n",
            [new("x = 0", "0", "Illustrative example: no bits are set."), new("x = 7", "3", "Illustrative example: 7 is 111 in binary."), new("x = -1", "32", "Illustrative C# example: all 32 bits are set.")],
            "new Solution().CountBits(arguments[0].GetInt32())", TestCount: 10001,
            JsSignature: "function countBits(x)",
            JsStarterCode: "/**\n * @param {number} x\n * @return {number}\n */\nfunction countBits(x) {\n    // Write your solution here.\n    return 0;\n}\n\nmodule.exports = { countBits };\n",
            JsInvocation: "countBits",
            ArgumentTypes: ["int"],
            PySignature: "def count_bits(x: int) -> int",
            PyStarterCode: "from test_framework import generic_test\n\n\ndef count_bits(x: int) -> int:\n    # TODO - you fill in here.\n    return 0\n",
            PyInvocation: "count_bits",
            PySourceFile: "count_bits.py"),
        new("two_sum", "Two Sum", "Arrays", "Unrated",
            "Given an array sorted in nondecreasing order and a target, determine whether two values in the array add up to the target. Return true if they do. This EPI variant allows you to use the same array element twice.",
            ["The input array is sorted.", "You may reuse the same element, so [3] with target 6 returns true.", "Return a boolean rather than the indices."],
            "bool HasTwoSum(List<int> values, int target)",
            "public class Solution\n{\n    public bool HasTwoSum(List<int> values, int target)\n    {\n        // Write your solution here.\n        return false;\n    }\n}\n",
            [new("values = [-2, 1, 2, 4, 7, 11], target = 6", "true", "Illustrative example: 2 + 4 = 6."), new("values = [3], target = 6", "true", "Illustrative example: the same element may be used twice.")],
            "new Solution().HasTwoSum(arguments[0].Deserialize<List<int>>()!, arguments[1].GetInt32())", ArgumentCount: 2, TestCount: 1005,
            JsSignature: "function hasTwoSum(values, target)",
            JsStarterCode: "/**\n * @param {number[]} values\n * @param {number} target\n * @return {boolean}\n */\nfunction hasTwoSum(values, target) {\n    // Write your solution here.\n    return false;\n}\n\nmodule.exports = { hasTwoSum };\n",
            JsInvocation: "hasTwoSum",
            ArgumentTypes: ["array(int)", "int"],
            PySignature: "def has_two_sum(A: List[int], t: int) -> bool",
            PyStarterCode: "from typing import List\n\nfrom test_framework import generic_test\n\n\ndef has_two_sum(A: List[int], t: int) -> bool:\n    # TODO - you fill in here.\n    return True\n",
            PyInvocation: "has_two_sum",
            PySourceFile: "two_sum.py"),
        new("anagrams", "Group Anagrams", "Hash tables", "Unrated",
            "Group dictionary entries that contain exactly the same characters with the same frequencies. Return only groups containing at least two entries. Character case and spaces are significant. The order of groups and words does not matter.",
            ["Each input entry is a string.", "Omit groups that contain just one entry.", "Keep each input entry intact in the output."],
            "List<List<string>> FindAnagrams(List<string> dictionary)",
            "public class Solution\n{\n    public List<List<string>> FindAnagrams(List<string> dictionary)\n    {\n        // Write your solution here.\n        return [];\n    }\n}\n",
            [new("dictionary = [\"eat\", \"tea\", \"tan\", \"ate\"]", "[[\"eat\", \"tea\", \"ate\"]]", "Illustrative example: only the three entries with the same characters form a group.")],
            "new Solution().FindAnagrams(arguments[0].Deserialize<List<string>>()!)", true, TestCount: 9,
            JsSignature: "function findAnagrams(dictionary)",
            JsStarterCode: "/**\n * @param {string[]} dictionary\n * @return {string[][]}\n */\nfunction findAnagrams(dictionary) {\n    // Write your solution here.\n    return [];\n}\n\nmodule.exports = { findAnagrams };\n",
            JsInvocation: "findAnagrams",
            ArgumentTypes: ["array(string)"],
            PySignature: "def find_anagrams(dictionary: List[str]) -> List[List[str]]",
            PyStarterCode: "from typing import List\n\nfrom test_framework import generic_test\n\n\ndef find_anagrams(dictionary: List[str]) -> List[List[str]]:\n    # TODO - you fill in here.\n    return []\n",
            PyInvocation: "find_anagrams",
            PySourceFile: "anagrams.py")
    ];

    private static IReadOnlyList<Problem> LoadCatalog()
    {
        using var stream = typeof(ProblemCatalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.catalog.json")
            ?? throw new InvalidOperationException("The embedded problem catalog is missing.");
        return JsonSerializer.Deserialize<Problem[]>(stream) ?? throw new InvalidOperationException("The problem catalog is invalid.");
    }

    public Problem? Find(string id) => Problems.FirstOrDefault(problem => problem.Id == id);

    public static string FindRepositoryRoot(string startingDirectory)
    {
        for (var directory = new DirectoryInfo(startingDirectory); directory is not null; directory = directory.Parent)
            if (Directory.Exists(Path.Combine(directory.FullName, "test_data")) &&
                File.Exists(Path.Combine(directory.FullName, "EPIJudge.Web.slnx"))) return directory.FullName;
        throw new DirectoryNotFoundException("Run this application from the EPIJudge repository so its test_data folder is available.");
    }

    public static List<TestCase> LoadTests(string repositoryRoot, string problemId, bool examplesOnly)
    {
        if (Blind75Catalog.Find(problemId) is not null)
            return Blind75Catalog.LoadTests(repositoryRoot, problemId, examplesOnly);
        if (InterviewCakeCatalog.Find(problemId) is not null)
            return InterviewCakeCatalog.LoadTests(repositoryRoot, problemId, examplesOnly);
        var problem = Curated.Concat(Additional).First(p => p.Id == problemId);
        var lines = File.ReadLines(Path.Combine(repositoryRoot, "test_data", problemId + ".tsv")).Skip(1);
        // Run uses a small visible slice of the real corpus. Submit uses every row.
        if (examplesOnly) lines = lines.Take(3);
        return lines.Select(line =>
        {
            var fields = line.Split('\t');
            var argumentCount = problem.ArgumentCount;
            var expected = problem.ResultType == "void" ? Parse("true") : Parse(fields[argumentCount]);
            if (problem.ResultType.StartsWith("binary_tree("))
            {
                // Equivalent trees may omit trailing null child markers.
                var nodes = expected.EnumerateArray().ToList();
                while (nodes.Count > 0 && nodes[^1].ValueKind == JsonValueKind.Null) nodes.RemoveAt(nodes.Count-1);
                expected = JsonSerializer.SerializeToElement(nodes);
            }
            return new TestCase(fields.Take(argumentCount).Select(Parse).ToArray(), expected);
        }).ToList();
    }

    private static JsonElement Parse(string json) => JsonSerializer.Deserialize<JsonElement>(json);
}
