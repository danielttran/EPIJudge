using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int CalculateLargestRectangle(List<int> heights)
    {
        var increasing = new Stack<int>();
        int best = 0;
        for (int right = 0; right <= heights.Count; right++)
        {
            int current = right == heights.Count ? 0 : heights[right];
            while (increasing.Count > 0 && heights[increasing.Peek()] >= current)
            {
                int height = heights[increasing.Pop()];
                int left = increasing.Count == 0 ? 0 : increasing.Peek() + 1;
                best = Math.Max(best, height * (right - left));
            }
            increasing.Push(right);
        }
        return best;
    }
}
