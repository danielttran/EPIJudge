using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class OfflineSampling
{
    public static void Solve(int arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "offline_sampling.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<int>) },
            values => Solve((int)values[0]!, (List<int>)values[1]!));
}
