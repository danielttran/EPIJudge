using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SmallestSubarrayCoveringAllValues
{
    public static int Solve(List<string> arg1, List<string> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "smallest_subarray_covering_all_values.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<string>), typeof(List<string>) },
            typeof(int), values => Solve((List<string>)values[0]!, (List<string>)values[1]!));
}
