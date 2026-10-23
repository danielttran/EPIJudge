using System;
using System.Collections.Generic;
using System.Text;
public sealed class BankError : Exception { public string Code { get; } public BankError(string code) : base(code) { Code=code; } }
public sealed class IntStack {
private readonly Stack<int> values = new();
public void Push(int value) { values.Push(value); }
public int Pop() { if (values.Count==0) throw new BankError("empty"); return values.Pop(); }
public int Peek() { if (values.Count==0) throw new BankError("empty"); return values.Peek(); }
public bool IsEmpty() { return values.Count==0; }
}
public sealed class Animal { public int Id { get; } public string Species { get; } public Animal(int id,string species) { Id=id; Species=species; } }
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
