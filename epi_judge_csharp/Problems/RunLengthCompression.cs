using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RunLengthCompression
{
    public static void Solve(string arg1, string arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "run_length_compression.tsv", new[] { "arg1", "arg2" }, new[] { typeof(string), typeof(string) },
            values => Solve((string)values[0]!, (string)values[1]!));
}
