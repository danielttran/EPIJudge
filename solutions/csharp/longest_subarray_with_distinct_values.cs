using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int LongestSubarrayWithDistinctEntries(List<int> A)
    {
        var last = new Dictionary<int, int>();
        int left = 0, best = 0;
        for (int right = 0; right < A.Count; right++)
        {
            if (last.TryGetValue(A[right], out int previous))
                left = Math.Max(left, previous + 1);
            last[A[right]] = right;
            best = Math.Max(best, right - left + 1);
        }
        return best;
    }
}
