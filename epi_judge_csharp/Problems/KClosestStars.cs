using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class KClosestStars
{
    public static List<double> Solve(List<(double, double, double)> arg1, int arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "k_closest_stars.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<(double, double, double)>), typeof(int) },
            typeof(List<double>), values => Solve((List<(double, double, double)>)values[0]!, (int)values[1]!));
}
