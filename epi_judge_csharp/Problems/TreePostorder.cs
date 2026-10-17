using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class TreePostorder
{
    public static List<int> Solve(BinaryTreeNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "tree_postorder.tsv", new[] { "arg1" }, new[] { typeof(BinaryTreeNode<int>) },
            typeof(List<int>), values => Solve((BinaryTreeNode<int>?)values[0]!));
}
