using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public ListNode? MergeKLists(ListNode?[] lists)
    {
        var queue = new PriorityQueue<ListNode, int>();
        foreach (var node in lists)
        if (node is not null)
            queue.Enqueue(node, node.val);
        var dummy = new ListNode();
        var tail = dummy;
        while (queue.TryDequeue(out var node, out _))
        {
            if (node.next is not null)
                queue.Enqueue(node.next, node.next.val);
            tail.next = node;
            tail = node;
        }
        tail.next = null;
        return dummy.next;
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
