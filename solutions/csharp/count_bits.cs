using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int CountBits(int x)
    {
        uint remaining = unchecked((uint)x);
        int count = 0;
        while (remaining != 0)
        {
            remaining &= remaining - 1;
            count++;
        }
        return count;
    }
}
