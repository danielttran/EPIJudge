using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PathSum
{
    public static bool Solve(BinaryTreeNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "path_sum.tsv", new[] { "arg1", "arg2" }, new[] { typeof(BinaryTreeNode<int>), typeof(int) },
            typeof(bool), values => Solve((BinaryTreeNode<int>?)values[0]!, (int)values[1]!));
}
