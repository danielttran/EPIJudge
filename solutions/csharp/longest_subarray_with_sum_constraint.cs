using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindLongestSubarrayLessEqualK(List<int> A, int k)
    {
        long[] prefix = new long[A.Count + 1], maximum = new long[A.Count + 1];
        for (int i = 0; i < A.Count; i++)
        {
            prefix[i + 1] = prefix[i] + A[i];
            maximum[i + 1] = Math.Max(maximum[i], prefix[i + 1]);
        }
        int best = 0;
        for (int end = 1; end <= A.Count; end++)
        {
            long threshold = prefix[end] - k;
            int low = 0, high = end;
            while (low < high)
            {
                int mid = low + (high - low) / 2;
                if (maximum[mid] >= threshold)
                    high = mid;
                else
                    low = mid + 1;
            }
            best = Math.Max(best, end - low);
        }
        return best;
    }
}
