using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int MinMeetingRooms(int[][] intervals)
    {
        var events = intervals.SelectMany(row => new[] { (time: row[0], delta: 1), (time: row[1], delta: -1) }).OrderBy(e => e.time).ThenBy(e => e.delta);
        int active = 0, best = 0;
        foreach (var e in events)
        {
            active += e.delta;
            best = Math.Max(best, active);
        }
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
