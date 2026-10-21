using System;
using System.Collections.Generic;
using System.Linq;
public class Trie
{
    private sealed class Branch
    {
        public readonly Dictionary<char, Branch> Children = new();
    public bool Terminal;
    }
    private readonly Branch root = new();
    private Branch? Follow(string text)
    {
        var node = root;
        foreach (char c in text)
        {
            if (!node.Children.TryGetValue(c, out var next))
                return null;
            node = next;
        }
        return node;
    }
    public void Insert(string word)
    {
        var node = root;
        foreach (char c in word)
        {
            if (!node.Children.TryGetValue(c, out var next))
            {
                next = new Branch();
                node.Children[c] = next;
            }
            node = next;
        }
        node.Terminal = true;
    }
    public bool Search(string word) => Follow(word)?.Terminal == true;
    public bool StartsWith(string prefix) => (root.Terminal || root.Children.Count > 0) && Follow(prefix) is not null;
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
