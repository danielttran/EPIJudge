using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LineThroughMostPoints
{
    public static int Solve(List<(int, int)> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "line_through_most_points.tsv", new[] { "arg1" }, new[] { typeof(List<(int, int)>) },
            typeof(int), values => Solve((List<(int, int)>)values[0]!));
}
