using System;
using System.Collections.Generic;
using System.Linq;
public class Codec
{
    public string Encode(string[] strings)
    {
        return string.Concat(strings.Select(s => s.Length + ":" + s));
    }
    public string[] Decode(string encoded)
    {
        var outp = new List<string>();
        int i = 0;
        while (i < encoded.Length)
        {
            int j = encoded.IndexOf(':', i), n = int.Parse(encoded[i..j]);
            i = j + 1;
            outp.Add(encoded.Substring(i, n));
            i += n;
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
