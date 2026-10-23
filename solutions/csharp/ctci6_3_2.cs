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
public class MinStack
{
    private sealed class Entry
    {
        public int Value, Minimum;
        public Entry? Next;
        public Entry(int value, int minimum, Entry? next)
        {
            Value = value;
            Minimum = minimum;
            Next = next;
        }
    }
    private Entry? top;

    public MinStack()
    {
    }
    public void Push(int value)
    {
        int minimum = top == null ? value : Math.Min(value, top.Minimum);
        top = new Entry(value, minimum, top);
    }
    public int Pop()
    {
        if (top == null)
            throw new BankError("empty");
        int value = top.Value;
        top = top.Next;
        return value;
    }
    public int Peek()
    {
        if (top == null)
            throw new BankError("empty");
        return top.Value;
    }
    public int GetMin()
    {
        if (top == null)
            throw new BankError("empty");
        return top.Minimum;
    }
    public bool IsEmpty()
    {
        return top == null;
    }
}
