using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] PlayOthello(int size, int[][] actions)
    {
        var board = Enumerable.Range(0, size)
                        .Select(
                            _ => new int[size])
                        .ToArray();
        var trace = new List<int[]>();
        int middle = size / 2;
        board[middle - 1][middle - 1] = board[middle][middle] = 2;
        board[middle - 1][middle] = board[middle][middle - 1] = 1;
        List<int[]> Captures(int row, int column, int color)
        {
            var result = new List<int[]>();
            if (row < 0 || row >= size || column < 0 || column >= size || board[row][column] != 0)
                return result;
            for (int dr = -1; dr <= 1; ++dr)
                for (int dc = -1; dc <= 1; ++dc)
                {
                    if (dr == 0 && dc == 0)
                        continue;
                    int r = row + dr, c = column + dc;
                    var path = new List<int[]>();
                    while (r >= 0 && r < size && c >= 0 && c < size && board[r][c] == 3 - color)
                    {
                        path.Add(new int[] { r, c });
                        r += dr;
                        c += dc;
                    }
                    if (path.Count > 0 && r >= 0 && r < size && c >= 0 && c < size &&
                        board[r][c] == color)
                        result.AddRange(path);
                }
            return result;
        }
        bool CanMove(int color)
        {
            for (int r = 0; r < size; ++r)
                for (int c = 0; c < size; ++c)
                    if (Captures(r, c, color).Count > 0)
                        return true;
            return false;
        }
        int turn = CanMove(1) ? 1 : 0;
        void Snapshot(int accepted)
        {
            int black = 0, white = 0;
            foreach (var row in board)
                foreach (int v in row)
                {
                    if (v == 1)
                        black++;
                    if (v == 2)
                        white++;
                }
            var result = new int[4 + size * size];
            result[0] = turn;
            result[1] = accepted;
            result[2] = black;
            result[3] = white;
            for (int r = 0; r < size; r++)
                for (int c = 0; c < size; c++)
                    result[4 + r * size + c] = board[r][c];
            trace.Add(result);
        }
        Snapshot(0);
        foreach (var action in actions)
        {
            int row = action[0], column = action[1], color = action[2], accepted = 0;
            if (turn != 0 && color == turn)
            {
                var flipped = Captures(row, column, color);
                if (flipped.Count > 0)
                {
                    board[row][column] = color;
                    foreach (var p in flipped)
                        board[p[0]][p[1]] = color;
                    accepted = 1;
                    turn = CanMove(3 - color) ? 3 - color : CanMove(color) ? color : 0;
                }
            }
            Snapshot(accepted);
        }
        return trace.ToArray();
    }
}
