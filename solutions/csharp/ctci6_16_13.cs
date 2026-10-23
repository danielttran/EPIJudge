using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public double[] BisectSquares(int[][] squares)
    {
        double x = squares[0][0] + squares[0][2] / 2.0, y = squares[0][1] + squares[0][2] / 2.0,
               dx = squares[1][0] + squares[1][2] / 2.0 - x,
               dy = squares[1][1] + squares[1][2] / 2.0 - y, other = 1;
        if (dx == 0 && dy == 0)
        {
            dy = 1;
            other = 0;
        }
        double scale = Math.Max(Math.Abs(dx), Math.Abs(dy)), first = squares[0][2] / (2.0 * scale),
               second = squares[1][2] / (2.0 * scale), start = Math.Min(-first, other - second),
               end = Math.Max(first, other + second);
        return [x + start * dx, y + start * dy, x + end * dx, y + end * dy];
    }
}
