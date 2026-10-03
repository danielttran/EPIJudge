using EpiJudge.TestFramework;

namespace EpiJudge.Solutions;

public static class CountBits
{
    public static short Solve(int x)
    {
        short count = 0;
        while (x != 0)
        {
            count += (short)(x & 1);
            x = (int)((uint)x >> 1);
        }
        return count;
    }

    public static int Run(string[] args) =>
        GenericTest.Run<int, short>(args, "count_bits.tsv", "x", Solve);
}
