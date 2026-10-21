using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool IsSubtree(TreeNode? root, TreeNode? subRoot)
    {
        return Algorithms.Subtree(root, subRoot);
    }
}

public static class Algorithms
{
    public static bool Same(TreeNode? a, TreeNode? b) => a is null || b is null ? a == b : a.val == b.val && Same(a.left, b.left) && Same(a.right, b.right);
    public static bool Subtree(TreeNode? root, TreeNode? target) => target is null || root is not null && (Same(root, target) || Subtree(root.left, target) || Subtree(root.right, target));
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
