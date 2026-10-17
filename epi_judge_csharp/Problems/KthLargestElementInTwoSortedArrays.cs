using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KthLargestElementInTwoSortedArrays
{
    public static int Solve(List<int> arg1, List<int> arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "kth_largest_element_in_two_sorted_arrays.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(List<int>), typeof(List<int>), typeof(int) },
            typeof(int), values => Solve((List<int>)values[0]!, (List<int>)values[1]!, (int)values[2]!));
}
