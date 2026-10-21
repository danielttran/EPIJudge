using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private readonly Queue<int> values = new();
    private readonly LinkedList<int> candidates = new();
    public void Initialize()
    {
        values.Clear();
        candidates.Clear();
    }
    public void Enqueue(int value)
    {
        values.Enqueue(value);
        while (candidates.Last is not null && candidates.Last.Value < value)
            candidates.RemoveLast();
        candidates.AddLast(value);
    }
    public int Dequeue()
    {
        int value = values.Dequeue();
        if (candidates.First!.Value == value)
            candidates.RemoveFirst();
        return value;
    }
    public int Max() => candidates.First!.Value;
}
