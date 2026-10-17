using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KthNodeInTree
{
    public static int Solve(BinaryTreeNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "kth_node_in_tree.tsv", new[] { "arg1", "arg2" }, new[] { typeof(BinaryTreeNode<int>), typeof(int) },
            typeof(int), values => Solve((BinaryTreeNode<int>?)values[0]!, (int)values[1]!));
}
