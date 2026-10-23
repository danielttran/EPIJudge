using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public bool IsDuplicateLeftBst(TreeNode? root)
    {
        var stack = new Stack<(TreeNode Node, long Lower, long Upper)>();
        if (root != null)
            stack.Push((root, -2147483649L, 2147483647L));
        while (stack.Count > 0)
        {
            var frame = stack.Pop();
            var node = frame.Node;
            if (node.Data <= frame.Lower || node.Data > frame.Upper)
                return false;
            if (node.Right != null)
                stack.Push((node.Right, node.Data, frame.Upper));
            if (node.Left != null)
                stack.Push((node.Left, frame.Lower, node.Data));
        }
        return true;
    }
}
