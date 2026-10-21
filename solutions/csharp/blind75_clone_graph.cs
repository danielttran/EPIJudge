using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public Node? CloneGraph(Node? node)
    {
        return Algorithms.Clone(node);
    }
}

public static class Algorithms
{
    public static Node? Clone(Node? root)
    {
        var copies = new Dictionary<Node, Node>();
        Node? Copy(Node? node)
        {
            if (node is null)
                return null;
            if (copies.TryGetValue(node, out var found))
                return found;
            var clone = new Node(node.val);
            copies[node] = clone;
            foreach (var neighbor in node.neighbors)
                clone.neighbors.Add(Copy(neighbor)!);
            return clone;
        }
        return Copy(root);
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
