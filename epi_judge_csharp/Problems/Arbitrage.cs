using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Arbitrage
{
    public static bool Solve(List<List<double>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "arbitrage.tsv", new[] { "arg1" }, new[] { typeof(List<List<double>>) },
            typeof(bool), values => Solve((List<List<double>>)values[0]!));
}
