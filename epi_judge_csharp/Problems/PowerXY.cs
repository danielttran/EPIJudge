using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PowerXY
{
    public static double Solve(double arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "power_x_y.tsv", new[] { "arg1", "arg2" }, new[] { typeof(double), typeof(int) },
            typeof(double), values => Solve((double)values[0]!, (int)values[1]!));
}
