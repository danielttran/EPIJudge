using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public void SolveSudoku(List<List<int>> board)
    {
        int n = board.Count, width = (int)Math.Sqrt(n);
        var rows = Enumerable.Range(0, n).Select(_ => new bool[n + 1]).ToArray();
        var columns = Enumerable.Range(0, n).Select(_ => new bool[n + 1]).ToArray();
        var blocks = Enumerable.Range(0, n).Select(_ => new bool[n + 1]).ToArray();
        for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++)
            if (board[r][c] != 0)
                rows[r][board[r][c]] = columns[c][board[r][c]] = blocks[r / width * width + c / width][board[r][c]] = true;
        bool Fill()
        {
            int row = -1, column = -1, smallest = int.MaxValue;
            List<int>? choices = null;
            for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
            if (board[r][c] == 0)
            {
                int block = r / width * width + c / width;
                var options = new List<int>();
                for (int value = 1; value <= n; value++)
                if (!rows[r][value] && !columns[c][value] && !blocks[block][value])
                    options.Add(value);
                if (options.Count == 0)
                    return false;
                if (options.Count < smallest)
                {
                    row = r;
                    column = c;
                    smallest = options.Count;
                    choices = options;
                }
            }
            if (row < 0)
                return true;
            int box = row / width * width + column / width;
            foreach (int value in choices!)
            {
                board[row][column] = value;
                rows[row][value] = columns[column][value] = blocks[box][value] = true;
                if (Fill())
                    return true;
                rows[row][value] = columns[column][value] = blocks[box][value] = false;
                board[row][column] = 0;
            }
            return false;
        }
        if (!Fill())
            throw new InvalidOperationException("No Sudoku solution exists.");
    }
}
