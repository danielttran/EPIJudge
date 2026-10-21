using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public long ClosestIntSameBitCount(long x)
    {
        for (int bit = 0; bit < 62; bit++)
            if (((x >> bit) & 1) != ((x >> (bit + 1)) & 1))
                return x ^ (1L << bit) ^ (1L << (bit + 1));
        throw new ArgumentException("No different nonnegative value has the same set-bit count.");
    }
}
