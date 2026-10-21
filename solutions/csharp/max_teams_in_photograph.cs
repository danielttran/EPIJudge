using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindLargestNumberTeams(int k, List<(int, int)> edges)
    {
        var outgoing = Enumerable.Range(0, k).Select(_ => new List<int>()).ToArray();
        int[] incoming = new int[k], length = Enumerable.Repeat(1, k).ToArray();
        foreach (var (from, to) in edges)
        {
            outgoing[from].Add(to);
            incoming[to]++;
        }
        var ready = new Queue<int>();
        for (int i = 0; i < k; i++)
        if (incoming[i] == 0)
            ready.Enqueue(i);
        int best = 0;
        while (ready.TryDequeue(out int team))
        {
            best = Math.Max(best, length[team]);
            foreach (int next in outgoing[team])
            {
                length[next] = Math.Max(length[next], length[team] + 1);
                if (--incoming[next] == 0)
                    ready.Enqueue(next);
            }
        }
        return best;
    }
}
