using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<List<int>> EightQueens()
    {
        int[] board = new int[8];
        var result = new List<List<int>>();
        void Visit(int row, int usedColumns, int usedDown, int usedUp)
        {
            if (row == 8)
            {
                result.Add(new List<int>(board));
                return;
            }
            for (int column = 0; column < 8; ++column)
            {
                int colBit = 1 << column, downBit = 1 << (row - column + 7),
                    upBit = 1 << (row + column);
                if ((usedColumns & colBit) != 0 || (usedDown & downBit) != 0 ||
                    (usedUp & upBit) != 0)
                    continue;
                board[row] = column;
                Visit(row + 1, usedColumns | colBit, usedDown | downBit, usedUp | upBit);
            }
        }
        Visit(0, 0, 0, 0);
        return result;
    }
}
