using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> RookAttack(List<List<int>> A)
    {
        var rows = new HashSet<int>();
        var columns = new HashSet<int>();
        for (int r = 0; r < A.Count; r++)
            for (int c = 0; c < A[r].Count; c++)
                if (A[r][c] == 0)
                {
                    rows.Add(r);
                    columns.Add(c);
                }
        for (int r = 0; r < A.Count; r++)
            for (int c = 0; c < A[r].Count; c++)
                if (rows.Contains(r) || columns.Contains(c))
                    A[r][c] = 0;
        return A;
    }
}
