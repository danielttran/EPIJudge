using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class DepthLink {public TreeNode Value;public DepthLink? Next;public DepthLink(TreeNode value){Value=value;}}
public class Solution
{
    public List<DepthLink> LinkedListsByDepth(TreeNode? root)
    {
        var heads = new List<DepthLink>();
        if (root == null)
            return heads;
        var current = new List<TreeNode> { root };
        while (current.Count > 0)
        {
            DepthLink? head = null, tail = null;
            var following = new List<TreeNode>();
            foreach (var node in current)
            {
                var link = new DepthLink(node);
                if (tail == null)
                    head = link;
                else
                    tail.Next = link;
                tail = link;
                if (node.Left != null)
                    following.Add(node.Left);
                if (node.Right != null)
                    following.Add(node.Right);
            }
            heads.Add(head!);
            current = following;
        }
        return heads;
    }
}
