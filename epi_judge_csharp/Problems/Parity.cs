using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Parity
{
    public static int Solve(long arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "parity.tsv", new[] { "arg1" }, new[] { typeof(long) },
            typeof(int), values => Solve((long)values[0]!));
}
