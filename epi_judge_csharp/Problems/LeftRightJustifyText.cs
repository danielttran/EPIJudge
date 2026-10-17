using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LeftRightJustifyText
{
    public static List<string> Solve(List<string> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "left_right_justify_text.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<string>), typeof(int) },
            typeof(List<string>), values => Solve((List<string>)values[0]!, (int)values[1]!));
}
