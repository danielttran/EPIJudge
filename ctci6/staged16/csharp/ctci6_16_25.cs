using System;
using System.Collections.Generic;
using System.Text;
public class LRUCache
{
    private readonly int capacity;
    private readonly LinkedList<(int Key, string Text)> order = new();
    private readonly Dictionary<int, LinkedListNode<(int Key, string Text)>> index = new();
    public LRUCache(int capacity)
    {
        this.capacity = capacity;
    }
    public string? Get(int key)
    {
        if (!index.TryGetValue(key, out var node))
            return null;
        order.Remove(node);
        order.AddLast(node);
        return node.Value.Text;
    }
    public void Set(int key, string value)
    {
        if (index.TryGetValue(key, out var node))
        {
            node.Value = (key, value);
            order.Remove(node);
            order.AddLast(node);
        }
        else
        {
            index[key] = order.AddLast((key, value));
            if (index.Count > capacity)
            {
                var oldest = order.First!;
                order.RemoveFirst();
                index.Remove(oldest.Value.Key);
            }
        }
    }
}
