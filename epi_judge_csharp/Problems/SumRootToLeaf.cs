using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SumRootToLeaf
{
    public static int Solve(BinaryTreeNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "sum_root_to_leaf.tsv", new[] { "arg1" }, new[] { typeof(BinaryTreeNode<int>) },
            typeof(int), values => Solve((BinaryTreeNode<int>?)values[0]!));
}
