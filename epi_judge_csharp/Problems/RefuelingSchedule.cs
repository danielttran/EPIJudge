using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class RefuelingSchedule
{
    public static void Solve(List<int> arg1, List<int> arg2)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "refueling_schedule.tsv", new[] { "arg1", "arg2" }, new[] { typeof(List<int>), typeof(List<int>) },
            values => Solve((List<int>)values[0]!, (List<int>)values[1]!));
}
