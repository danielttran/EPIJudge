using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Gcd
{
    public static long Solve(long arg1, long arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "gcd.tsv", new[] { "arg1", "arg2" }, new[] { typeof(long), typeof(long) },
            typeof(long), values => Solve((long)values[0]!, (long)values[1]!));
}
