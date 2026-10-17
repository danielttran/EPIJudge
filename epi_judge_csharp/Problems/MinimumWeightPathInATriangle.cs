using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MinimumWeightPathInATriangle
{
    public static int Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "minimum_weight_path_in_a_triangle.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            typeof(int), values => Solve((List<List<int>>)values[0]!));
}
