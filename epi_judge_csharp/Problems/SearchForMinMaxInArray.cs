using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SearchForMinMaxInArray
{
    public static (int, int) Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "search_for_min_max_in_array.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof((int, int)), values => Solve((List<int>)values[0]!));
}
