using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> CreateOutputList(BinaryTreeNode<int>? tree)
    {
        var output = new List<int>();
        if (tree is null)
            return output;
        bool Leaf(BinaryTreeNode<int> node) => node.Left is null && node.Right is null;
        output.Add(tree.Data);
        for (var node = tree.Left; node is not null; node = node.Left ?? node.Right)
        if (!Leaf(node))
            output.Add(node.Data);
        void Leaves(BinaryTreeNode<int>? node)
        {
            if (node is null)
                return;
            if (Leaf(node))
                output.Add(node.Data);
            else
            {
                Leaves(node.Left);
                Leaves(node.Right);
            }
        }
        Leaves(tree.Left);
        Leaves(tree.Right);
        var rightBoundary = new List<int>();
        for (var node = tree.Right; node is not null; node = node.Right ?? node.Left)
        if (!Leaf(node))
            rightBoundary.Add(node.Data);
        rightBoundary.Reverse();
        output.AddRange(rightBoundary);
        return output;
    }
}
