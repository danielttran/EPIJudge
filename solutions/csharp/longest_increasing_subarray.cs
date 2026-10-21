using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindLongestIncreasingSubarray(List<int> A)
    {
        int best = 0, length = 0;
        for (int i = 0; i < A.Count; i++)
        {
            length = i > 0 && A[i] > A[i - 1] ? length + 1 : 1;
            best = Math.Max(best, length);
        }
        return best;
    }
}
