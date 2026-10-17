using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class GraphClone
{
    public static void Solve(int arg1, List<(int, int)> arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "graph_clone.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<(int, int)>) },
            values => Solve((int)values[0]!, (List<(int, int)>)values[1]!));
}
