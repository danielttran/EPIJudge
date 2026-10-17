using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Knapsack
{
    public static int Solve(List<(int, int)> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "knapsack.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<(int, int)>), typeof(int) },
            typeof(int), values => Solve((List<(int, int)>)values[0]!, (int)values[1]!));
}
