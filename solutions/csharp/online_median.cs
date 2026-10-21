using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<double> OnlineMedian(List<int> sequence)
    {
        var lower = new PriorityQueue<int, long>();
        var upper = new PriorityQueue<int, int>();
        var result = new List<double>();
        foreach (int value in sequence)
        {
            if (lower.Count == 0 || value <= lower.Peek())
                lower.Enqueue(value, -(long)value);
            else
                upper.Enqueue(value, value);
            if (lower.Count > upper.Count + 1)
            {
                int moved = lower.Dequeue();
                upper.Enqueue(moved, moved);
            }
            if (upper.Count > lower.Count)
            {
                int moved = upper.Dequeue();
                lower.Enqueue(moved, -(long)moved);
            }
            result.Add(lower.Count == upper.Count ? (lower.Peek() + (double)upper.Peek()) / 2 : lower.Peek());
        }
        return result;
    }
}
