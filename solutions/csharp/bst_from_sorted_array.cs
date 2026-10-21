using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? BuildMinHeightBstFromSortedArray(List<int> values)
    {
        BinaryTreeNode<int>? Build(int start, int end)
        {
            if (start >= end)
                return null;
            int middle = start + (end - start) / 2;
            return new BinaryTreeNode<int>(values[middle])
            {
                Left = Build(start, middle),
                Right = Build(middle + 1, end)
            };
        }
        return Build(0, values.Count);
    }
}
