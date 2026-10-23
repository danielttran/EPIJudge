using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] MissingTwo(int[] values)
    {
        int n = values.Length + 2, combined = 0;
        for (int value = 1; value <= n; ++value)
            combined ^= value;
        foreach (int value in values)
            combined ^= value;
        int bit = combined & -combined, first = 0, second = 0;
        for (int value = 1; value <= n; ++value)
        {
            if ((value & bit) != 0)
                first ^= value;
            else
                second ^= value;
        }
        foreach (int value in values)
        {
            if ((value & bit) != 0)
                first ^= value;
            else
                second ^= value;
        }
        return [Math.Min(first, second), Math.Max(first, second)];
    }
}
