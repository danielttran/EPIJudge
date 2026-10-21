using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int CoinChange(int[] coins, int amount)
    {
        var dp = Enumerable.Repeat(amount + 1, amount + 1).ToArray();
        dp[0] = 0;
        for (int v = 1; v <= amount; v++)
        foreach (int c in coins)
        if (c <= v)
            dp[v] = Math.Min(dp[v], dp[v - c] + 1);
        return dp[amount] > amount ? -1 : dp[amount];
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
