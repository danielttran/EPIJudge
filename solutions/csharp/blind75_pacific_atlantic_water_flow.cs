using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int[][] PacificAtlantic(int[][] heights)
    {
        int rows = heights.Length, cols = heights[0].Length;
        bool[,] Flood(bool pacific)
        {
            var seen = new bool[rows, cols];
            var q = new Queue<(int, int)>();
            for (int r = 0; r < rows; r++)
            {
                int c = pacific ? 0 : cols - 1;
                if (!seen[r, c])
                {
                    seen[r, c] = true;
                    q.Enqueue((r, c));
                }
            }
            for (int c = 0; c < cols; c++)
            {
                int r = pacific ? 0 : rows - 1;
                if (!seen[r, c])
                {
                    seen[r, c] = true;
                    q.Enqueue((r, c));
                }
            }
            int[] dr = [-1, 1, 0, 0], dc = [0, 0, -1, 1];
            while (q.TryDequeue(out var p))
            for (int i = 0; i < 4; i++)
            {
                int u = p.Item1 + dr[i], v = p.Item2 + dc[i];
                if (u >= 0 && u < rows && v >= 0 && v < cols && !seen[u, v] && heights[u][v] >= heights[p.Item1][p.Item2])
                {
                    seen[u, v] = true;
                    q.Enqueue((u, v));
                }
            }
            return seen;
        }
        var a = Flood(true);
        var b = Flood(false);
        var outp = new List<int[]>();
        for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
        if (a[r, c] && b[r, c])
            outp.Add([r, c]);
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
