using System;
using System.Collections.Generic;
using System.Text;
public class HashTable<K, V>
    where K : notnull
{
    private sealed class Node(K key, V value, Node? next)
    {
        public readonly K Key = key;
        public V Value = value;
        public Node? Next = next;
    }
    private readonly Node?[] buckets;
    public HashTable(int capacity)
    {
        buckets = new Node?[capacity];
    }
    private int Index(K key) => (int)((uint)EqualityComparer<K>.Default.GetHashCode(key) %
                                      (uint)buckets.Length);
    private Node? Find(K key)
    {
        for (var node = buckets[Index(key)]; node is not null; node = node.Next)
            if (EqualityComparer<K>.Default.Equals(node.Key, key))
                return node;
        return null;
    }
    public void Put(K key, V value)
    {
        var node = Find(key);
        if (node is not null)
        {
            node.Value = value;
            return;
        }
        int index = Index(key);
        buckets[index] = new Node(key, value, buckets[index]);
    }
    public V Get(K key)
    {
        var node = Find(key);
        if (node is null)
            throw new KeyNotFoundException();
        return node.Value;
    }
    public bool Contains(K key) => Find(key) is not null;
    public bool Remove(K key)
    {
        int index = Index(key);
        Node? previous = null;
        var node = buckets[index];
        while (node is not null)
        {
            if (EqualityComparer<K>.Default.Equals(node.Key, key))
            {
                if (previous is null)
                    buckets[index] = node.Next;
                else
                    previous.Next = node.Next;
                return true;
            }
            previous = node;
            node = node.Next;
        }
        return false;
    }
}
