using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public void ConstructRightSibling(BinaryTreeNode<int>? tree)
    {
        if (tree is null)
            return;
        tree.Next = null;
        for (var level = tree; level.Left is not null; level = level.Left)
            for (var node = level; node is not null; node = node.Next)
            {
                node.Left!.Next = node.Right;
                node.Right!.Next = node.Next?.Left;
            }
    }
}
