using EpiJudge.TestFramework;

namespace EpiJudge.Problems;

public static class HuffmanCoding
{
    public static double Solve(List<(string, double)> arg1)
    {
        // TODO - implement this problem.
        return default!;
    }

    public static int Run(string[] args) =>
        GenericTest.Run(args, "huffman_coding.tsv", new[] { "arg1" }, new[] { typeof(List<(string, double)>) },
            typeof(double), values => Solve((List<(string, double)>)values[0]!));
}
