using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DrawingSkyline
{
    public static List<(int, int, int)> Solve(List<(int, int, int)> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "drawing_skyline.tsv", new[] { "arg1" }, new[] { typeof(List<(int, int, int)>) },
            typeof(List<(int, int, int)>), values => Solve((List<(int, int, int)>)values[0]!));
}
