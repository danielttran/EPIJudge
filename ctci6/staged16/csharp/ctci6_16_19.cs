using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] PondSizes(int[][] land)
    {
        int rows = land.Length, columns = rows == 0 ? 0 : land[0].Length;
        bool[,] seen = new bool[rows, columns];
        var sizes = new List<int>();
        for (int row = 0; row < rows; ++row)
        {
            for (int column = 0; column < columns; ++column)
            {
                if (land[row][column] != 0 || seen[row, column])
                    continue;
                seen[row, column] = true;
                var work = new Stack<(int, int)>();
                work.Push((row, column));
                int size = 0;
                while (work.Count > 0)
                {
                    var (r, c) = work.Pop();
                    ++size;
                    for (int dr = -1; dr <= 1; ++dr)
                    {
                        for (int dc = -1; dc <= 1; ++dc)
                        {
                            if (dr == 0 && dc == 0)
                                continue;
                            int nr = r + dr, nc = c + dc;
                            if (nr >= 0 && nr < rows && nc >= 0 && nc < columns &&
                                land[nr][nc] == 0 && !seen[nr, nc])
                            {
                                seen[nr, nc] = true;
                                work.Push((nr, nc));
                            }
                        }
                    }
                }
                sizes.Add(size);
            }
        }
        sizes.Sort();
        return sizes.ToArray();
    }
}
