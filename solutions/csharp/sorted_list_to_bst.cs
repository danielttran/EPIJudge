using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? BuildBstFromSortedDoublyList(BinaryTreeNode<int>? head, int count)
    {
        var cursor = head;
        BinaryTreeNode<int>? Build(int size)
        {
            if (size == 0)
                return null;
            var left = Build(size / 2);
            var root = cursor!;
            cursor = cursor!.Right;
            root.Left = left;
            root.Right = Build(size - size / 2 - 1);
            if (root.Left is not null)
                root.Left.Parent = root;
            if (root.Right is not null)
                root.Right.Parent = root;
            return root;
        }
        return Build(count);
    }
}
