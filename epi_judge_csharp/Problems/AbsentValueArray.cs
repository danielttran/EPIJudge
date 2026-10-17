using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class AbsentValueArray
{
    public static void Solve(List<int> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "absent_value_array.tsv", new[] { "arg1" }, new[] { typeof(List<int>) },
            values => Solve((List<int>)values[0]!));
}
