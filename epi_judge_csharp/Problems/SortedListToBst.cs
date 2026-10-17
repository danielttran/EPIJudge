using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SortedListToBst
{
    public static void Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "sorted_list_to_bst.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            values => Solve((List<int>)values[0]!));
}
