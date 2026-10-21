using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MaxSubarraySumInCircular(List<int> A)
    {
        long maximumSuffix = 0, minimumSuffix = 0, best = 0, worst = 0, total = 0;
        foreach (int value in A)
        {
            total += value;
            maximumSuffix = Math.Max(0, maximumSuffix + value);
            best = Math.Max(best, maximumSuffix);
            minimumSuffix = Math.Min(0, minimumSuffix + value);
            worst = Math.Min(worst, minimumSuffix);
        }
        return (int)Math.Max(best, total - worst);
    }
}
