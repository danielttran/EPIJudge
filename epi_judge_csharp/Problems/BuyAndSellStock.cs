using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class BuyAndSellStock
{
    public static double Solve(List<double> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "buy_and_sell_stock.tsv", new[] { "arg1" }, new[] { typeof(List<double>) },
            typeof(double), values => Solve((List<double>)values[0]!));
}
