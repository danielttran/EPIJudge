using System;
using System.Collections.Generic;
using System.Text;
public sealed class BankError : Exception { public string Code { get; } public BankError(string code) : base(code) { Code=code; } }
public class TwoStackQueue
{
    private readonly Stack<int> newest = new(), oldest = new();
    private void Shift()
    {
        if (oldest.Count == 0)
        {
            while (!(newest.Count == 0))
            {
                oldest.Push(newest.Pop());
            }
        }
    }
    public TwoStackQueue()
    {
    }
    public void Add(int value)
    {
        newest.Push(value);
    }
    public int Remove()
    {
        Shift();
        if (oldest.Count == 0)
            throw new BankError("empty");
        return oldest.Pop();
    }
    public int Peek()
    {
        Shift();
        if (oldest.Count == 0)
            throw new BankError("empty");
        return oldest.Peek();
    }
    public int Size()
    {
        return newest.Count + oldest.Count;
    }
}
