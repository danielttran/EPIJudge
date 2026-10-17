using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class OnlineMedian
{
    public static List<double> Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "online_median.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(List<double>), values => Solve((List<int>)values[0]!));
}
