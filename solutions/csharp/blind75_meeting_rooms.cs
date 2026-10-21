using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool CanAttendMeetings(int[][] intervals)
    {
        var rows = intervals.OrderBy(r => r[0]).ToArray();
        for (int i = 1; i < rows.Length; i++)
        if (rows[i][0] < rows[i - 1][1])
            return false;
        return true;
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
