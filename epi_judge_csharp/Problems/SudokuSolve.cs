using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SudokuSolve
{
    public static void Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "sudoku_solve.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            values => Solve((List<List<int>>)values[0]!));
}
