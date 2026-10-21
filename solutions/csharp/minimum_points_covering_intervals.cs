using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindMinimumVisits(List<(int, int)> A)
    {
        int visits = 0;
        long last = long.MinValue;
        foreach (var interval in A.OrderBy(x => x.Item2))
            if (interval.Item1 > last)
            {
                visits++;
                last = interval.Item2;
            }
        return visits;
    }
}
