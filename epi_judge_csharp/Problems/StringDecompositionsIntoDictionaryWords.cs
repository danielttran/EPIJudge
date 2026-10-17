using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class StringDecompositionsIntoDictionaryWords
{
    public static List<int> Solve(string arg1, List<string> arg2)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "string_decompositions_into_dictionary_words.tsv", new[] { "arg1", "arg2" }, new[] { typeof(string), typeof(List<string>) },
            typeof(List<int>), values => Solve((string)values[0]!, (List<string>)values[1]!));
}
