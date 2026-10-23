using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] PlayMinesweeper(int[][] bombs, int[][] actions)
    {
        int rows = bombs.Length, columns = bombs[0].Length;
        var visible = Enumerable.Range(0, rows)
                          .Select(
                              _ => Enumerable.Repeat(9, columns).ToArray())
                          .ToArray();
        int remaining = 0, state = 0;
        foreach (var row in bombs)
            foreach (int value in row)
                if (value == 0)
                    remaining++;
        var trace = new List<int[]>();
        void Snapshot(int accepted)
        {
            var result = new int[2 + rows * columns];
            result[0] = state;
            result[1] = accepted;
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < columns; c++)
                    result[2 + r * columns + c] = visible[r][c];
            trace.Add(result);
        }
        void Expose(int row, int column, List<int[]> queue)
        {
            if (visible[row][column] != 9 || bombs[row][column] != 0)
                return;
            int number = 0;
            for (int r = Math.Max(0, row - 1); r < Math.Min(rows, row + 2); ++r)
                for (int c = Math.Max(0, column - 1); c < Math.Min(columns, column + 2); ++c)
                    number += bombs[r][c];
            visible[row][column] = number;
            --remaining;
            if (number == 0)
                queue.Add(new int[] { row, column });
        }
        Snapshot(0);
        foreach (var action in actions)
        {
            int row = action[0], column = action[1], kind = action[2], accepted = 0;
            if (state == 0 && row >= 0 && row < rows && column >= 0 && column < columns)
            {
                if (kind == 1 && (visible[row][column] == 9 || visible[row][column] == 10))
                {
                    visible[row][column] = 19 - visible[row][column];
                    accepted = 1;
                }
                else if (kind == 0 && visible[row][column] == 9)
                {
                    accepted = 1;
                    if (bombs[row][column] != 0)
                    {
                        visible[row][column] = 11;
                        state = 2;
                    }
                    else
                    {
                        var queue = new List<int[]>();
                        Expose(row, column, queue);
                        for (int head = 0; head < queue.Count; ++head)
                        {
                            int r = queue[head][0], c = queue[head][1];
                            for (int nr = Math.Max(0, r - 1); nr < Math.Min(rows, r + 2); ++nr)
                                for (int nc = Math.Max(0, c - 1); nc < Math.Min(columns, c + 2);
                                     ++nc)
                                    Expose(nr, nc, queue);
                        }
                        if (remaining == 0)
                            state = 1;
                    }
                }
            }
            Snapshot(accepted);
        }
        return trace.ToArray();
    }
}
