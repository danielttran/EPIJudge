using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> SortApproximatelySortedArray(List<int> sequence, int k)
    {
        var heap = new PriorityQueue<int, int>();
        var output = new List<int>(sequence.Count);
        foreach (int value in sequence)
        {
            heap.Enqueue(value, value);
            if (heap.Count > k)
                output.Add(heap.Dequeue());
        }
        while (heap.TryDequeue(out int value, out _))
            output.Add(value);
        return output;
    }
}
