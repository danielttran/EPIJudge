using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SortedArraysMerge
{
    public static List<int> Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "sorted_arrays_merge.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            typeof(List<int>), values => Solve((List<List<int>>)values[0]!));
}
