using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class AddingCredits
{
    public static void Solve(List<(string, string, int)> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "adding_credits.tsv", new[] { "arg1" }, new[] { typeof(List<(string, string, int)>) },
            values => Solve((List<(string, string, int)>)values[0]!));
}
