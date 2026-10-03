using EpiJudge.Problems;

if (args.Length == 0)
{
    Console.Error.WriteLine("Usage: dotnet run --project epi_judge_csharp -- <problem> [judge options]");
    Console.Error.WriteLine("Problems: anagrams, count_bits");
    return 2;
}

var judgeArgs = args[1..];
return args[0] switch
{
    "anagrams" => Anagrams.Run(judgeArgs),
    "count_bits" => CountBits.Run(judgeArgs),
    _ => UnknownProblem(args[0]),
};

static int UnknownProblem(string problem)
{
    Console.Error.WriteLine($"Unknown problem: {problem}");
    return 2;
}
