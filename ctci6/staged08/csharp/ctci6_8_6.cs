using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<List<int>> SolveHanoi(int disks)
    {
        var towers = new Stack<int>[] { new(), new(), new() };
        for (int disk = disks; disk >= 1; --disk)
            towers[0].Push(disk);
        var moves = new List<List<int>>();
        void Transfer(int count, int source, int buffer, int destination)
        {
            if (count == 0)
                return;
            Transfer(count - 1, source, destination, buffer);
            int disk = towers[source].Pop();
            towers[destination].Push(disk);
            moves.Add([disk, source, destination]);
            Transfer(count - 1, buffer, source, destination);
        }
        Transfer(disks, 0, 1, 2);
        return moves;
    }
}
