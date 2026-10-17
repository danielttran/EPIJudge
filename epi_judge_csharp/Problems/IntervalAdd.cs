using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IntervalAdd
{
    public static List<(int, int)> Solve(List<(int, int)> arg1, (int, int) arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "interval_add.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<(int, int)>), typeof((int, int)) },
            typeof(List<(int, int)>), values => Solve((List<(int, int)>)values[0]!, ((int, int))values[1]!));
}
