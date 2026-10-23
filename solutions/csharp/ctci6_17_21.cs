using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int HistogramWaterVolume(int[] heights)
    {
        int left = 0, right = heights.Length - 1, leftMax = 0, rightMax = 0, volume = 0;
        while (left <= right)
        {
            if (leftMax <= rightMax)
            {
                leftMax = Math.Max(leftMax, heights[left]);
                volume += leftMax - heights[left];
                ++left;
            }
            else
            {
                rightMax = Math.Max(rightMax, heights[right]);
                volume += rightMax - heights[right];
                --right;
            }
        }
        return volume;
    }
}
