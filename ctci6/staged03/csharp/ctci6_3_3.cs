using System;
using System.Collections.Generic;
using System.Text;
public sealed class BankError : Exception { public string Code { get; } public BankError(string code) : base(code) { Code=code; } }
public class SetOfStacks
{
    private readonly int capacity;
    private readonly List<List<int>> stacks = new();
    public SetOfStacks(int supplied)
    {
        if (supplied < 1 || supplied > 256)
            throw new BankError("capacity");
        capacity = supplied;
    }
    public void Push(int value)
    {
        int last = stacks.Count - 1;
        if (last < 0 || stacks[last].Count == capacity)
        {
            stacks.Add(new List<int>());
            ++last;
        }
        stacks[last].Add(value);
    }
    public int Pop()
    {
        if (stacks.Count == 0)
            throw new BankError("empty");
        int last = stacks.Count - 1;
        int value = stacks[last][stacks[last].Count - 1];
        stacks[last].RemoveAt(stacks[last].Count - 1);
        if (stacks[last].Count == 0)
        {
            stacks.RemoveAt(last);
        }
        return value;
    }
    public int PopAt(int index)
    {
        if (index < 0 || index >= stacks.Count)
            throw new BankError("index");
        int value = stacks[index][stacks[index].Count - 1];
        stacks[index].RemoveAt(stacks[index].Count - 1);
        for (int i = index; i + 1 < stacks.Count; ++i)
        {
            int bottom = stacks[i + 1][0];
            stacks[i + 1].RemoveAt(0);
            stacks[i].Add(bottom);
        }
        int last = stacks.Count - 1;
        if (stacks[last].Count == 0)
        {
            stacks.RemoveAt(last);
        }
        return value;
    }
    public bool IsEmpty()
    {
        return stacks.Count == 0;
    }
}
