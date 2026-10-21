using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int NumberOfWays(int n, int m)
    {
        if (n <= 0 || m <= 0)
            return 0;
        int[] ways = Enumerable.Repeat(1, Math.Min(n, m)).ToArray();
        for (int r = 1; r < Math.Max(n, m); r++)
        for (int c = 1; c < ways.Length; c++)
            ways[c] += ways[c - 1];
        return ways[^1];
    }
}
