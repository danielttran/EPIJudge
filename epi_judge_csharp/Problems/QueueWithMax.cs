using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class QueueWithMax
{
    public static void Solve(List<(string, int)> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "queue_with_max.tsv", new[] { "arg1" }, new[] { typeof(List<(string, int)>) },
            values => Solve((List<(string, int)>)values[0]!));
}
