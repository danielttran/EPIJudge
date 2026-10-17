using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class StringTransformability
{
    public static int Solve(HashSet<string> arg1, string arg2, string arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "string_transformability.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(HashSet<string>), typeof(string), typeof(string) },
            typeof(int), values => Solve((HashSet<string>)values[0]!, (string)values[1]!, (string)values[2]!));
}
