using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RemoveDuplicates
{
    public static List<string> Solve(List<(string, string)> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "remove_duplicates.tsv", new[] { "arg1" }, new[] { typeof(List<(string, string)>) },
            typeof(List<string>), values => Solve((List<(string, string)>)values[0]!));
}
