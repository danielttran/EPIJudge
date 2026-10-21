using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public TreeNode? InvertTree(TreeNode? root)
    {
        return Algorithms.Invert(root);
    }
}

public static class Algorithms
{
    public static TreeNode? Invert(TreeNode? node)
    {
        if (node is not null)
        {
            var left = Invert(node.left);
            node.left = Invert(node.right);
            node.right = left;
        }
        return node;
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
