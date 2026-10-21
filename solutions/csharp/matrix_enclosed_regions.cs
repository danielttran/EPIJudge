using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<string>> FillSurroundedRegions(List<List<string>> board)
    {
        if (board.Count == 0 || board[0].Count == 0)
            return board;
        int rows = board.Count, columns = board[0].Count;
        var safe = new bool[rows, columns];
        var queue = new Queue<(int Row, int Column)>();
        void Add(int r, int c)
        {
            if (r >= 0 && r < rows && c >= 0 && c < columns && !safe[r, c] && board[r][c] == "W")
            {
                safe[r, c] = true;
                queue.Enqueue((r, c));
            }
        }
        for (int r = 0; r < rows; r++)
        {
            Add(r, 0);
            Add(r, columns - 1);
        }
        for (int c = 0; c < columns; c++)
        {
            Add(0, c);
            Add(rows - 1, c);
        }
        while (queue.TryDequeue(out var cell))
        {
            Add(cell.Row - 1, cell.Column);
            Add(cell.Row + 1, cell.Column);
            Add(cell.Row, cell.Column - 1);
            Add(cell.Row, cell.Column + 1);
        }
        for (int r = 0; r < rows; r++)
        for (int c = 0; c < columns; c++)
        if (board[r][c] == "W" && !safe[r, c])
            board[r][c] = "B";
        return board;
    }
}
