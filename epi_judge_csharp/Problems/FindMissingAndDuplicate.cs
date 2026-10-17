using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class FindMissingAndDuplicate
{
    public static (int, int) Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "find_missing_and_duplicate.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof((int, int)), values => Solve((List<int>)values[0]!));
}
