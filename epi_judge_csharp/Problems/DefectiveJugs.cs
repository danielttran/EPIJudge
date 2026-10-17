using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DefectiveJugs
{
    public static bool Solve(List<(int, int)> arg1, int arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "defective_jugs.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(List<(int, int)>), typeof(int), typeof(int) },
            typeof(bool), values => Solve((List<(int, int)>)values[0]!, (int)values[1]!, (int)values[2]!));
}
