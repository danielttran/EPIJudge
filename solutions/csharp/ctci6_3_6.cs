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
public class AnimalShelter
{
    private sealed class Entry
    {
        public Animal Value;
        public int Order;
        public Entry? Next;
        public Entry(Animal value, int order)
        {
            Value = value;
            Order = order;
        }
    }
    private readonly Entry?[] heads = new Entry?[2], tails = new Entry?[2];
    private int order = 0, count = 0;
    private int Oldest()
    {
        if (heads[0] == null)
            return 1;
        if (heads[1] == null)
            return 0;
        return heads[0]!.Order < heads[1]!.Order ? 0 : 1;
    }
    private Animal? Take(int slot)
    {
        var entry = heads[slot];
        if (entry == null)
            return null;
        heads[slot] = entry.Next;
        if (heads[slot] == null)
            tails[slot] = null;
        --count;
        return entry.Value;
    }

    public AnimalShelter()
    {
    }
    public void Enqueue(Animal animal)
    {
        int slot;
        if (animal.Species == "dog")
            slot = 0;
        else if (animal.Species == "cat")
            slot = 1;
        else
            throw new BankError("species");
        var entry = new Entry(animal, order++);
        if (tails[slot] == null)
            heads[slot] = entry;
        else
            tails[slot]!.Next = entry;
        tails[slot] = entry;
        ++count;
    }
    public Animal? DequeueAny()
    {
        return Take(Oldest());
    }
    public Animal? DequeueDog()
    {
        return Take(0);
    }
    public Animal? DequeueCat()
    {
        return Take(1);
    }
    public Animal? Peek()
    {
        return heads[Oldest()]?.Value;
    }
    public int Size()
    {
        return count;
    }
}
