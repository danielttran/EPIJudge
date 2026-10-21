using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool IsValidBST(TreeNode? root)
    {
        var a = Algorithms.Inorder(root).ToArray();
        return a.Zip(a.Skip(1)).All(p => p.First < p.Second);
    }
}

public static class Algorithms
{
    public static IEnumerable<int> Inorder(TreeNode? node)
    {
        var stack = new Stack<TreeNode>();
        while (node is not null || stack.Count > 0)
        {
            while (node is not null)
            {
                stack.Push(node);
                node = node.left;
            }
            node = stack.Pop();
            yield return node.val;
            node = node.right;
        }
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
