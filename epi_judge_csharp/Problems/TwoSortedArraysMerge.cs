using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class TwoSortedArraysMerge
{
    public static List<int> Solve(List<int> arg1, int arg2, List<int> arg3, int arg4)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "two_sorted_arrays_merge.tsv", new[] { "arg1", "arg2", "arg3", "arg4" }, new[] { typeof(List<int>), typeof(int), typeof(List<int>), typeof(int) },
            typeof(List<int>), values => Solve((List<int>)values[0]!, (int)values[1]!, (List<int>)values[2]!, (int)values[3]!));
}
