using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class NearestRepeatedEntries
{
    public static int Solve(List<string> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "nearest_repeated_entries.tsv", new[] { "arg1" }, new[] { typeof(List<string>) },
            typeof(int), values => Solve((List<string>)values[0]!));
}
