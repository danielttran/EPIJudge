using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public string MinWindow(string s, string t)
    {
        var need = new int[128];
        foreach (char c in t)
            need[c]++;
        int missing = t.Length, left = 0, start = 0, length = int.MaxValue;
        for (int r = 0; r < s.Length; r++)
        {
            if (need[s[r]]-- > 0)
                missing--;
            while (missing == 0)
            {
                if (r - left + 1 < length)
                {
                    start = left;
                    length = r - left + 1;
                }
                if (++need[s[left++]] > 0)
                    missing++;
            }
        }
        return length == int.MaxValue ? "" : s.Substring(start, length);
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
