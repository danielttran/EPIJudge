using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RangeLookupInBst
{
    public static List<int> Solve(BinaryTreeNode<int>? arg1, (int, int) arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "range_lookup_in_bst.tsv", new[] { "arg1", "arg2" }, new[] { typeof(BinaryTreeNode<int>), typeof((int, int)) },
            typeof(List<int>), values => Solve((BinaryTreeNode<int>?)values[0]!, ((int, int))values[1]!));
}
