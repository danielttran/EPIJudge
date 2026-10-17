using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ABSqrt2
{
    public static List<double> Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "a_b_sqrt2.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(List<double>), values => Solve((int)values[0]!));
}
