using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool MatrixSearch(List<List<int>> A, int x)
    {
        if (A.Count == 0 || A[0].Count == 0)
            return false;
        int row = 0, column = A[0].Count - 1;
        while (row < A.Count && column >= 0)
        {
            int value = A[row][column];
            if (value == x)
                return true;
            if (value > x)
                column--;
            else
                row++;
        }
        return false;
    }
}
