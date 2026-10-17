using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MatrixEnclosedRegions
{
    public static List<List<string>> Solve(List<List<string>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "matrix_enclosed_regions.tsv", new[] { "arg1" }, new[] { typeof(List<List<string>>) },
            typeof(List<List<string>>), values => Solve((List<List<string>>)values[0]!));
}
