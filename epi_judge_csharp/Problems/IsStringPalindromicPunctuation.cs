using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsStringPalindromicPunctuation
{
    public static bool Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_string_palindromic_punctuation.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(bool), values => Solve((string)values[0]!));
}
