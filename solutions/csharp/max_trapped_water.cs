using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int GetMaxTrappedWater(List<int> heights)
    {
        int left = 0, right = heights.Count - 1, best = 0;
        while (left < right)
        {
            best = Math.Max(best, (right - left) * Math.Min(heights[left], heights[right]));
            if (heights[left] <= heights[right])
                left++;
            else
                right--;
        }
        return best;
    }
}
