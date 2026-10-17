using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IntersectSortedArrays
{
    public static List<int> Solve(List<int> arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "intersect_sorted_arrays.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(List<int>) },
            typeof(List<int>), values => Solve((List<int>)values[0]!, (List<int>)values[1]!));
}
