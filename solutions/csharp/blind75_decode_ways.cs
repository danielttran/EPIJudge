using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int NumDecodings(string s)
    {
        System.Numerics.BigInteger a = 1, b = s[0] == '0' ? 0 : 1;
        for (int i = 1; i < s.Length; i++)
        {
            System.Numerics.BigInteger next = s[i] == '0' ? 0 : b;
            int pair = (s[i - 1] - '0') * 10 + s[i] - '0';
            if (pair >= 10 && pair <= 26)
                next += a;
            a = b;
            b = next;
        }
        return (int)b;
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
