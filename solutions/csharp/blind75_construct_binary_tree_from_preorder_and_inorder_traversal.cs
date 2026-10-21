using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public TreeNode? BuildTree(int[] preorder, int[] inorder)
    {
        return Algorithms.Build(preorder, inorder);
    }
}

public static class Algorithms
{
    public static TreeNode? Build(int[] preorder, int[] inorder)
    {
        var positions = inorder.Select((value, index) => (value, index)).ToDictionary(p => p.value, p => p.index);
        int next = 0;
        TreeNode? Visit(int left, int right)
        {
            if (left >= right)
                return null;
            int value = preorder[next++], middle = positions[value];
            return new TreeNode(value, Visit(left, middle), Visit(middle + 1, right));
        }
        return Visit(0, inorder.Length);
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
