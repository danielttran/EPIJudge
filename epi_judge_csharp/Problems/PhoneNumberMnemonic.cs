using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class PhoneNumberMnemonic
{
    public static List<string> Solve(string arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "phone_number_mnemonic.tsv", new[] { "arg1" }, new[] { typeof(string) },
            typeof(List<string>), values => Solve((string)values[0]!),
            (expected, actual) => GenericTest.UnorderedEquals(expected, actual, typeof(List<string>)));
}
