using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private int[] buffer = new int[1];
    private int head, count;

    public void Initialize(int capacity)
    {
        buffer = new int[Math.Max(1, capacity)];
        head = count = 0;
    }

    public void Enqueue(int value)
    {
        if (count == buffer.Length)
        {
            var larger = new int[buffer.Length * 2];
            for (int i = 0; i < count; i++)
                larger[i] = buffer[(head + i) % buffer.Length];
            buffer = larger;
            head = 0;
        }
        buffer[(head + count) % buffer.Length] = value;
        count++;
    }

    public int Dequeue()
    {
        if (count == 0)
            throw new InvalidOperationException("The queue is empty.");
        int value = buffer[head];
        head = (head + 1) % buffer.Length;
        count--;
        return value;
    }

    public int Size() => count;
}
