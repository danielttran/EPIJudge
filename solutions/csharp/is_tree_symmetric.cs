using EpiJudge.TestFramework;
public class Solution
{
    public bool IsSymmetric(BinaryTreeNode<int>? tree)
    {
        bool Mirrors(BinaryTreeNode<int>? a, BinaryTreeNode<int>? b)
        {
            if (a is null || b is null)
                return a is null && b is null;
            return a.Data == b.Data && Mirrors(a.Left, b.Right) && Mirrors(a.Right, b.Left);
        }
        return tree is null || Mirrors(tree.Left, tree.Right);
    }
}
