using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class CopyPostingList
{
    public static void Solve(List<(int, int)> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "copy_posting_list.tsv", new[] { "arg1" }, new[] { typeof(List<(int, int)>) },
            values => Solve((List<(int, int)>)values[0]!));
}
