using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SumRootToLeaf(BinaryTreeNode<int>? tree)
    {
        int Visit(BinaryTreeNode<int>? node, int prefix)
        {
            if (node is null)
                return 0;
            int value = (prefix << 1) | node.Data;
            return node.Left is null && node.Right is null ? value : Visit(node.Left, value) + Visit(node.Right, value);
        }
        return Visit(tree, 0);
    }
}
