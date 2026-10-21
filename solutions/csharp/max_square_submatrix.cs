using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int MaxSquareSubmatrix(List<List<bool>> A)
    {
        if (A.Count == 0)
            return 0;
        int[] previous = new int[A[0].Count + 1];
        int side = 0;
        foreach (var row in A)
        {
            int[] current = new int[row.Count + 1];
            for (int c = 1; c <= row.Count; c++)
            if (row[c - 1])
            {
                current[c] = 1 + Math.Min(previous[c - 1], Math.Min(previous[c], current[c - 1]));
                side = Math.Max(side, current[c]);
            }
            previous = current;
        }
        return side * side;
    }
}
