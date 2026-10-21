using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool HasCycle(ListNode? head)
    {
        var slow = head;
        var fast = head;
        while (fast?.next != null)
        {
            slow = slow!.next;
            fast = fast.next.next;
            if (ReferenceEquals(slow, fast))
                return true;
        }
        return false;
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
