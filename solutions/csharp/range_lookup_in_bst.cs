using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> RangeLookupInBst(BinaryTreeNode<int>? tree, (int, int) i)
    {
        var values = new List<int>();
        void Visit(BinaryTreeNode<int>? node)
        {
            if (node is null)
                return;
            if (node.Data >= i.Item1)
                Visit(node.Left);
            if (node.Data >= i.Item1 && node.Data <= i.Item2)
                values.Add(node.Data);
            if (node.Data <= i.Item2)
                Visit(node.Right);
        }
        Visit(tree);
        return values;
    }
}
