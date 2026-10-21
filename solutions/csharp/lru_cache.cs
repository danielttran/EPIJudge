using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    private int limit;
    private readonly LinkedList<(int Key, int Price)> order = new();
    private readonly Dictionary<int, LinkedListNode<(int Key, int Price)>> entries = new();
    public void Initialize(int capacity)
    {
        limit = capacity;
        entries.Clear();
        order.Clear();
    }
    public int Lookup(int isbn)
    {
        if (!entries.TryGetValue(isbn, out var node))
            return -1;
        order.Remove(node);
        order.AddFirst(node);
        return node.Value.Price;
    }
    public void Insert(int isbn, int price)
    {
        if (entries.TryGetValue(isbn, out var existing))
        {
            order.Remove(existing);
            order.AddFirst(existing);
            return;
        }
        if (limit <= 0)
            return;
        if (entries.Count == limit)
        {
            var last = order.Last!;
            entries.Remove(last.Value.Key);
            order.RemoveLast();
        }
        entries[isbn] = order.AddFirst((isbn, price));
    }
    public bool Erase(int isbn)
    {
        if (!entries.Remove(isbn, out var node))
            return false;
        order.Remove(node);
        return true;
    }
}
