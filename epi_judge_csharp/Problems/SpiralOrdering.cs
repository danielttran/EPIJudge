using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SpiralOrdering
{
    public static List<int> Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "spiral_ordering.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            typeof(List<int>), values => Solve((List<List<int>>)values[0]!));
}
