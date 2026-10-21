using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int CombinationSum4(int[] nums, int target)
    {
        var dp = new System.Numerics.BigInteger[target + 1];
        dp[0] = 1;
        for (int v = 1; v <= target; v++)
        foreach (int c in nums)
        if (c <= v)
            dp[v] += dp[v - c];
        return (int)dp[target];
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
