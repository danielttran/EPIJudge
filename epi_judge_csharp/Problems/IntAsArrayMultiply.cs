using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IntAsArrayMultiply
{
    public static List<int> Solve(List<int> arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "int_as_array_multiply.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(List<int>) },
            typeof(List<int>), values => Solve((List<int>)values[0]!, (List<int>)values[1]!));
}
