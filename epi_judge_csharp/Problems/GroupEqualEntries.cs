using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class GroupEqualEntries
{
    public static void Solve(List<(int, string)> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "group_equal_entries.tsv", new[] { "arg1" }, new[] { typeof(List<(int, string)>) },
            values => Solve((List<(int, string)>)values[0]!));
}
