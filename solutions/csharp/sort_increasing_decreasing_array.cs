using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> SortKIncreasingDecreasingArray(List<int> A)
    {
        var runs = new List<List<int>>();
        int start = 0;
        while (start < A.Count)
        {
            int end = start + 1;
            bool increasing = end == A.Count || A[end] >= A[start];
            while (end < A.Count && (increasing ? A[end] >= A[end - 1] : A[end] <= A[end - 1]))
                end++;
            var run = A.GetRange(start, end - start);
            if (!increasing)
                run.Reverse();
            runs.Add(run);
            start = end;
        }
        var heap = new PriorityQueue<(int Run, int Position), int>();
        for (int i = 0; i < runs.Count; i++)
            heap.Enqueue((i, 0), runs[i][0]);
        var result = new List<int>(A.Count);
        while (heap.TryDequeue(out var entry, out int value))
        {
            result.Add(value);
            int next = entry.Position + 1;
            if (next < runs[entry.Run].Count)
                heap.Enqueue((entry.Run, next), runs[entry.Run][next]);
        }
        return result;
    }
}
