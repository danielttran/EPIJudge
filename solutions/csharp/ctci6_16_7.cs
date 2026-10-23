using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int MaximumWithoutComparison(int first, int second)
    {
        int negativeFirst = (int)((uint)first >> 31), negativeSecond = (int)((uint)second >> 31),
            negativeDifference = (int)(unchecked((uint)first - (uint)second) >> 31);
        int different = negativeFirst ^ negativeSecond,
            chooseFirst =
                different * (negativeFirst ^ 1) + (different ^ 1) * (negativeDifference ^ 1),
            mask = -chooseFirst;
        return (first & mask) | (second & ~mask);
    }
}
