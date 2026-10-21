using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MaximumRevenue(List<int> coins)
    {
        int n = coins.Count;
        if (n == 0)
            return 0;
        var best = new int[n, n];
        int Value(int left, int right) => left > right ? 0 : best[left, right];
        for (int length = 1; length <= n; length++)
            for (int left = 0; left + length <= n; left++)
            {
                int right = left + length - 1;
                int takeLeft = coins[left] + Math.Min(Value(left + 2, right), Value(left + 1, right - 1));
                int takeRight = coins[right] + Math.Min(Value(left + 1, right - 1), Value(left, right - 2));
                best[left, right] = Math.Max(takeLeft, takeRight);
            }
        return best[0, n - 1];
    }
}
