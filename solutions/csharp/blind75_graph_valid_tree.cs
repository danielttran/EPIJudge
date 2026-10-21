using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool ValidTree(int n, int[][] edges)
    {
        if (n == 0 || edges.Length != n - 1)
            return false;
        var parent = Enumerable.Range(0, n).ToArray();
        int Find(int v)
        {
            while (v != parent[v])
            {
                parent[v] = parent[parent[v]];
                v = parent[v];
            }
            return v;
        }
        int count = n;
        foreach (var e in edges)
        {
            int a = Find(e[0]), b = Find(e[1]);
            if (a != b)
            {
                parent[a] = b;
                count--;
            }
        }
        return count == 1;
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
