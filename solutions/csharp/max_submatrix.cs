using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MaxRectangleSubmatrix(List<List<bool>> A)
    {
        if (A.Count == 0)
            return 0;
        int[] heights = new int[A[0].Count];
        int best = 0;
        foreach (var row in A)
        {
            for (int c = 0; c < heights.Length; c++)
                heights[c] = row[c] ? heights[c] + 1 : 0;
            var stack = new Stack<int>();
            for (int c = 0; c <= heights.Length; c++)
            {
                int current = c == heights.Length ? 0 : heights[c];
                while (stack.Count > 0 && heights[stack.Peek()] >= current)
                {
                    int height = heights[stack.Pop()];
                    int left = stack.Count == 0 ? 0 : stack.Peek() + 1;
                    best = Math.Max(best, height * (c - left));
                }
                stack.Push(c);
            }
        }
        return best;
    }
}
