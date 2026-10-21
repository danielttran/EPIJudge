using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int Lca(BinaryTreeNode<int>? tree, int node0, int node1)
    {
        if (tree is null)
            throw new ArgumentException("The target nodes must exist.");
        var parents = new Dictionary<BinaryTreeNode<int>, BinaryTreeNode<int>?> { [tree] = null };
        var pending = new Stack<BinaryTreeNode<int>>();
        pending.Push(tree);
        BinaryTreeNode<int>? first = null, second = null;
        while (pending.Count > 0 && (first is null || second is null))
        {
            var node = pending.Pop();
            if (node.Data == node0)
                first = node;
            if (node.Data == node1)
                second = node;
            if (node.Left is not null)
            {
                parents[node.Left] = node;
                pending.Push(node.Left);
            }
            if (node.Right is not null)
            {
                parents[node.Right] = node;
                pending.Push(node.Right);
            }
        }
        if (first is null || second is null)
            throw new ArgumentException("The target nodes must exist.");
        var ancestors = new HashSet<BinaryTreeNode<int>>();
        for (var node = first; node is not null; node = parents[node])
            ancestors.Add(node);
        for (var node = second; node is not null; node = parents[node])
        if (ancestors.Contains(node))
            return node.Data;
        throw new InvalidOperationException();
    }
}
