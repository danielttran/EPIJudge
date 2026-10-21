using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public void ReorderList(ListNode? head)
    {
        if (head?.next is null)
            return;
        var slow = head;
        var fast = head;
        while (fast.next?.next is not null)
        {
            slow = slow.next!;
            fast = fast.next.next;
        }
        ListNode? current = slow.next, previous = null;
        slow.next = null;
        while (current is not null)
        {
            var next = current.next;
            current.next = previous;
            previous = current;
            current = next;
        }
        var first = head;
        while (previous is not null)
        {
            var a = first.next;
            var b = previous.next;
            first.next = previous;
            previous.next = a;
            first = a!;
            previous = b;
        }
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
