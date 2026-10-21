using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int ComputeBinomialCoefficient(int n, int k)
    {
        if (k < 0 || k > n)
            return 0;
        k = Math.Min(k, n - k);
        long result = 1;
        for (int i = 1; i <= k; i++)
            result = result * (n - k + i) / i;
        return (int)result;
    }
}
