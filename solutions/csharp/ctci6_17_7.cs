using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[][] TrueNameFrequencies(string[] names, int[] frequencies, int[][] synonyms)
    {
        int n = names.Length;
        var adjacent = new List<int>[n];
        for (int i = 0; i < n; ++i)
            adjacent[i] = new List<int>();
        foreach (var edge in synonyms)
        {
            adjacent[edge[0]].Add(edge[1]);
            adjacent[edge[1]].Add(edge[0]);
        }
        bool[] visited = new bool[n];
        var result = new List<int[]>();
        for (int start = 0; start < n; ++start)
        {
            if (visited[start])
                continue;
            visited[start] = true;
            var queue = new List<int> { start };
            int total = 0;
            for (int head = 0; head < queue.Count; ++head)
            {
                int name = queue[head];
                total += frequencies[name];
                foreach (int other in adjacent[name])
                    if (!visited[other])
                    {
                        visited[other] = true;
                        queue.Add(other);
                    }
            }
            result.Add([start, total]);
        }
        return result.ToArray();
    }
}
