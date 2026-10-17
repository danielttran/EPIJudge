using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class TreeLevelOrder
{
    public static List<List<int>> Solve(BinaryTreeNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "tree_level_order.tsv", new[] { "arg1" }, new[] { typeof(BinaryTreeNode<int>) },
            typeof(List<List<int>>), values => Solve((BinaryTreeNode<int>?)values[0]!));
}
