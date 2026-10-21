using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool IsValid(string s)
    {
        var stack = new Stack<char>();
        foreach (char c in s)
        {
            if (c is '(' or '[' or '{')
                stack.Push(c);
            else
            {
                int j = ")] }".Replace(" ", "").IndexOf(c);
                if (stack.Count == 0 || stack.Pop() != "([{"[j])
                    return false;
            }
        }
        return stack.Count == 0;
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
