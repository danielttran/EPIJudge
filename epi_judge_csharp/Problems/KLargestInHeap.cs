using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KLargestInHeap
{
    public static List<int> Solve(List<int> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "k_largest_in_heap.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(int) },
            typeof(List<int>), values => Solve((List<int>)values[0]!, (int)values[1]!),
            (expected, actual) => GenericTest.UnorderedEquals(expected, actual, typeof(List<int>)));
}
