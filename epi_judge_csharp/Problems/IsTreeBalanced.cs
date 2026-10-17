using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsTreeBalanced
{
    public static bool Solve(BinaryTreeNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_tree_balanced.tsv", new[] { "arg1" }, new[] { typeof(BinaryTreeNode<int>) },
            typeof(bool), values => Solve((BinaryTreeNode<int>?)values[0]!));
}
