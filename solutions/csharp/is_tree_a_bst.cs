using EpiJudge.TestFramework;
public class Solution
{
    public bool IsBinaryTreeBst(BinaryTreeNode<int>? tree)
    {
        if (tree is null)
            return true;
        var pending = new Stack<(BinaryTreeNode<int> Node, long Low, long High)>();
        pending.Push((tree, long.MinValue, long.MaxValue));
        while (pending.TryPop(out var entry))
        {
            var (node, low, high) = entry;
            if (node.Data < low || node.Data > high)
                return false;
            if (node.Left is not null)
                pending.Push((node.Left, low, node.Data));
            if (node.Right is not null)
                pending.Push((node.Right, node.Data, high));
        }
        return true;
    }
}
