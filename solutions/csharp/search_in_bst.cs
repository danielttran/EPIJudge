using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int SearchBst(BinaryTreeNode<int>? tree, int key)
    {
        while (tree is not null)
        {
            if (tree.Data == key)
                return key;
            tree = key < tree.Data ? tree.Left : tree.Right;
        }
        return -1;
    }
}
