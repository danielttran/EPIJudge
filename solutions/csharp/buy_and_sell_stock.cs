using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public double BuyAndSellStockOnce(List<double> prices)
    {
        double minimum = double.PositiveInfinity, profit = 0;
        foreach (double price in prices)
        {
            profit = Math.Max(profit, price - minimum);
            minimum = Math.Min(minimum, price);
        }
        return profit;
    }
}
