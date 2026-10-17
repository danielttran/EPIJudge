using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ReverseBits
{
    public static long Solve(long arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "reverse_bits.tsv", new[] { "arg1" }, new[] { typeof(long) },
            typeof(long), values => Solve((long)values[0]!));
}
