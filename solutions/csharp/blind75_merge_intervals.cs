using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[][] Merge(int[][] intervals)
    {
        var outp = new List<int[]>();
        foreach (var row in intervals.OrderBy(r => r[0]))
        {
            if (outp.Count > 0 && row[0] <= outp[^1][1])
                outp[^1][1] = Math.Max(outp[^1][1], row[1]);
            else
                outp.Add(row.ToArray());
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
