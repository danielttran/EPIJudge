using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Fibonacci
{
    public static int Solve(int arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "fibonacci.tsv", new[] { "arg1" }, new[] { typeof(int) },
            typeof(int), values => Solve((int)values[0]!));
}
