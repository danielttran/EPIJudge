using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class NonuniformRandomNumber
{
    public static void Solve(List<int> arg1, List<double> arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "nonuniform_random_number.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(List<double>) },
            values => Solve((List<int>)values[0]!, (List<double>)values[1]!));
}
