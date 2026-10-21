using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> RotateMatrix(List<List<int>> square_matrix)
    {
        int n = square_matrix.Count;
        for (int r = 0; r < n; r++)
        for (int c = r + 1; c < n; c++)
            (square_matrix[r][c], square_matrix[c][r]) = (square_matrix[c][r], square_matrix[r][c]);
        foreach (var row in square_matrix)
            row.Reverse();
        return square_matrix;
    }
}
