using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SearchFirstOfK(List<int> A, int k)
    {
        int left = 0, right = A.Count;
        while (left < right)
        {
            int middle = left + (right - left) / 2;
            if (A[middle] < k)
                left = middle + 1;
            else
                right = middle;
        }
        return left < A.Count && A[left] == k ? left : -1;
    }
}
