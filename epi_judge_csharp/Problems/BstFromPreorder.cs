using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class BstFromPreorder
{
    public static BinaryTreeNode<int>? Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "bst_from_preorder.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(BinaryTreeNode<int>), values => Solve((List<int>)values[0]!));
}
