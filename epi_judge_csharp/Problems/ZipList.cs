using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ZipList
{
    public static ListNode<int>? Solve(ListNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "zip_list.tsv", new[] { "arg1" }, new[] { typeof(ListNode<int>) },
            typeof(ListNode<int>), values => Solve((ListNode<int>?)values[0]!));
}
