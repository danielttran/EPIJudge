using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class UniformRandomNumber
{
    public static void Solve(int arg1, int arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "uniform_random_number.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(int) },
            values => Solve((int)values[0]!, (int)values[1]!));
}
