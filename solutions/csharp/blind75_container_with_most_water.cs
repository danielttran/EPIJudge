using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int MaxArea(int[] height)
    {
        int l = 0, r = height.Length - 1, best = 0;
        while (l < r)
        {
            best = Math.Max(best, (r - l) * Math.Min(height[l], height[r]));
            if (height[l] < height[r])
                l++;
            else
                r--;
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
