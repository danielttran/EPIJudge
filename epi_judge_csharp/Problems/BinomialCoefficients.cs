using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class BinomialCoefficients
{
    public static int Solve(int arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "binomial_coefficients.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(int) },
            typeof(int), values => Solve((int)values[0]!, (int)values[1]!));
}
