using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] SearchSortedMatrix(int[][] matrix, int target)
    {
        int rows = matrix.Length, columns = rows == 0 ? 0 : matrix[0].Length, row = 0,
            column = columns - 1;
        while (row < rows && column >= 0)
        {
            int value = matrix[row][column];
            if (value == target)
                return [row, column];
            if (value > target)
                --column;
            else
                ++row;
        }
        return [-1, -1];
    }
}
