using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool IsDeadlocked(int num_nodes, List<(int, int)> edges)
    {
        var graph = Enumerable.Range(0, num_nodes).Select(_ => new List<int>()).ToArray();
        var indegree = new int[num_nodes];
        foreach (var (from, to) in edges)
        {
            graph[from].Add(to);
            indegree[to]++;
        }
        var ready = new Queue<int>(Enumerable.Range(0, num_nodes).Where(v => indegree[v] == 0));
        int removed = 0;
        while (ready.TryDequeue(out int vertex))
        {
            removed++;
            foreach (int neighbor in graph[vertex])
            if (--indegree[neighbor] == 0)
                ready.Enqueue(neighbor);
        }
        return removed != num_nodes;
    }
}
