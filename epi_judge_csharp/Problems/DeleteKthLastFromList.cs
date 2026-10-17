using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DeleteKthLastFromList
{
    public static ListNode<int>? Solve(ListNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "delete_kth_last_from_list.tsv", new[] { "arg1", "arg2" }, new[] { typeof(ListNode<int>), typeof(int) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!, (int)values[1]!));
}
