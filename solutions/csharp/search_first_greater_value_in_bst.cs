using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int FindFirstGreaterThanK(BinaryTreeNode<int>? tree, int k)
    {
        int candidate = -1;
        while (tree is not null)
        {
            if (tree.Data > k)
            {
                candidate = tree.Data;
                tree = tree.Left;
            }
            else
                tree = tree.Right;
        }
        return candidate;
    }
}
