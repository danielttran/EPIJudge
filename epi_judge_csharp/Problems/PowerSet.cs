using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PowerSet
{
    public static List<List<int>> Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "power_set.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(List<List<int>>), values => Solve((List<int>)values[0]!));
}
