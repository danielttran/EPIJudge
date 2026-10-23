using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] SmallestK(int[] values, int k)
    {
        if (k == 0)
            return [];
        var heap = new PriorityQueue<int, int>(Comparer<int>.Create((a, b) => b.CompareTo(a)));
        for (int i = 0; i < k; ++i)
            heap.Enqueue(values[i], values[i]);
        for (int i = k; i < values.Length; ++i)
        {
            if (values[i] < heap.Peek())
            {
                heap.Dequeue();
                heap.Enqueue(values[i], values[i]);
            }
        }
        int[] result = new int[k];
        for (int i = k - 1; i >= 0; --i)
            result[i] = heap.Dequeue();
        return result;
    }
}
