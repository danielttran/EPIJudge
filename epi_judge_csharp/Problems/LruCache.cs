using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class LruCache
{
    public static void Solve(List<(string, int, int)> arg1)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "lru_cache.tsv", new[] { "arg1" }, new[] { typeof(List<(string, int, int)>) },
            values => Solve((List<(string, int, int)>)values[0]!));
}
