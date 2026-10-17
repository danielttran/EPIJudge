using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MaximumSubarrayInCircularArray
{
    public static int Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "maximum_subarray_in_circular_array.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(int), values => Solve((List<int>)values[0]!));
}
