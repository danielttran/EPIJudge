using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DeadlockDetection
{
    public static bool Solve(int arg1, List<(int, int)> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "deadlock_detection.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<(int, int)>) },
            typeof(bool), values => Solve((int)values[0]!, (List<(int, int)>)values[1]!));
}
