using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[][] CombinationSum(int[] candidates, int target)
    {
        var outp = new List<int[]>();
        var path = new List<int>();
        void Visit(int start, int remaining)
        {
            if (remaining == 0)
            {
                outp.Add(path.ToArray());
                return;
            }
            for (int i = start; i < candidates.Length; i++)
            if (candidates[i] <= remaining)
            {
                path.Add(candidates[i]);
                Visit(i, remaining - candidates[i]);
                path.RemoveAt(path.Count - 1);
            }
        }
        Visit(0, target);
        return outp.ToArray();
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
