using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class FindSalaryThreshold
{
    public static double Solve(int arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "find_salary_threshold.tsv", new[] { "arg1", "arg2" }, new[] { typeof(int), typeof(List<int>) },
            typeof(double), values => Solve((int)values[0]!, (List<int>)values[1]!));
}
