using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class BuyAndSellStockKTimes
{
    public static double Solve(List<double> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "buy_and_sell_stock_k_times.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<double>), typeof(int) },
            typeof(double), values => Solve((List<double>)values[0]!, (int)values[1]!));
}
