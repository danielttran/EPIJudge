using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MinimumDistance3SortedArrays
{
    public static int Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "minimum_distance_3_sorted_arrays.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            typeof(int), values => Solve((List<List<int>>)values[0]!));
}
