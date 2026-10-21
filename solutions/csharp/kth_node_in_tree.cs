using EpiJudge.TestFramework;
public class Solution
{
    public int FindKthNodeBinaryTree(BinaryTreeNode<int>? tree, int k)
    {
        var pending = new Stack<BinaryTreeNode<int>>();
        var current = tree;
        while (current is not null || pending.Count > 0)
        {
            while (current is not null)
            {
                pending.Push(current);
                current = current.Left;
            }
            current = pending.Pop();
            if (--k == 0)
                return current.Data;
            current = current.Right;
        }
        throw new ArgumentOutOfRangeException(nameof(k));
    }
}
