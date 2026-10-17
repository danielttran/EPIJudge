using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class EnumerateBalancedParentheses
{
    public static List<string> Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "enumerate_balanced_parentheses.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(List<string>), values => Solve((int)values[0]!));
}
