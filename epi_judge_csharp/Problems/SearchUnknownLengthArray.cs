using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SearchUnknownLengthArray
{
    public static int Solve(List<int> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "search_unknown_length_array.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(int) },
            typeof(int), values => Solve((List<int>)values[0]!, (int)values[1]!));
}
