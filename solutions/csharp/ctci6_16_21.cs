using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] SumSwap(int[] first, int[] second)
    {
        long difference = 0;
        foreach (int value in first)
            difference += value;
        foreach (int value in second)
            difference -= value;
        if (difference % 2 != 0)
        {
            return [];
        }
        long half = difference / 2;
        var contents = new HashSet<int>(second);
        foreach (int value in first)
        {
            long required = (long)value - half;
            if (required >= -2147483648L && required <= 2147483647L &&
                contents.Contains((int)required))
            {
                return [value, (int)required];
            }
        }
        return [];
    }
}
