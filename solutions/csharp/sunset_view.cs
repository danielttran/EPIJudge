using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> ExamineBuildingsWithSunset(List<int> sequence)
    {
        var visible = new List<int>();
        int maximum = int.MinValue;
        bool any = false;
        for (int i = sequence.Count - 1; i >= 0; i--)
            if (!any || sequence[i] > maximum)
            {
                visible.Add(i);
                maximum = sequence[i];
                any = true;
            }
        return visible;
    }
}
