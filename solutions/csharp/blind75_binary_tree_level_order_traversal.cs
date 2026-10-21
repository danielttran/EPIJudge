using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[][] LevelOrder(TreeNode? root)
    {
        return Algorithms.Levels(root);
    }
}

public static class Algorithms
{
    public static int[][] Levels(TreeNode? root)
    {
        var result = new List<int[]>();
        var level = new List<TreeNode>();
        if (root is not null)
            level.Add(root);
        while (level.Count > 0)
        {
            result.Add(level.Select(node => node.val).ToArray());
            level = level.SelectMany(node => new[] { node.left, node.right }).OfType<TreeNode>().ToList();
        }
        return result.ToArray();
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
