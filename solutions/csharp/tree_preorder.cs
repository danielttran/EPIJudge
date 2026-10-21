using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> PreorderTraversal(BinaryTreeNode<int>? tree)
    {
        var output = new List<int>();
        void Visit(BinaryTreeNode<int>? node)
        {
            if (node is null)
                return;
            output.Add(node.Data);
            Visit(node.Left);
            Visit(node.Right);
        }
        Visit(tree);
        return output;
    }
}
