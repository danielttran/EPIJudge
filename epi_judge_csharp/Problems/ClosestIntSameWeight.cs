using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ClosestIntSameWeight
{
    public static long Solve(long arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "closest_int_same_weight.tsv", new[] { "arg1" }, new[] { typeof(long) },
            typeof(long), values => Solve((long)values[0]!));
}
