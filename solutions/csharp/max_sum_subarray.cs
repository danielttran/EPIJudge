using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindMaximumSubarray(List<int> A)
    {
        int suffix = 0, best = 0;
        foreach (int value in A)
        {
            suffix = Math.Max(0, suffix + value);
            best = Math.Max(best, suffix);
        }
        return best;
    }
}
