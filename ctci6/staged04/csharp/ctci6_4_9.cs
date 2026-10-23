using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public List<List<int>> BstInsertionSequences(TreeNode? root)
    {
        var result = new List<List<int>>();
        var path = new List<int>();
        void Visit(List<TreeNode> available)
        {
            if (available.Count == 0)
            {
                result.Add(new List<int>(path));
                return;
            }
            for (int i = 0; i < available.Count; ++i)
            {
                var node = available[i];
                var following = new List<TreeNode>(available);
                following.RemoveAt(i);
                if (node.Left != null)
                    following.Add(node.Left);
                if (node.Right != null)
                    following.Add(node.Right);
                path.Add(node.Data);
                Visit(following);
                path.RemoveAt(path.Count - 1);
            }
        }
        Visit(root == null ? new List<TreeNode>() : new List<TreeNode> { root });
        return result;
    }
}
