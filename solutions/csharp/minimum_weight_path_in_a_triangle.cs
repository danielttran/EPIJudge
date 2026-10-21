using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MinimumPathWeight(List<List<int>> triangle)
    {
        if (triangle.Count == 0)
            return 0;
        int[] costs = triangle[^1].ToArray();
        for (int r = triangle.Count - 2; r >= 0; r--)
            for (int c = 0; c <= r; c++)
                costs[c] = triangle[r][c] + Math.Min(costs[c], costs[c + 1]);
        return costs[0];
    }
}
