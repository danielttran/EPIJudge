using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public bool ContainsExactSubtree(TreeNode? large, TreeNode? small)
    {
        if (small == null)
            return true;List<string> Encode(TreeNode? root)
        {
            var tokens = new List<string>();
            var stack = new Stack<TreeNode?>();
            stack.Push(root);
            while (stack.Count > 0)
            {
                var node = stack.Pop();
                if (node == null)
                    tokens.Add("#");
                else
                {
                    tokens.Add("V" + node.Data.ToString(
                                         System.Globalization.CultureInfo.InvariantCulture));
                    stack.Push(node.Right);
                    stack.Push(node.Left);
                }
            }
            return tokens;
        }
        var text = Encode(large);
        var pattern = Encode(small);
        int[] prefix = new int[pattern.Count];
        for (int i = 1; i < pattern.Count; ++i)
        {
            int matched = prefix[i - 1];
            while (matched > 0 && pattern[i] != pattern[matched])
                matched = prefix[matched - 1];
            if (pattern[i] == pattern[matched])
                ++matched;
            prefix[i] = matched;
        }
        int count = 0;
        foreach (string token in text)
        {
            while (count > 0 && token != pattern[count])
                count = prefix[count - 1];
            if (token == pattern[count])
                ++count;
            if (count == pattern.Count)
                return true;
        }
        return false;
    }
}
