using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsStringInMatrix
{
    public static bool Solve(List<List<int>> arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_string_in_matrix.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<List<int>>), typeof(List<int>) },
            typeof(bool), values => Solve((List<List<int>>)values[0]!, (List<int>)values[1]!));
}
