using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public bool HasDirectedRoute(int nodeCount, int[][] edges, int start, int target)
    {
        if (start == target)
            return true;
        var adjacent = new List<int>[nodeCount];
        for (int i = 0; i < nodeCount; ++i)
            adjacent[i] = new List<int>();
        foreach (var edge in edges)
            adjacent[edge[0]].Add(edge[1]);
        bool[] visited = new bool[nodeCount];
        var queue = new List<int> { start };
        visited[start] = true;
        for (int head = 0; head < queue.Count; ++head)
            foreach (int neighbor in adjacent[queue[head]])
                if (!visited[neighbor])
                {
                    if (neighbor == target)
                        return true;
                    visited[neighbor] = true;
                    queue.Add(neighbor);
                }
        return false;
    }
}
