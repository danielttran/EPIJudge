using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public TreeNode? CreateMinimalBst(int[] sortedValues)
    {
        TreeNode ? Build(int lower, int upper, TreeNode ? parent)
        {
            if (lower >= upper)
                return null;
            int middle = lower + (upper - lower) / 2;
            var node = new TreeNode(sortedValues[middle]);
            node.Parent = parent;
            node.Left = Build(lower, middle, node);
            node.Right = Build(middle + 1, upper, node);
            return node;
        }
        return Build(0, sortedValues.Length, null);
    }
}
