using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int MaximumContiguousSum(int[] values)
    {
        int running = 0, best = 0;
        foreach (int value in values)
        {
            running = Math.Max(0, running + value);
            best = Math.Max(best, running);
        }
        return best;
    }
}
