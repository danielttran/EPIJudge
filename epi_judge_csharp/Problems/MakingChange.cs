using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MakingChange
{
    public static int Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "making_change.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(int), values => Solve((int)values[0]!));
}
