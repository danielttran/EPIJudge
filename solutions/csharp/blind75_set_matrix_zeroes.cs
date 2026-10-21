using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public void SetZeroes(int[][] matrix)
    {
        int rows = matrix.Length, cols = matrix[0].Length;
        var zeroRows = new bool[rows];
        var zeroCols = new bool[cols];
        for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
        if (matrix[r][c] == 0)
        {
            zeroRows[r] = true;
            zeroCols[c] = true;
        }
        for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
        if (zeroRows[r] || zeroCols[c])
            matrix[r][c] = 0;
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
