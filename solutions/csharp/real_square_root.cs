using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public double SquareRoot(double x)
    {
        if (x == 0)
            return 0;
        double low = 0, high = Math.Max(1, x);
        for (int step = 0; step < 1100; step++)
        {
            double middle = low + (high - low) / 2;
            if (middle == low || middle == high)
                break;
            if (middle <= x / middle)
                low = middle;
            else
                high = middle;
        }
        return low + (high - low) / 2;
    }
}
