using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int Parity(long x)
    {
        ulong remaining = unchecked((ulong)x);
        int parity = 0;
        while (remaining != 0)
        {
            parity ^= 1;
            remaining &= remaining - 1;
        }
        return parity;
    }
}
