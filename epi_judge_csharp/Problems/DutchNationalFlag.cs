using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class DutchNationalFlag
{
    public static void Solve(List<int> arg1, int arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "dutch_national_flag.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(int) },
            values => Solve((List<int>)values[0]!, (int)values[1]!));
}
