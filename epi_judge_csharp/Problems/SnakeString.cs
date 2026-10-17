using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SnakeString
{
    public static string Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "snake_string.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(string), values => Solve((string)values[0]!));
}
