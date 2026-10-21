using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool CanReachEnd(List<int> A)
    {
        long farthest = 0;
        for (int i = 0; i < A.Count && i <= farthest; i++)
        {
            farthest = Math.Max(farthest, (long)i + A[i]);
            if (farthest >= A.Count - 1)
                return true;
        }
        return A.Count == 0;
    }
}
