using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class MajorityElement
{
    public static string Solve(List<string> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "majority_element.tsv", new[] { "arg1" }, new[] { typeof(List<string>) },
            typeof(string), values => Solve((List<string>)values[0]!));
}
