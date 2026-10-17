using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RoadNetwork
{
    public static (int, int, int) Solve(List<(int, int, int)> arg1, List<(int, int, int)> arg2, int arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "road_network.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(List<(int, int, int)>), typeof(List<(int, int, int)>), typeof(int) },
            typeof((int, int, int)), values => Solve((List<(int, int, int)>)values[0]!, (List<(int, int, int)>)values[1]!, (int)values[2]!));
}
