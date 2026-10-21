using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private readonly Stack<(int Value, int Maximum)> entries = new();
    public void Initialize() => entries.Clear();
    public void Push(int value) => entries.Push((value, entries.Count == 0 ? value : Math.Max(value, entries.Peek().Maximum)));
    public int Pop() => entries.Pop().Value;
    public bool Empty() => entries.Count == 0;
    public int Max() => entries.Peek().Maximum;
}
