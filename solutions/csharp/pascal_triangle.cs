using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> GeneratePascalTriangle(int n)
    {
        var rows = new List<List<int>>();
        for (int r = 0; r < n; r++)
        {
            var row = Enumerable.Repeat(1, r + 1).ToList();
            for (int c = 1; c < r; c++)
                row[c] = rows[r - 1][c - 1] + rows[r - 1][c];
            rows.Add(row);
        }
        return rows;
    }
}
