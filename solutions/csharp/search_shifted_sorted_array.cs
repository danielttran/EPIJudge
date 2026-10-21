using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SearchSmallest(List<int> A)
    {
        int left = 0, right = A.Count - 1;
        while (left < right)
        {
            int middle = left + (right - left) / 2;
            if (A[middle] > A[right])
                left = middle + 1;
            else
                right = middle;
        }
        return A.Count == 0 ? -1 : left;
    }
}
