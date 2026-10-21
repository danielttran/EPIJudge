using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int MaxPathSum(TreeNode? root)
    {
        return Algorithms.MaxPath(root);
    }
}

public static class Algorithms
{
    public static int MaxPath(TreeNode root)
    {
        int best = int.MinValue;
        int Gain(TreeNode? node)
        {
            if (node is null)
                return 0;
            int left = Math.Max(0, Gain(node.left)), right = Math.Max(0, Gain(node.right));
            best = Math.Max(best, node.val + left + right);
            return node.val + Math.Max(left, right);
        }
        Gain(root);
        return best;
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
