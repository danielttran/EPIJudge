using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public bool IsHeightBalanced(TreeNode? root)
    {
        if (root == null)
            return true;
        var heights = new Dictionary<TreeNode, int>();
        var stack = new Stack<(TreeNode Node, bool Exit)>();
        stack.Push((root, false));
        while (stack.Count > 0)
        {
            var frame = stack.Pop();
            var node = frame.Node;
            if (!frame.Exit)
            {
                stack.Push((node, true));
                if (node.Right != null)
                    stack.Push((node.Right, false));
                if (node.Left != null)
                    stack.Push((node.Left, false));
            }
            else
            {
                int left = node.Left == null ? 0 : heights[node.Left],
                    right = node.Right == null ? 0 : heights[node.Right];
                if (Math.Abs(left - right) > 1)
                    return false;
                heights[node] = 1 + Math.Max(left, right);
            }
        }
        return true;
    }
}
