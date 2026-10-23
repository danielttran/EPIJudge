using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<List<int>> FindRobotPath(int[][] grid)
    {
        int rows = grid.Length, columns = rows == 0 ? 0 : grid[0].Length;
        if (rows == 0 || columns == 0)
        {
            return [];
        }
        int[,] parent = new int[rows, columns];
        var path = new List<List<int>>();
        for (int r = 0; r < rows; ++r)
        {
            for (int c = 0; c < columns; ++c)
            {
                if (grid[r][c] == 0)
                    continue;
                if (r == 0 && c == 0)
                    parent[r, c] = 3;
                else if (r > 0 && parent[r - 1, c] != 0)
                    parent[r, c] = 1;
                else if (c > 0 && parent[r, c - 1] != 0)
                    parent[r, c] = 2;
            }
        }
        if (parent[rows - 1, columns - 1] == 0)
        {
            return [];
        }
        int row = rows - 1, col = columns - 1;
        while (true)
        {
            path.Add([row, col]);
            if (row == 0 && col == 0)
                break;
            if (parent[row, col] == 1)
                --row;
            else
                --col;
        }
        path.Reverse();
        return path;
    }
}
