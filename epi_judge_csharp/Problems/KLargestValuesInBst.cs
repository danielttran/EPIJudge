using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KLargestValuesInBst
{
    public static List<int> Solve(BinaryTreeNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "k_largest_values_in_bst.tsv", new[] { "arg1", "arg2" }, new[] { typeof(BinaryTreeNode<int>), typeof(int) },
            typeof(List<int>), values => Solve((BinaryTreeNode<int>?)values[0]!, (int)values[1]!));
}
