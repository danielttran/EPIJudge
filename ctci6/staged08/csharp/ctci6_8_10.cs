using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] PaintFill(int[][] screen, int row, int column, int newColor)
    {
        int rows = screen.Length, columns = rows == 0 ? 0 : screen[0].Length;
        if (row < 0 || row >= rows || column < 0 || column >= columns)
            return screen;
        int oldColor = screen[row][column];
        if (oldColor == newColor)
            return screen;
        var work = new Stack<(int, int)>();
        work.Push((row, column));
        screen[row][column] = newColor;
        int[] dr = { -1, 1, 0, 0 }, dc = { 0, 0, -1, 1 };
        while (work.Count > 0)
        {
            var (r, c) = work.Pop();
            for (int i = 0; i < 4; ++i)
            {
                int nr = r + dr[i], nc = c + dc[i];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && screen[nr][nc] == oldColor)
                {
                    screen[nr][nc] = newColor;
                    work.Push((nr, nc));
                }
            }
        }
        return screen;
    }
}
