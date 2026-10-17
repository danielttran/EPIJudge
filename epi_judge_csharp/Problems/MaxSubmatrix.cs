using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MaxSubmatrix
{
    public static int Solve(List<List<bool>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "max_submatrix.tsv", new[] { "arg1" }, new[] { typeof(List<List<bool>>) },
            typeof(int), values => Solve((List<List<bool>>)values[0]!));
}
