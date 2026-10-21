using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[] SpiralOrder(int[][] matrix)
    {
        var outp = new List<int>();
        int top = 0, bottom = matrix.Length - 1, left = 0, right = matrix[0].Length - 1;
        while (top <= bottom && left <= right)
        {
            for (int c = left; c <= right; c++)
                outp.Add(matrix[top][c]);
            top++;
            for (int r = top; r <= bottom; r++)
                outp.Add(matrix[r][right]);
            right--;
            if (top <= bottom)
            {
                for (int c = right; c >= left; c--)
                    outp.Add(matrix[bottom][c]);
                bottom--;
            }
            if (left <= right)
            {
                for (int r = bottom; r >= top; r--)
                    outp.Add(matrix[r][left]);
                left++;
            }
        }
        return outp.ToArray();
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
