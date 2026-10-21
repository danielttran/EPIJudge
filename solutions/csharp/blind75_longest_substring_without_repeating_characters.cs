using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int LengthOfLongestSubstring(string s)
    {
        var last = new Dictionary<char, int>();
        int left = 0, best = 0;
        for (int i = 0; i < s.Length; i++)
        {
            if (last.TryGetValue(s[i], out int j))
                left = Math.Max(left, j + 1);
            last[s[i]] = i;
            best = Math.Max(best, i - left + 1);
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
