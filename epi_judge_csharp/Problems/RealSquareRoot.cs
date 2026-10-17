using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RealSquareRoot
{
    public static double Solve(double arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "real_square_root.tsv", new[] { "arg1" }, new[] { typeof(double) },
            typeof(double), values => Solve((double)values[0]!));
}
