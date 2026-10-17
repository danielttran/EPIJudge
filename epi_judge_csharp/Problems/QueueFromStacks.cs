using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class QueueFromStacks
{
    public static void Solve(List<(string, int)> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "queue_from_stacks.tsv", new[] { "arg1" }, new[] { typeof(List<(string, int)>) },
            values => Solve((List<(string, int)>)values[0]!));
}
