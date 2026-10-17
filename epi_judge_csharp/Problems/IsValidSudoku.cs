using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsValidSudoku
{
    public static bool Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_valid_sudoku.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            typeof(bool), values => Solve((List<List<int>>)values[0]!));
}
