using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public void Rotate(int[][] matrix)
    {
        int n = matrix.Length;
        for (int r = 0; r < n; r++)
        for (int c = r + 1; c < n; c++)
            (matrix[r][c], matrix[c][r]) = (matrix[c][r], matrix[r][c]);
        foreach (var row in matrix)
            Array.Reverse(row);
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
