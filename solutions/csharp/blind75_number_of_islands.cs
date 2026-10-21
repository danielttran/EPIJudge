using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int NumIslands(string[] grid)
    {
        int rows = grid.Length, cols = grid[0].Length, count = 0;
        var seen = new bool[rows, cols];
        int[] dr = [-1, 1, 0, 0], dc = [0, 0, -1, 1];
        for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
        if (grid[r][c] == '1' && !seen[r, c])
        {
            count++;
            seen[r, c] = true;
            var q = new Queue<(int, int)>();
            q.Enqueue((r, c));
            while (q.TryDequeue(out var p))
            for (int i = 0; i < 4; i++)
            {
                int u = p.Item1 + dr[i], v = p.Item2 + dc[i];
                if (u >= 0 && u < rows && v >= 0 && v < cols && grid[u][v] == '1' && !seen[u, v])
                {
                    seen[u, v] = true;
                    q.Enqueue((u, v));
                }
            }
        }
        return count;
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
