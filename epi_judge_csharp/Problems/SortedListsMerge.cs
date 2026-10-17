using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SortedListsMerge
{
    public static ListNode<int>? Solve(ListNode<int>? arg1, ListNode<int>? arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "sorted_lists_merge.tsv", new[] { "arg1", "arg2" }, new[] { typeof(ListNode<int>), typeof(ListNode<int>) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!, (ListNode<int>?)values[1]!));
}
