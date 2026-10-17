using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PrimeSieve
{
    public static List<int> Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "prime_sieve.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(List<int>), values => Solve((int)values[0]!));
}
