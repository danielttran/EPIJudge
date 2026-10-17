using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MaxOfSlidingWindow
{
    public static List<(int, double)> Solve(List<(int, double)> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "max_of_sliding_window.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<(int, double)>), typeof(int) },
            typeof(List<(int, double)>), values => Solve((List<(int, double)>)values[0]!, (int)values[1]!));
}
