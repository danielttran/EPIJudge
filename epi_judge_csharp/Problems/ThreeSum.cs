using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ThreeSum
{
    public static bool Solve(List<int> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "three_sum.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(int) },
            typeof(bool), values => Solve((List<int>)values[0]!, (int)values[1]!));
}
