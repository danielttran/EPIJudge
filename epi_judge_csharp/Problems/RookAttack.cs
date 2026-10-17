using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RookAttack
{
    public static List<List<int>> Solve(List<List<int>> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "rook_attack.tsv", new[] { "arg1" }, new[] { typeof(List<List<int>>) },
            typeof(List<List<int>>), values => Solve((List<List<int>>)values[0]!));
}
