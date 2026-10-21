using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public double BuyAndSellStockTwice(List<double> prices)
    {
        double firstBuy = double.NegativeInfinity, firstSell = 0;
        double secondBuy = double.NegativeInfinity, secondSell = 0;
        foreach (double price in prices)
        {
            secondSell = Math.Max(secondSell, secondBuy + price);
            secondBuy = Math.Max(secondBuy, firstSell - price);
            firstSell = Math.Max(firstSell, firstBuy + price);
            firstBuy = Math.Max(firstBuy, -price);
        }
        return secondSell;
    }
}
