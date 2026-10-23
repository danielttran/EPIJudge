using System;
using System.Collections.Generic;
using System.Text;
public class TreeNode {public int Data;public TreeNode? Left,Right,Parent;public TreeNode(int data){Data=data;}}
public class Solution
{
    public int CountDownwardSumPaths(TreeNode? root, int target)
    {
        if (root == null)
            return 0;
        var prefix = new Dictionary<int, int> { { 0, 1 } };
        var stack = new Stack<(TreeNode Node, int Sum, bool Exit)>();
        stack.Push((root, 0, false));
        int answer = 0;
        while (stack.Count > 0)
        {
            var frame = stack.Pop();
            if (frame.Exit)
            {
                if (--prefix[frame.Sum] == 0)
                    prefix.Remove(frame.Sum);
                continue;
            }
            int running = frame.Sum + frame.Node.Data;
            prefix.TryGetValue(running - target, out int count);
            answer += count;
            prefix.TryGetValue(running, out int previous);
            prefix[running] = previous + 1;
            stack.Push((frame.Node, running, true));
            if (frame.Node.Right != null)
                stack.Push((frame.Node.Right, running, false));
            if (frame.Node.Left != null)
                stack.Push((frame.Node.Left, running, false));
        }
        return answer;
    }
}
