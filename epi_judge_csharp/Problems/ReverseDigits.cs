using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ReverseDigits
{
    public static long Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "reverse_digits.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(long), values => Solve((int)values[0]!));
}
