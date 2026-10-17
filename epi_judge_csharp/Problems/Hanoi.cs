using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Hanoi
{
    public static void Solve(int arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "hanoi.tsv", new[] { "arg1" }, new[] { typeof(int) },
            values => Solve((int)values[0]!));
}
