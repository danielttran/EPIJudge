using System;
using System.Collections.Generic;
using System.Linq;
public class Codec
{
    public string Serialize(TreeNode? root)
    {
        return Algorithms.Serialize(root);
    }
    public TreeNode? Deserialize(string encoded)
    {
        return Algorithms.Deserialize(encoded);
    }
}

public static class Algorithms
{
    public static string Serialize(TreeNode? root)
    {
        var text = new System.Text.StringBuilder();
        void Visit(TreeNode? node)
        {
            if (node is null)
            {
                text.Append("# ");
                return;
            }
            text.Append(node.val).Append(' ');
            Visit(node.left);
            Visit(node.right);
        }
        Visit(root);
        return text.ToString();
    }
    public static TreeNode? Deserialize(string text)
    {
        var tokens = new Queue<string>(text.Split(' ', StringSplitOptions.RemoveEmptyEntries));
        TreeNode? Read()
        {
            string token = tokens.Dequeue();
            return token == "#" ? null : new TreeNode(int.Parse(token), Read(), Read());
        }
        return Read();
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
