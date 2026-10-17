using System.Text.Json;

namespace EpiJudge.Runner;

public sealed record Example(string Input, string Output, string Explanation);
public sealed record Problem(string Id, string Title, string Topic, string Difficulty,
    string Description, string[] Constraints, string Signature, string StarterCode,
    Example[] Examples, string Invocation, bool Unordered = false);
public sealed record TestCase(JsonElement[] Arguments, JsonElement Expected);

public sealed class ProblemCatalog
{
    public IReadOnlyList<Problem> Problems { get; } =
    [
        new("count_bits", "Count Bits", "Primitive types", "Easy",
            "Count the number of bits set to 1 in the 32-bit binary representation of an integer. Return the count. Treat negative inputs as their 32-bit two's-complement representation.",
            ["Input is a signed 32-bit integer.", "Return an integer from 0 to 32.", "Try solving it without converting the input to a string."],
            "int CountBits(int x)",
            "public class Solution\n{\n    public int CountBits(int x)\n    {\n        // Write your solution here.\n        return 0;\n    }\n}\n",
            [new("x = 0", "0", "No bits are set."), new("x = 7", "3", "7 is 111 in binary."), new("x = -1", "32", "All 32 bits are set.")],
            "new Solution().CountBits(arguments[0].GetInt32())"),
        new("two_sum", "Two Sum", "Arrays", "Easy",
            "Given an array sorted in nondecreasing order and a target, determine whether two values in the array add up to the target. Return true if they do. This EPI variant allows you to use the same array element twice.",
            ["The input array is sorted.", "You may reuse the same element, so [3] with target 6 returns true.", "Return a boolean rather than the indices."],
            "bool HasTwoSum(List<int> values, int target)",
            "public class Solution\n{\n    public bool HasTwoSum(List<int> values, int target)\n    {\n        // Write your solution here.\n        return false;\n    }\n}\n",
            [new("values = [-2, 1, 2, 4, 7, 11], target = 6", "true", "2 + 4 = 6."), new("values = [3], target = 6", "true", "The same element may be used twice.")],
            "new Solution().HasTwoSum(arguments[0].Deserialize<List<int>>()!, arguments[1].GetInt32())"),
        new("anagrams", "Group Anagrams", "Hash tables", "Medium",
            "Group dictionary entries that contain exactly the same characters with the same frequencies. Return only groups containing at least two entries. Character case and spaces are significant. The order of groups and words does not matter.",
            ["Each input entry is a string.", "Omit groups that contain just one entry.", "Keep each input entry intact in the output."],
            "List<List<string>> FindAnagrams(List<string> dictionary)",
            "public class Solution\n{\n    public List<List<string>> FindAnagrams(List<string> dictionary)\n    {\n        // Write your solution here.\n        return [];\n    }\n}\n",
            [new("dictionary = [\"eat\", \"tea\", \"tan\", \"ate\"]", "[[\"eat\", \"tea\", \"ate\"]]", "Only the three entries with the same characters form a group.")],
            "new Solution().FindAnagrams(arguments[0].Deserialize<List<string>>()!)", true)
    ];

    public Problem? Find(string id) => Problems.FirstOrDefault(problem => problem.Id == id);

    public static string FindRepositoryRoot(string startingDirectory)
    {
        for (var directory = new DirectoryInfo(startingDirectory); directory is not null; directory = directory.Parent)
            if (Directory.Exists(Path.Combine(directory.FullName, "test_data")) &&
                File.Exists(Path.Combine(directory.FullName, "EPIJudge.slnx"))) return directory.FullName;
        throw new DirectoryNotFoundException("Run this application from the EPIJudge repository so its test_data folder is available.");
    }

    public static List<TestCase> LoadTests(string repositoryRoot, string problemId, bool examplesOnly)
    {
        var lines = File.ReadLines(Path.Combine(repositoryRoot, "test_data", problemId + ".tsv")).Skip(1);
        // Run uses a small visible slice of the real corpus. Submit uses every row.
        if (examplesOnly) lines = lines.Take(3);
        return lines.Select(line =>
        {
            var fields = line.Split('\t');
            var argumentCount = problemId == "two_sum" ? 2 : 1;
            return new TestCase(fields.Take(argumentCount).Select(Parse).ToArray(), Parse(fields[argumentCount]));
        }).ToList();
    }

    private static JsonElement Parse(string json) => JsonSerializer.Deserialize<JsonElement>(json);
}
