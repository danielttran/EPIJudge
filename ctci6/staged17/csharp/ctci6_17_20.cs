using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public double[] ContinuousMedians(int[] values)
    {
        var lower = new PriorityQueue<int, long>();
        var upper = new PriorityQueue<int, long>();
        var medians = new double[values.Length];
        for (int i = 0; i < values.Length; ++i)
        {
            int value = values[i];
            if (lower.Count == 0 || value <= lower.Peek())
                lower.Enqueue(value, -(long)value);
            else
                upper.Enqueue(value, value);
            if (lower.Count > upper.Count + 1)
            {
                int moved = lower.Dequeue();
                upper.Enqueue(moved, moved);
            }
            else if (upper.Count > lower.Count)
            {
                int moved = upper.Dequeue();
                lower.Enqueue(moved, -(long)moved);
            }
            medians[i] = lower.Count > upper.Count ? lower.Peek()
                                                   : ((double)lower.Peek() + upper.Peek()) / 2.0;
        }
        return medians;
    }
}
