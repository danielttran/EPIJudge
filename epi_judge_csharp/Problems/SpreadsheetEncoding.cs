using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class SpreadsheetEncoding
{
    public static int Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "spreadsheet_encoding.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(int), values => Solve((string)values[0]!));
}
