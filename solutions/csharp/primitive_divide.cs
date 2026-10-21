using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int Divide(int x, int y)
    {
        if (y <= 0)
            throw new ArgumentOutOfRangeException(nameof(y));
        long remaining = x;
        int quotient = 0;
        for (int bit = 30; bit >= 0; bit--)
        {
            long part = (long)y << bit;
            if (part <= remaining)
            {
                remaining -= part;
                quotient |= 1 << bit;
            }
        }
        return quotient;
    }
}
