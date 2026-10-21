using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public BinaryTreeNode<int>? MergeTwoBsts(BinaryTreeNode<int>? A, BinaryTreeNode<int>? B)
    {
        List<int> Inorder(BinaryTreeNode<int>? node)
        {
            var values = new List<int>();
            var stack = new Stack<BinaryTreeNode<int>>();
            while (node is not null || stack.Count > 0)
            {
                while (node is not null)
                {
                    stack.Push(node);
                    node = node.Left;
                }
                node = stack.Pop();
                values.Add(node.Data);
                node = node.Right;
            }
            return values;
        }
        var first = Inorder(A);
        var second = Inorder(B);
        var merged = new List<int>();
        int i = 0, j = 0;
        while (i < first.Count || j < second.Count)
            merged.Add(j == second.Count || (i < first.Count && first[i] <= second[j]) ? first[i++] : second[j++]);
        BinaryTreeNode<int>? Build(int start, int end)
        {
            if (start >= end)
                return null;
            int middle = start + (end - start) / 2;
            return new BinaryTreeNode<int>(merged[middle]) { Left = Build(start, middle), Right = Build(middle + 1, end) };
        }
        return Build(0, merged.Count);
    }
}
