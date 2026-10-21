using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public long Reverse(int x)
    {
        long remaining = Math.Abs((long)x), reversed = 0;
        while (remaining != 0)
        {
            reversed = reversed * 10 + remaining % 10;
            remaining /= 10;
        }
        return x < 0 ? -reversed : reversed;
    }
}
