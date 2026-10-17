using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MaxTeamsInPhotograph
{
    public static int Solve(int arg1, List<(int, int)> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "max_teams_in_photograph.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<(int, int)>) },
            typeof(int), values => Solve((int)values[0]!, (List<(int, int)>)values[1]!));
}
