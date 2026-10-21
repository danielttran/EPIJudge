using System;
using System.Collections.Generic;
using System.Linq;
public class MedianFinder
{
    private readonly PriorityQueue<int, long> lower = new();
    private readonly PriorityQueue<int, long> upper = new();
    public void AddNum(int value)
    {
        lower.Enqueue(value, -(long)value);
        int moved = lower.Dequeue();
        upper.Enqueue(moved, moved);
        if (upper.Count > lower.Count)
        {
            moved = upper.Dequeue();
            lower.Enqueue(moved, -(long)moved);
        }
    }
    public double FindMedian() => lower.Count > upper.Count ? lower.Peek() : ((double)lower.Peek() + upper.Peek()) / 2;
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
