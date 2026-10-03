using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class CountBits
{
    public static short Solve(int x)
    {
        // TODO - you fill in here.
        return 0;
    }

    public static int Run(string[] args) =>
        GenericTest.Run<int, short>(args, "count_bits.tsv", "x", Solve);
}
