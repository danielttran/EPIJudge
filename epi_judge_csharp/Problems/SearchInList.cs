using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SearchInList
{
    public static int Solve(ListNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "search_in_list.tsv", new[] { "arg1", "arg2" }, new[] { typeof(ListNode<int>), typeof(int) },
            typeof(int), values => Solve((ListNode<int>?)values[0]!, (int)values[1]!));
}
