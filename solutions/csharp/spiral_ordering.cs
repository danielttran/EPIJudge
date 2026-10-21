using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> MatrixInSpiralOrder(List<List<int>> square_matrix)
    {
        var result = new List<int>();
        int top = 0, bottom = square_matrix.Count - 1;
        int left = 0, right = bottom;
        while (top <= bottom && left <= right)
        {
            for (int c = left; c <= right; c++)
                result.Add(square_matrix[top][c]);
            top++;
            for (int r = top; r <= bottom; r++)
                result.Add(square_matrix[r][right]);
            right--;
            if (top <= bottom)
            {
                for (int c = right; c >= left; c--)
                    result.Add(square_matrix[bottom][c]);
                bottom--;
            }
            if (left <= right)
            {
                for (int r = bottom; r >= top; r--)
                    result.Add(square_matrix[r][left]);
                left++;
            }
        }
        return result;
    }
}
