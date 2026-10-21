using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool CheckFeasible(List<(int, int)> jugs, int l, int h)
    {
        var impossible = new HashSet<(int Low, int High)>();
        bool Search(int low, int high)
        {
            if (low <= 0 && high >= 0)
                return true;
            if (high < 0 || low > high || impossible.Contains((low, high)))
                return false;
            foreach (var (jugLow, jugHigh) in jugs)
            {
                if (jugLow <= 0 || jugHigh < jugLow)
                    continue;
                if (Search(low - jugLow, high - jugHigh))
                    return true;
            }
            impossible.Add((low, high));
            return false;
        }
        return Search(l, h);
    }
}
