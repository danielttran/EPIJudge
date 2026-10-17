using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsListPalindromic
{
    public static bool Solve(ListNode<int>? arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_list_palindromic.tsv", new[] { "arg1" }, new[] { typeof(ListNode<int>) },
            typeof(bool), values => Solve((ListNode<int>?)values[0]!));
}
