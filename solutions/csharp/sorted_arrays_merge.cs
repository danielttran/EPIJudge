using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> MergeSortedArrays(List<List<int>> sorted_arrays)
    {
        var heap = new PriorityQueue<(int Array, int Position), int>();
        for (int i = 0; i < sorted_arrays.Count; i++)
            if (sorted_arrays[i].Count > 0)
                heap.Enqueue((i, 0), sorted_arrays[i][0]);
        var result = new List<int>();
        while (heap.TryDequeue(out var entry, out int value))
        {
            result.Add(value);
            int next = entry.Position + 1;
            if (next < sorted_arrays[entry.Array].Count)
                heap.Enqueue((entry.Array, next), sorted_arrays[entry.Array][next]);
        }
        return result;
    }
}
