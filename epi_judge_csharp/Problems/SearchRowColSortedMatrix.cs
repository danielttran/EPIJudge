using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SearchRowColSortedMatrix
{
    public static bool Solve(List<List<int>> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "search_row_col_sorted_matrix.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<List<int>>), typeof(int) },
            typeof(bool), values => Solve((List<List<int>>)values[0]!, (int)values[1]!));
}
