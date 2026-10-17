using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KthLargestInArray
{
    public static int Solve(int arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "kth_largest_in_array.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<int>) },
            typeof(int), values => Solve((int)values[0]!, (List<int>)values[1]!));
}
