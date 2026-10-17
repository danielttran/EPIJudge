using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class BstMerge
{
    public static BinaryTreeNode<int>? Solve(BinaryTreeNode<int>? arg1, BinaryTreeNode<int>? arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "bst_merge.tsv", new[] { "arg1", "arg2" }, new[] { typeof(BinaryTreeNode<int>), typeof(BinaryTreeNode<int>) },
            typeof(BinaryTreeNode<int>), values => Solve((BinaryTreeNode<int>?)values[0]!, (BinaryTreeNode<int>?)values[1]!));
}
