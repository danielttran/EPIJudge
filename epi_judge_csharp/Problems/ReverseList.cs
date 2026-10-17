using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ReverseList
{
    public static ListNode<int>? Solve(ListNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "reverse_list.tsv", new[] { "arg1" }, new[] { typeof(ListNode<int>) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!));
}
