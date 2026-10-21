using System;
using System.Collections.Generic;
using System.Linq;
public class Solution
{
    public int CharacterReplacement(string s, int k)
    {
        var counts = new int[26];
        int left = 0, most = 0, best = 0;
        for (int r = 0; r < s.Length; r++)
        {
            most = Math.Max(most, ++counts[s[r] - 'A']);
            while (r - left + 1 - most > k)
                counts[s[left++] - 'A']--;
            best = Math.Max(best, r - left + 1);
        }
        return best;
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
