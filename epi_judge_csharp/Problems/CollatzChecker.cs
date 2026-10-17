using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class CollatzChecker
{
    public static bool Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "collatz_checker.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(bool), values => Solve((int)values[0]!));
}
