using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> MergeTwoSortedArrays(List<int> A, int m, List<int> B, int n)
    {
        int first = m - 1, second = n - 1, output = m + n - 1;
        while (second >= 0)
        {
            if (first >= 0 && A[first] > B[second])
                A[output--] = A[first--];
            else
                A[output--] = B[second--];
        }
        return A;
    }
}
