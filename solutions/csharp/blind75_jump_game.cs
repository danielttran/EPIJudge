using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool CanJump(int[] nums)
    {
        int far = 0;
        for (int i = 0; i < nums.Length && i <= far; i++)
        {
            far = Math.Max(far, i + nums[i]);
            if (far >= nums.Length - 1)
                return true;
        }
        return false;
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
