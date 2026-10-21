using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public long SwapBits(long x, int i, int j)
    {
        ulong bits = unchecked((ulong)x);
        if (((bits >> i) & 1UL) != ((bits >> j) & 1UL))
            bits ^= (1UL << i) | (1UL << j);
        return unchecked((long)bits);
    }
}
