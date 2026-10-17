using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class EnumeratePalindromicDecompositions
{
    public static List<List<string>> Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "enumerate_palindromic_decompositions.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(List<List<string>>), values => Solve((string)values[0]!));
}
