using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsAnonymousLetterConstructible
{
    public static bool Solve(string arg1, string arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "is_anonymous_letter_constructible.tsv", new[] { "arg1", "arg2" }, new[] { typeof(string), typeof(string) },
            typeof(bool), values => Solve((string)values[0]!, (string)values[1]!));
}
