using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool TestCollatzConjecture(int n)
    {
        for (long start = 3; start <= n; start += 2)
        {
            var seen = new HashSet<long>();
            long value = start;
            while (value >= start)
            {
                if (!seen.Add(value))
                    return false;
                if ((value & 1) == 0)
                    value /= 2;
                else
                    value = checked(3 * value + 1);
            }
        }
        return true;
    }
}
