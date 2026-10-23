using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> LangtonBoard(int steps)
    {
        int width = 2 * steps + 1, row = 0, column = 0, direction = 0, minRow = 0, maxRow = 0,
            minColumn = 0, maxColumn = 0;
        var black = new HashSet<int>();
        int[] dr = { 0, 1, 0, -1 }, dc = { 1, 0, -1, 0 };
        for (int turn = 0; turn < steps; ++turn)
        {
            int key = (row + steps) * width + column + steps;
            if (black.Contains(key))
            {
                direction = (direction + 3) % 4;
                black.Remove(key);
            }
            else
            {
                direction = (direction + 1) % 4;
                black.Add(key);
            }
            row += dr[direction];
            column += dc[direction];
            minRow = Math.Min(minRow, row);
            maxRow = Math.Max(maxRow, row);
            minColumn = Math.Min(minColumn, column);
            maxColumn = Math.Max(maxColumn, column);
        }
        var result = new List<string>();
        for (int r = minRow; r <= maxRow; ++r)
        {
            var line = new StringBuilder();
            for (int c = minColumn; c <= maxColumn; ++c)
                line.Append(r == row && c == column                           ? "RDLU"[direction]
                            : black.Contains((r + steps) * width + c + steps) ? '#'
                                                                              : '.');
            result.Add(line.ToString());
        }
        return result;
    }
}
