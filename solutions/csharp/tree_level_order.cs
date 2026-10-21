using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<List<int>> BinaryTreeDepthOrder(BinaryTreeNode<int>? tree)
    {
        var output = new List<List<int>>();
        if (tree is null)
            return output;
        var queue = new Queue<BinaryTreeNode<int>>();
        queue.Enqueue(tree);
        while (queue.Count > 0)
        {
            int size = queue.Count;
            var level = new List<int>(size);
            for (int i = 0; i < size; i++)
            {
                var node = queue.Dequeue();
                level.Add(node.Data);
                if (node.Left is not null)
                    queue.Enqueue(node.Left);
                if (node.Right is not null)
                    queue.Enqueue(node.Right);
            }
            output.Add(level);
        }
        return output;
    }
}
