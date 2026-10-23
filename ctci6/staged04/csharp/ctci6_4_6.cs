using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public TreeNode? InorderSuccessor(TreeNode? node)
    {
        if (node == null)
            return null;
        if (node.Right != null)
        {
            var following = node.Right;
            while (following.Left != null)
                following = following.Left;
            return following;
        }
        TreeNode current = node;
        TreeNode? parent = node.Parent;
        while (parent != null && current == parent.Right)
        {
            current = parent;
            parent = parent.Parent;
        }
        return parent;
    }
}
