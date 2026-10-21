using EpiJudge.TestFramework;
public class Solution
{
    public bool IsBalancedBinaryTree(BinaryTreeNode<int>? tree)
    {
        int Height(BinaryTreeNode<int>? node)
        {
            if (node is null)
                return 0;
            int left = Height(node.Left);
            if (left < 0)
                return -1;
            int right = Height(node.Right);
            if (right < 0 || Math.Abs(left - right) > 1)
                return -1;
            return Math.Max(left, right) + 1;
        }
        return Height(tree) >= 0;
    }
}
