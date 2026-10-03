using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Anagrams
{
    public static List<List<string>> Solve(List<string> dictionary)
    {
        // TODO - you fill in here.
        return [];
    }

    public static int Run(string[] args) =>
        GenericTest.Run<List<string>, List<List<string>>>(
            args, "anagrams.tsv", "dictionary", Solve, UnorderedGroupsEqual);

    private static bool UnorderedGroupsEqual(List<List<string>> expected, List<List<string>> actual) =>
        Normalize(expected).SequenceEqual(Normalize(actual));

    private static IEnumerable<string> Normalize(IEnumerable<List<string>> groups) =>
        groups.Select(group => string.Join("\u0000", group.OrderBy(word => word, StringComparer.Ordinal)))
            .OrderBy(group => group, StringComparer.Ordinal);
}
