using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int Lca(BinaryTreeNode<int>? tree, int s, int b)
    {
        while (tree is not null)
        {
            if (tree.Data < s)
                tree = tree.Right;
            else if (tree.Data > b)
                tree = tree.Left;
            else
                return tree.Data;
        }
        throw new ArgumentException("Both target nodes must exist.");
    }
}
