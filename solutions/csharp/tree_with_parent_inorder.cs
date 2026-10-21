using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<int> InorderTraversal(BinaryTreeNode<int>? tree)
    {
        var output = new List<int>();
        BinaryTreeNode<int>? previous = null, current = tree;
        while (current is not null)
        {
            BinaryTreeNode<int>? next;
            if (ReferenceEquals(previous, current.Parent))
            {
                if (current.Left is not null)
                    next = current.Left;
                else
                {
                    output.Add(current.Data);
                    next = current.Right ?? current.Parent;
                }
            }
            else if (ReferenceEquals(previous, current.Left))
            {
                output.Add(current.Data);
                next = current.Right ?? current.Parent;
            }
            else
                next = current.Parent;
            previous = current;
            current = next;
        }
        return output;
    }
}
