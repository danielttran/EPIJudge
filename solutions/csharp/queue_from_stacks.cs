using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private readonly Stack<int> incoming = new();
    private readonly Stack<int> outgoing = new();
    public void Initialize()
    {
        incoming.Clear();
        outgoing.Clear();
    }
    public void Enqueue(int value) => incoming.Push(value);
    public int Dequeue()
    {
        if (outgoing.Count == 0)
            while (incoming.Count != 0)
                outgoing.Push(incoming.Pop());
        return outgoing.Pop();
    }
}
