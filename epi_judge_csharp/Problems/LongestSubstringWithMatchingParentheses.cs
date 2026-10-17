using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LongestSubstringWithMatchingParentheses
{
    public static int Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "longest_substring_with_matching_parentheses.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(int), values => Solve((string)values[0]!));
}
