using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class NumberOfTraversalsStaircase
{
    public static int Solve(int arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "number_of_traversals_staircase.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(int) },
            typeof(int), values => Solve((int)values[0]!, (int)values[1]!));
}
