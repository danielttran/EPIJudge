using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class NumberOfScoreCombinations
{
    public static int Solve(int arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "number_of_score_combinations.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<int>) },
            typeof(int), values => Solve((int)values[0]!, (List<int>)values[1]!));
}
