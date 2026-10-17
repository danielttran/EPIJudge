using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LowestCommonAncestor
{
    public static int Solve(BinaryTreeNode<int>? arg1, int arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "lowest_common_ancestor.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(BinaryTreeNode<int>), typeof(int), typeof(int) },
            typeof(int), values => Solve((BinaryTreeNode<int>?)values[0]!, (int)values[1]!, (int)values[2]!));
}
