using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindClosestElementsInSortedArrays(List<List<int>> sorted_arrays)
    {
        if (sorted_arrays.Count == 0)
            return 0;
        var minima = new PriorityQueue<(int Array, int Index), int>();
        int maximum = int.MinValue;
        for (int i = 0; i < sorted_arrays.Count; i++)
        {
            int value = sorted_arrays[i][0];
            minima.Enqueue((i, 0), value);
            maximum = Math.Max(maximum, value);
        }
        long best = long.MaxValue;
        while (minima.TryDequeue(out var entry, out int minimum))
        {
            best = Math.Min(best, (long)maximum - minimum);
            int next = entry.Index + 1;
            if (next == sorted_arrays[entry.Array].Count)
                break;
            int value = sorted_arrays[entry.Array][next];
            maximum = Math.Max(maximum, value);
            minima.Enqueue((entry.Array, next), value);
        }
        return (int)best;
    }
}
