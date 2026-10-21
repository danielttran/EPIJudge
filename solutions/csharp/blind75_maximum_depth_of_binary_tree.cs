using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int MaxDepth(TreeNode? root)
    {
        return Algorithms.Depth(root);
    }
}

public static class Algorithms
{
    public static int Depth(TreeNode? node) => node is null ? 0 : 1 + Math.Max(Depth(node.left), Depth(node.right));
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
