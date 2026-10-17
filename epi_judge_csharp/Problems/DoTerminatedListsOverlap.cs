using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DoTerminatedListsOverlap
{
    public static void Solve(ListNode<int>? arg1, ListNode<int>? arg2, ListNode<int>? arg3)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "do_terminated_lists_overlap.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(ListNode<int>), typeof(ListNode<int>), typeof(ListNode<int>) },
            values => Solve((ListNode<int>?)values[0]!, (ListNode<int>?)values[1]!, (ListNode<int>?)values[2]!));
}
