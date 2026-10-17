using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IntervalsUnion
{
    public static List<(int, bool, int, bool)> Solve(List<(int, bool, int, bool)> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "intervals_union.tsv", new[] { "arg1" }, new[] { typeof(List<(int, bool, int, bool)>) },
            typeof(List<(int, bool, int, bool)>), values => Solve((List<(int, bool, int, bool)>)values[0]!));
}
