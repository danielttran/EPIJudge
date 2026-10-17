using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LevenshteinDistance
{
    public static int Solve(string arg1, string arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "levenshtein_distance.tsv", new[] { "arg1", "arg2" }, new[] { typeof(string), typeof(string) },
            typeof(int), values => Solve((string)values[0]!, (string)values[1]!));
}
