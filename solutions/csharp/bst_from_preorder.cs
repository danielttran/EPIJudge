using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? RebuildBstFromPreorder(List<int> preorder_sequence)
    {
        if (preorder_sequence.Count == 0)
            return null;
        var root = new BinaryTreeNode<int>(preorder_sequence[0]);
        var ancestors = new Stack<BinaryTreeNode<int>>();
        ancestors.Push(root);
        foreach (int value in preorder_sequence.Skip(1))
        {
            var node = new BinaryTreeNode<int>(value);
            if (value < ancestors.Peek().Data)
                ancestors.Peek().Left = node;
            else
            {
                BinaryTreeNode<int>? parent = null;
                while (ancestors.Count > 0 && value >= ancestors.Peek().Data)
                    parent = ancestors.Pop();
                parent!.Right = node;
            }
            ancestors.Push(node);
        }
        return root;
    }
}
