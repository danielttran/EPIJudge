using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class OnlineSampling
{
    public static void Solve(List<int> arg1, int arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "online_sampling.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(int) },
            values => Solve((List<int>)values[0]!, (int)values[1]!));
}
