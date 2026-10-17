using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class IsStringDecomposableIntoWords
{
    public static void Solve(string arg1, HashSet<string> arg2, bool arg3)
    {
        // TODO - implement this problem.
        throw new NotImplementedException();
    }

    public static int Run(string[] args) =>
        GenericTest.RunVoid(args, "is_string_decomposable_into_words.tsv", new[] { "arg1", "arg2", "arg3" }, new[] { typeof(string), typeof(HashSet<string>), typeof(bool) },
            values => Solve((string)values[0]!, (HashSet<string>)values[1]!, (bool)values[2]!));
}
