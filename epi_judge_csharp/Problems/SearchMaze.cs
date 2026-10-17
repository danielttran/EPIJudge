using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SearchMaze
{
    public static bool Solve(List<List<int>> arg1, (int, int) arg2, (int, int) arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "search_maze.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(List<List<int>>), typeof((int, int)), typeof((int, int)) },
            typeof(bool), values => Solve((List<List<int>>)values[0]!, ((int, int))values[1]!, ((int, int))values[2]!));
}
