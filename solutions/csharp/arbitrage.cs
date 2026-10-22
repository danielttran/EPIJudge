using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool IsArbitrageExist(List<List<double>> graph)
    {
        int n = graph.Count;
        if (n == 0) return false;
        var distances = new double[n];
        for (int pass = 0; pass < n; pass++)
        {
            bool changed = false;
            for (int from = 0; from < n; from++)
                for (int to = 0; to < n; to++)
                {
                    double candidate = distances[from] - Math.Log(graph[from][to]);
                    if (candidate < distances[to] - 1e-12)
                    {
                        distances[to] = candidate;
                        changed = true;
                    }
                }
            if (!changed)
                return false;
        }
        return true;
    }
}
