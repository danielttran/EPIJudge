using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> CreateListOfLeaves(BinaryTreeNode<int>? tree)
    {
        var result = new List<int>();
        void Visit(BinaryTreeNode<int>? node)
        {
            if (node is null)
                return;
            if (node.Left is null && node.Right is null)
            {
                result.Add(node.Data);
                return;
            }
            Visit(node.Left);
            Visit(node.Right);
        }
        Visit(tree);
        return result;
    }
}
