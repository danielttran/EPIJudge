using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public string LongestPalindrome(string s)
    {
        int start = 0, length = 0;
        void Expand(int l, int r)
        {
            while (l >= 0 && r < s.Length && s[l] == s[r])
            {
                if (r - l + 1 > length || (r - l + 1 == length && l < start))
                {
                    start = l;
                    length = r - l + 1;
                }
                l--;
                r++;
            }
        }
        for (int i = 0; i < s.Length; i++)
        {
            Expand(i, i);
            Expand(i, i + 1);
        }
        return s.Substring(start, length);
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
