using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class AdvanceByOffsets
{
    public static bool Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "advance_by_offsets.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            typeof(bool), values => Solve((List<int>)values[0]!));
}
