using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class Painting
{
    public static List<List<int>> Solve(int arg1, int arg2, List<List<int>> arg3)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "painting.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(int), typeof(int), typeof(List<List<int>>) },
            typeof(List<List<int>>), values => Solve((int)values[0]!, (int)values[1]!, (List<List<int>>)values[2]!));
}
