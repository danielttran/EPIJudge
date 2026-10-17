using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PascalTriangle
{
    public static List<List<int>> Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "pascal_triangle.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(List<List<int>>), values => Solve((int)values[0]!));
}
