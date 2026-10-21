using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public double Power(double x, int y)
    {
        long exponent = y;
        if (exponent < 0)
        {
            x = 1.0 / x;
            exponent = -exponent;
        }
        double result = 1.0;
        while (exponent > 0)
        {
            if ((exponent & 1) != 0)
                result *= x;
            x *= x;
            exponent >>= 1;
        }
        return result;
    }
}
