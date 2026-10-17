using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsListCyclic
{
    public static void Solve(ListNode<int>? arg1, int arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "is_list_cyclic.tsv", new[] { "arg1", "arg2" }, new[] { typeof(ListNode<int>), typeof(int) },
            values => Solve((ListNode<int>?)values[0]!, (int)values[1]!));
}
