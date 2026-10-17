using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsArrayDominated
{
    public static void Solve(List<int> arg1, List<int> arg2, bool arg3, bool arg4)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "is_array_dominated.tsv", new[] { "arg1", "arg2", "arg3", "arg4" }, new[] { typeof(List<int>), typeof(List<int>), typeof(bool), typeof(bool) },
            values => Solve((List<int>)values[0]!, (List<int>)values[1]!, (bool)values[2]!, (bool)values[3]!));
}
