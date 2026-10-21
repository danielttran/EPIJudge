using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int CalculateTrappingWater(List<int> heights)
    {
        int left = 0, right = heights.Count - 1, leftMax = 0, rightMax = 0, water = 0;
        while (left <= right)
        {
            if (leftMax <= rightMax)
            {
                leftMax = Math.Max(leftMax, heights[left]);
                water += leftMax - heights[left++];
            }
            else
            {
                rightMax = Math.Max(rightMax, heights[right]);
                water += rightMax - heights[right--];
            }
        }
        return water;
    }
}
