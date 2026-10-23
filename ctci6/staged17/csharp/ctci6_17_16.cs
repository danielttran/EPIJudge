using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int MaximumMassageMinutes(int[] appointments)
    {
        int oneBack = 0, twoBack = 0;
        foreach (int duration in appointments)
        {
            int current = Math.Max(oneBack, duration + twoBack);
            twoBack = oneBack;
            oneBack = current;
        }
        return oneBack;
    }
}
