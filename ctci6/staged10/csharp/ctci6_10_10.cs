using System;
using System.Collections.Generic;
using System.Text;
public class RankTracker
{
    private sealed class Node
    {
        public int Value, LeftCount;
        public Node? Left, Right;
        public Node(int value)
        {
            Value = value;
        }
    }
    private Node? root;
    public RankTracker()
    {
    }
    public void Track(int value)
    {
        if (root == null)
        {
            root = new Node(value);
            return;
        }
        Node node = root;
        while (true)
        {
            if (value <= node.Value)
            {
                ++node.LeftCount;
                if (node.Left == null)
                {
                    node.Left = new Node(value);
                    return;
                }
                node = node.Left;
            }
            else
            {
                if (node.Right == null)
                {
                    node.Right = new Node(value);
                    return;
                }
                node = node.Right;
            }
        }
    }
    public int GetRank(int value)
    {
        Node? node = root;
        int skipped = 0;
        while (node != null)
        {
            if (value == node.Value)
                return skipped + node.LeftCount;
            if (value < node.Value)
                node = node.Left;
            else
            {
                skipped += node.LeftCount + 1;
                node = node.Right;
            }
        }
        return -1;
    }
}
