using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public TreeNode? FirstCommonAncestor(TreeNode? first, TreeNode? second)
    {
        if (first == null || second == null)
            return null;
        int depthFirst = 0, depthSecond = 0;
        for (var cursor = first; cursor != null; cursor = cursor.Parent)
            ++depthFirst;
        for (var cursor = second; cursor != null; cursor = cursor.Parent)
            ++depthSecond;
        while (depthFirst > depthSecond)
        {
            first = first!.Parent;
            --depthFirst;
        }
        while (depthSecond > depthFirst)
        {
            second = second!.Parent;
            --depthSecond;
        }
        while (!ReferenceEquals(first, second))
        {
            first = first?.Parent;
            second = second?.Parent;
        }
        return first;
    }
}
