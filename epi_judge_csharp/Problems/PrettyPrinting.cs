using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PrettyPrinting
{
    public static int Solve(List<string> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "pretty_printing.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<string>), typeof(int) },
            typeof(int), values => Solve((List<string>)values[0]!, (int)values[1]!));
}
