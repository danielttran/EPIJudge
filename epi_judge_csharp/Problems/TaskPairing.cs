using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class TaskPairing
{
    public static List<(int, int)> Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "task_pairing.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(List<(int, int)>), values => Solve((List<int>)values[0]!));
}
