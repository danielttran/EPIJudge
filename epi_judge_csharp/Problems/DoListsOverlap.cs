using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DoListsOverlap
{
    public static void Solve(ListNode<int>? arg1, ListNode<int>? arg2, ListNode<int>? arg3, int arg4, int arg5)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "do_lists_overlap.tsv", new[] { "arg1", "arg2", "arg3", "arg4", "arg5" }, new[] { typeof(ListNode<int>), typeof(ListNode<int>), typeof(ListNode<int>), typeof(int), typeof(int) },
            values => Solve((ListNode<int>?)values[0]!, (ListNode<int>?)values[1]!, (ListNode<int>?)values[2]!, (int)values[3]!, (int)values[4]!));
}
