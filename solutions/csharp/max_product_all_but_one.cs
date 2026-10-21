using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindBiggestNMinusOneProduct(List<int> A)
    {
        if (A.Count == 0)
            return 0;
        System.Numerics.BigInteger product = 1;
        int zeroes = 0;
        foreach (int value in A)
        {
            if (value == 0)
                zeroes++;
            else
                product *= value;
        }
        if (zeroes > 1)
            return 0;
        if (zeroes == 1)
            return (int)(A.Count == 1 ? product : System.Numerics.BigInteger.Max(0, product));
        var best = product / A[0];
        foreach (int value in A)
            best = System.Numerics.BigInteger.Max(best, product / value);
        return (int)best;
    }
}
