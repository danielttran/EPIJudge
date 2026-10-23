using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public void DrawHorizontalLine(byte[] screen, int width, int x1, int x2, int y)
    {
        int first = x1 / 8, last = x2 / 8, row = y * (width / 8);
        for (int cell = first; cell <= last; ++cell)
        {
            int start = cell == first ? x1 % 8 : 0, end = cell == last ? x2 % 8 : 7,
                mask = (255 >> start) & ((255 << (7 - end)) & 255);
            screen[row + cell] = (byte)(screen[row + cell] | mask);
        }
    }
}
