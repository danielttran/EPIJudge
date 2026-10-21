using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int Rob(int[] nums)
    {
        int Run(int lo, int hi)
        {
            int a = 0, b = 0;
            for (int i = lo; i < hi; i++)
            {
                int next = Math.Max(b, a + nums[i]);
                a = b;
                b = next;
            }
            return b;
        }
        return Run(0, nums.Length);
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
