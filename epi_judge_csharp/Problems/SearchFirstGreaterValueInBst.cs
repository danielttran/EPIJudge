using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SearchFirstGreaterValueInBst
{
    public static int Solve(BinaryTreeNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "search_first_greater_value_in_bst.tsv", new[] { "arg1", "arg2" }, new[] { typeof(BinaryTreeNode<int>), typeof(int) },
            typeof(int), values => Solve((BinaryTreeNode<int>?)values[0]!, (int)values[1]!));
}
