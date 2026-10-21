using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? BinaryTreeFromPreorderInorder(List<int> preorder, List<int> inorder)
    {
        var positions = inorder.Select((value, index) => (value, index)).ToDictionary(x => x.value, x => x.index);
        int next = 0;
        BinaryTreeNode<int>? Build(int left, int right)
        {
            if (left >= right)
                return null;
            int value = preorder[next++], middle = positions[value];
            var root = new BinaryTreeNode<int>(value) { Left = Build(left, middle), Right = Build(middle + 1, right) };
            if (root.Left is not null)
                root.Left.Parent = root;
            if (root.Right is not null)
                root.Right.Parent = root;
            return root;
        }
        return Build(0, inorder.Count);
    }
}
