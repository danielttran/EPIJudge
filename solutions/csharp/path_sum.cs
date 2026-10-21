using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public bool HasPathSum(BinaryTreeNode<int>? tree, int remaining_weight)
    {
        bool Visit(BinaryTreeNode<int>? node, long remaining)
        {
            if (node is null)
                return false;
            remaining -= node.Data;
            if (node.Left is null && node.Right is null)
                return remaining == 0;
            return Visit(node.Left, remaining) || Visit(node.Right, remaining);
        }
        return Visit(tree, remaining_weight);
    }
}
