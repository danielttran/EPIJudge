using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ConvertBase
{
    public static string Solve(string arg1, int arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "convert_base.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(string), typeof(int), typeof(int) },
            typeof(string), values => Solve((string)values[0]!, (int)values[1]!, (int)values[2]!));
}
