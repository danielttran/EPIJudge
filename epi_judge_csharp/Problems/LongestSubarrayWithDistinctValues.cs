using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LongestSubarrayWithDistinctValues
{
    public static int Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "longest_subarray_with_distinct_values.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(int), values => Solve((List<int>)values[0]!));
}
