using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int CalculateBonus(List<int> productivity)
    {
        int n = productivity.Count;
        var bonuses = Enumerable.Repeat(1, n).ToArray();
        for (int i = 1; i < n; i++)
            if (productivity[i] > productivity[i - 1])
                bonuses[i] = bonuses[i - 1] + 1;
        for (int i = n - 2; i >= 0; i--)
            if (productivity[i] > productivity[i + 1])
                bonuses[i] = Math.Max(bonuses[i], bonuses[i + 1] + 1);
        return bonuses.Sum();
    }
}
