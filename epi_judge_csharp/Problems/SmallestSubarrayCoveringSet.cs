using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SmallestSubarrayCoveringSet
{
    public static int Solve(List<string> arg1, HashSet<string> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "smallest_subarray_covering_set.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<string>), typeof(HashSet<string>) },
            typeof(int), values => Solve((List<string>)values[0]!, (HashSet<string>)values[1]!));
}
