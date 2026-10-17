using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class ReplaceAndRemove
{
    public static List<string> Solve(int arg1, List<string> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "replace_and_remove.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<string>) },
            typeof(List<string>), values => Solve((int)values[0]!, (List<string>)values[1]!));
}
