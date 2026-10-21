using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public string[] FindWords(string[] board, string[] words)
    {
        var outp = new List<string>();
        foreach (string word in words.Distinct())
        {
            int rows = board.Length, cols = board[0].Length;
            var used = Enumerable.Range(0, rows).Select(_ => new bool[cols]).ToArray();
            bool Visit(int r, int c, int i)
            {
                if (r < 0 || r >= rows || c < 0 || c >= cols || used[r][c] || board[r][c] != word[i])
                    return false;
                if (i == word.Length - 1)
                    return true;
                used[r][c] = true;
                bool ok = Visit(r - 1, c, i + 1) || Visit(r + 1, c, i + 1) || Visit(r, c - 1, i + 1) || Visit(r, c + 1, i + 1);
                used[r][c] = false;
                return ok;
            }
            bool found = false;
            for (int r = 0; r < rows && !found; r++)
            for (int c = 0; c < cols && !found; c++)
                found = Visit(r, c, 0);
            if (found)
                outp.Add(word);
        }
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
