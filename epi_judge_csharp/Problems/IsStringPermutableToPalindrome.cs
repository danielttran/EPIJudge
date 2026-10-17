using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsStringPermutableToPalindrome
{
    public static bool Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_string_permutable_to_palindrome.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(bool), values => Solve((string)values[0]!));
}
