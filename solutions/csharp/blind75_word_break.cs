using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool WordBreak(string s, string[] wordDict)
    {
        var possible = new bool[s.Length + 1];
        possible[0] = true;
        for (int i = 0; i < s.Length; i++)
        if (possible[i])
        foreach (string w in wordDict)
        if (i + w.Length <= s.Length && s.AsSpan(i, w.Length).SequenceEqual(w))
            possible[i + w.Length] = true;
        return possible[^1];
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
