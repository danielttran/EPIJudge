using System;
using System.Collections.Generic;
using System.Text;
public sealed class BankError : Exception { public string Code { get; } public BankError(string code) : base(code) { Code=code; } }
public class ThreeStacks
{
    private readonly int capacity;
    private readonly int[] values;
    private readonly int[] sizes = new int[3];
    private void Check(int stack)
    {
        if (stack < 0 || stack >= 3)
            throw new BankError("index");
    }
    public ThreeStacks(int supplied)
    {
        if (supplied < 1 || supplied > 256)
            throw new BankError("capacity");
        capacity = supplied;
        values = new int[3 * supplied];
    }
    public void Push(int stack, int value)
    {
        Check(stack);
        if (sizes[stack] == capacity)
            throw new BankError("full");
        values[stack * capacity + sizes[stack]] = value;
        ++sizes[stack];
    }
    public int Pop(int stack)
    {
        Check(stack);
        if (sizes[stack] == 0)
            throw new BankError("empty");
        --sizes[stack];
        return values[stack * capacity + sizes[stack]];
    }
    public int Peek(int stack)
    {
        Check(stack);
        if (sizes[stack] == 0)
            throw new BankError("empty");
        return values[stack * capacity + sizes[stack] - 1];
    }
    public bool IsEmpty(int stack)
    {
        Check(stack);
        return sizes[stack] == 0;
    }
    public bool IsFull(int stack)
    {
        Check(stack);
        return sizes[stack] == capacity;
    }
}
