using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RemoveDuplicatesFromSortedList
{
    public static ListNode<int>? Solve(ListNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "remove_duplicates_from_sorted_list.tsv", new[] { "arg1" }, new[] { typeof(ListNode<int>) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!));
}
