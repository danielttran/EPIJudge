using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class BstToSortedList
{
    public static List<int> Solve(BinaryTreeNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "bst_to_sorted_list.tsv", new[] { "arg1" }, new[] { typeof(BinaryTreeNode<int>) },
            typeof(List<int>), values => Solve((BinaryTreeNode<int>?)values[0]!));
}
