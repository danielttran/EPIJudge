using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] SolveJigsaw(int size, int[][] pieces)
    {
        int count = pieces.Length;
        var placed = Enumerable.Range(0, count)
                         .Select(
                             _ => new int[2])
                         .ToArray();
        var used = new bool[count];
        int Edge(int index, int turn, int side) => pieces[index][(side - turn + 4) % 4];
        bool Search(int position)
        {
            if (position == count)
                return true;
            int row = position / size, column = position % size;
            for (int index = 0; index < count; ++index)
            {
                if (used[index])
                    continue;
                for (int turn = 0; turn < 4; ++turn)
                {
                    int[] values = new int[4];
                    bool[] bounds = { row == 0, column == size - 1, row == size - 1, column == 0 };
                    bool fits = true;
                    for (int side = 0; side < 4; ++side)
                    {
                        values[side] = Edge(index, turn, side);
                        if ((values[side] == 0) != bounds[side])
                            fits = false;
                    }
                    if (!fits)
                        continue;
                    if (row > 0 && values[0] != -Edge(placed[position - size][0],
                                                      placed[position - size][1], 2))
                        continue;
                    if (column > 0 &&
                        values[3] != -Edge(placed[position - 1][0], placed[position - 1][1], 1))
                        continue;
                    used[index] = true;
                    placed[position][0] = index;
                    placed[position][1] = turn;
                    if (Search(position + 1))
                        return true;
                    used[index] = false;
                }
            }
            return false;
        }
        return Search(0) ? placed : Array.Empty<int[]>();
    }
}
