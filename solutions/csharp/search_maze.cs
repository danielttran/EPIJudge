using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<(int Row, int Column)> SearchMaze(List<List<int>> maze, (int Row, int Column) start, (int Row, int Column) end)
    {
        bool White((int Row, int Column) p) => p.Row >= 0 && p.Row < maze.Count && p.Column >= 0 && p.Column < maze[p.Row].Count && maze[p.Row][p.Column] == 0;
        if (!White(start) || !White(end))
            return new();
        var previous = new Dictionary<(int Row, int Column), (int Row, int Column)> { [start] = start };
        var pending = new Queue<(int Row, int Column)>();
        pending.Enqueue(start);
        (int Row, int Column)[] steps = [(1, 0), (-1, 0), (0, 1), (0, -1)];
        while (pending.TryDequeue(out var cell))
        {
            if (cell == end)
            {
                var path = new List<(int Row, int Column)>();
                for (var p = end; ; p = previous[p])
                {
                    path.Add(p);
                    if (p == start)
                        break;
                }
                path.Reverse();
                return path;
            }
            foreach (var step in steps)
            {
                var neighbor = (Row: cell.Row + step.Row, Column: cell.Column + step.Column);
                if (White(neighbor) && previous.TryAdd(neighbor, cell))
                    pending.Enqueue(neighbor);
            }
        }
        return new();
    }
}
