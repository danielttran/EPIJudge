using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int MaxProduct(int[] nums)
    {
        int high = nums[0], low = nums[0], best = nums[0];
        foreach (int v in nums.Skip(1))
        {
            int a = high * v, b = low * v;
            high = Math.Max(v, Math.Max(a, b));
            low = Math.Min(v, Math.Min(a, b));
            best = Math.Max(best, high);
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
