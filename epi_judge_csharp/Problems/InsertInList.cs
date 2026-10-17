using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class InsertInList
{
    public static ListNode<int>? Solve(ListNode<int>? arg1, int arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "insert_in_list.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(ListNode<int>), typeof(int), typeof(int) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!, (int)values[1]!, (int)values[2]!));
}
