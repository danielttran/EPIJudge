using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class StringIntegerInterconversion
{
    public static void Solve(int arg1, string arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "string_integer_interconversion.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(string) },
            values => Solve((int)values[0]!, (string)values[1]!));
}
