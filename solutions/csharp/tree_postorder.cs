using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> PostorderTraversal(BinaryTreeNode<int>? tree)
    {
        var output = new List<int>();
        void Visit(BinaryTreeNode<int>? node)
        {
            if (node is null)
                return;
            Visit(node.Left);
            Visit(node.Right);
            output.Add(node.Data);
        }
        Visit(tree);
        return output;
    }
}
