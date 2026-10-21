using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public double BuyAndSellStockKTimes(List<double> prices, int k)
    {
        if (k <= 0 || prices.Count < 2)
            return 0;
        if (k >= prices.Count / 2)
        {
            double total = 0;
            for (int i = 1; i < prices.Count; i++)
                total += Math.Max(0, prices[i] - prices[i - 1]);
            return total;
        }
        var holding = Enumerable.Repeat(double.NegativeInfinity, k + 1).ToArray();
        var sold = new double[k + 1];
        foreach (double price in prices)
            for (int transaction = k; transaction >= 1; transaction--)
            {
                sold[transaction] = Math.Max(sold[transaction], holding[transaction] + price);
                holding[transaction] = Math.Max(holding[transaction], sold[transaction - 1] - price);
            }
        return sold[k];
    }
}
