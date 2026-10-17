using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DescendantAndAncestorInBst
{
    public static bool Solve(BinaryTreeNode<int>? arg1, int arg2, int arg3, int arg4)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "descendant_and_ancestor_in_bst.tsv", new[] { "arg1", "arg2", "arg3", "arg4" }, new[] { typeof(BinaryTreeNode<int>), typeof(int), typeof(int), typeof(int) },
            typeof(bool), values => Solve((BinaryTreeNode<int>?)values[0]!, (int)values[1]!, (int)values[2]!, (int)values[3]!));
}
