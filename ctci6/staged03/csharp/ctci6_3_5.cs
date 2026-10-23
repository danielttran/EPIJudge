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
public class Solution
{
    public void SortStack(IntStack stack)
    {
        var spare = new IntStack();
        while (!stack.IsEmpty())
        {
            int value = stack.Pop();
            while (!spare.IsEmpty() && spare.Peek() > value)
                stack.Push(spare.Pop());
            spare.Push(value);
        }
        while (!spare.IsEmpty())
            stack.Push(spare.Pop());
    }
}
