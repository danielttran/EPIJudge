using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public bool CanFinish(int numCourses, int[][] prerequisites)
    {
        var graph = Enumerable.Range(0, numCourses).Select(_ => new List<int>()).ToArray();
        var degree = new int[numCourses];
        foreach (var e in prerequisites)
        {
            graph[e[1]].Add(e[0]);
            degree[e[0]]++;
        }
        var q = new Queue<int>(Enumerable.Range(0, numCourses).Where(v => degree[v] == 0));
        int count = 0;
        while (q.TryDequeue(out int v))
        {
            count++;
            foreach (int u in graph[v])
            if (--degree[u] == 0)
                q.Enqueue(u);
        }
        return count == numCourses;
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
