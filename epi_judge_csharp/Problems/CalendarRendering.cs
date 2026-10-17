using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class CalendarRendering
{
    public static int Solve(List<(int, int)> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "calendar_rendering.tsv", new[] { "arg1" }, new[] { typeof(List<(int, int)>) },
            typeof(int), values => Solve((List<(int, int)>)values[0]!));
}
