using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int LengthOfLIS(int[] nums)
    {
        var tails = new List<int>();
        foreach (int v in nums)
        {
            int l = 0, r = tails.Count;
            while (l < r)
            {
                int mid = l + (r - l) / 2;
                if (tails[mid] < v)
                    l = mid + 1;
                else
                    r = mid;
            }
            if (l == tails.Count)
                tails.Add(v);
            else
                tails[l] = v;
        }
        return tails.Count;
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
