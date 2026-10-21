using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindSuccessor(BinaryTreeNode<int>? tree, int node_idx)
    {
        var stack = new Stack<BinaryTreeNode<int>>();
        if (tree is not null)
            stack.Push(tree);
        BinaryTreeNode<int>? node = null;
        while (stack.TryPop(out var current))
        {
            if (current.Data == node_idx)
            {
                node = current;
                break;
            }
            if (current.Right is not null)
                stack.Push(current.Right);
            if (current.Left is not null)
                stack.Push(current.Left);
        }
        if (node is null)
            return -1;
        if (node.Right is not null)
        {
            node = node.Right;
            while (node.Left is not null)
                node = node.Left;
            return node.Data;
        }
        while (node.Parent is not null && ReferenceEquals(node.Parent.Right, node))
            node = node.Parent;
        return node.Parent?.Data ?? -1;
    }
}
