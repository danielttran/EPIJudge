using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LookAndSay
{
    public static string Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "look_and_say.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(string), values => Solve((int)values[0]!));
}
