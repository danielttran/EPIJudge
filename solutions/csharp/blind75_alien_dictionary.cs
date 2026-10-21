using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public string AlienOrder(string[] words)
    {
        var graph = new Dictionary<char, HashSet<char>>();
        foreach (char c in string.Concat(words))
            graph.TryAdd(c, []);
        for (int i = 1; i < words.Length; i++)
        {
            string a = words[i - 1], b = words[i];
            int j = 0;
            while (j < Math.Min(a.Length, b.Length) && a[j] == b[j])
                j++;
            if (j == Math.Min(a.Length, b.Length))
            {
                if (a.Length > b.Length)
                    return "";
            }
            else
                graph[a[j]].Add(b[j]);
        }
        var degree = graph.Keys.ToDictionary(c => c, _ => 0);
        foreach (var row in graph.Values)
        foreach (char c in row)
            degree[c]++;
        var ready = new SortedSet<char>(degree.Where(p => p.Value == 0).Select(p => p.Key));
        var outp = new List<char>();
        while (ready.Count > 0)
        {
            char c = ready.Min;
            ready.Remove(c);
            outp.Add(c);
            foreach (char next in graph[c])
            if (--degree[next] == 0)
                ready.Add(next);
        }
        return outp.Count == graph.Count ? new string(outp.ToArray()) : "";
    }
}

// Shared node types from the supplied starter.
public class ListNode
{
    public int val;
    public ListNode? next;
    public ListNode(int val = 0, ListNode? next = null)
    {
        this.val = val;
        this.next = next;
    }
}
public class TreeNode
{
    public int val;
    public TreeNode? left, right;
    public TreeNode(int val = 0, TreeNode? left = null, TreeNode? right = null)
    {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
public class Node
{
    public int val;
    public List<Node> neighbors = new();
    public Node(int val = 0)
    {
        this.val = val;
    }
}
