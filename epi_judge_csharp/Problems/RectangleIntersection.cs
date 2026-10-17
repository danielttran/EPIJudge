using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RectangleIntersection
{
    public static (int, int, int, int) Solve((int, int, int, int) arg1, (int, int, int, int) arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "rectangle_intersection.tsv", new[] { "arg1", "arg2" }, new[] { typeof((int, int, int, int)), typeof((int, int, int, int)) },
            typeof((int, int, int, int)), values => Solve(((int, int, int, int))values[0]!, ((int, int, int, int))values[1]!));
}
