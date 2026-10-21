using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[] ProductExceptSelf(int[] nums)
    {
        var outp = new int[nums.Length];
        int product = 1;
        for (int i = 0; i < nums.Length; i++)
        {
            outp[i] = product;
            product *= nums[i];
        }
        product = 1;
        for (int i = nums.Length - 1; i >= 0; i--)
        {
            outp[i] *= product;
            product *= nums[i];
        }
        return outp;
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
