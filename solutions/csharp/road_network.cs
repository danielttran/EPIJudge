using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public (int, int, int) FindBestProposals(List<(int, int, int)> H, List<(int, int, int)> P, int n)
    {
        if (P.Count == 0)
            return (-1, -1, 0);
        const long infinity = long.MaxValue / 4;
        var distance = new long[n, n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                distance[i, j] = i == j ? 0 : infinity;
        foreach (var (a, b, length) in H)
        {
            distance[a, b] = Math.Min(distance[a, b], length);
            distance[b, a] = Math.Min(distance[b, a], length);
        }
        for (int via = 0; via < n; via++)
            for (int from = 0; from < n; from++)
                for (int to = 0; to < n; to++)
                    distance[from, to] = Math.Min(distance[from, to], distance[from, via] + distance[via, to]);
        long bestSaving = -1;
        var best = P[0];
        foreach (var proposal in P)
        {
            var (a, b, length) = proposal;
            long saving = 0;
            for (int from = 0; from < n; from++)
                for (int to = from + 1; to < n; to++)
                {
                    long viaEdge = Math.Min(distance[from, a] + length + distance[b, to],
                                            distance[from, b] + length + distance[a, to]);
                    saving += distance[from, to] - Math.Min(distance[from, to], viaEdge);
                }
            if (saving > bestSaving)
            {
                bestSaving = saving;
                best = proposal;
            }
        }
        return best;
    }
}
