using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private static ulong Add(ulong a, ulong b)
    {
        while (b != 0)
        {
            ulong carry = (a & b) << 1;
            a ^= b;
            b = carry;
        }
        return a;
    }
    public long Multiply(long x, long y)
    {
        ulong a = (ulong)x, b = (ulong)y, product = 0;
        while (a != 0)
        {
            if ((a & 1) != 0)
                product = Add(product, b);
            a >>= 1;
            b <<= 1;
        }
        return unchecked((long)product);
    }
}
