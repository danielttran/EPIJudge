using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public long ReverseBits(long x)
    {
        ulong source = unchecked((ulong)x), result = 0;
        for (int bit = 0; bit < 64; bit++)
        {
            result = (result << 1) | (source & 1);
            source >>= 1;
        }
        return unchecked((long)result);
    }
}
