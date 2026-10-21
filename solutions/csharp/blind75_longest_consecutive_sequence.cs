using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int LongestConsecutive(int[] nums)
    {
        var seen = nums.ToHashSet();
        int best = 0;
        foreach (int v in seen)
        if (!seen.Contains(v - 1))
        {
            int end = v;
            while (seen.Contains(end))
                end++;
            best = Math.Max(best, end - v);
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
