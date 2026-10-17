using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KthLargestElementInLongArray
{
    public static int Solve(List<int> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "kth_largest_element_in_long_array.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(int) },
            typeof(int), values => Solve((List<int>)values[0]!, (int)values[1]!));
}
