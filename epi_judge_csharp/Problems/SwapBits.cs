using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SwapBits
{
    public static long Solve(long arg1, int arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "swap_bits.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(long), typeof(int), typeof(int) },
            typeof(long), values => Solve((long)values[0]!, (int)values[1]!, (int)values[2]!));
}
