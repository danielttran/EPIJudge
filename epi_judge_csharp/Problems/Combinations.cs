using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Combinations
{
    public static List<List<int>> Solve(int arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "combinations.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(int) },
            typeof(List<List<int>>), values => Solve((int)values[0]!, (int)values[1]!),
            (expected, actual) => GenericTest.UnorderedEquals(expected, actual, typeof(List<List<int>>)));
}
