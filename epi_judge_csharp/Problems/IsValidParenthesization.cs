using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsValidParenthesization
{
    public static bool Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_valid_parenthesization.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(bool), values => Solve((string)values[0]!));
}
