using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SunsetView
{
    public static List<int> Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "sunset_view.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(List<int>), values => Solve((List<int>)values[0]!));
}
