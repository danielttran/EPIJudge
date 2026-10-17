using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class TreeFromPreorderWithNull
{
    public static BinaryTreeNode<int>? Solve(List<string> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "tree_from_preorder_with_null.tsv", new[] { "arg1" }, new[] { typeof(List<string>) },
            typeof(BinaryTreeNode<int>), values => Solve((List<string>)values[0]!));
}
