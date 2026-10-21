using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? ReconstructPreorder(List<string> data)
    {
        int position = 0;
        BinaryTreeNode<int>? Build()
        {
            if (position >= data.Count)
                return null;
            string token = data[position++];
            if (token == "null")
                return null;
            var root = new BinaryTreeNode<int>(int.Parse(token, System.Globalization.CultureInfo.InvariantCulture));
            root.Left = Build();
            root.Right = Build();
            if (root.Left is not null)
                root.Left.Parent = root;
            if (root.Right is not null)
                root.Right.Parent = root;
            return root;
        }
        return Build();
    }
}
