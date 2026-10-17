using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IntAsListAdd
{
    public static ListNode<int>? Solve(ListNode<int>? arg1, ListNode<int>? arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "int_as_list_add.tsv", new[] { "arg1", "arg2" }, new[] { typeof(ListNode<int>), typeof(ListNode<int>) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!, (ListNode<int>?)values[1]!));
}
