using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RomanToInteger
{
    public static int Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "roman_to_integer.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(int), values => Solve((string)values[0]!));
}
