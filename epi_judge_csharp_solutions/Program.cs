using EpiJudge.Solutions;

if (args.Length == 0)
{
    Console.Error.WriteLine("Usage: dotnet run --project epi_judge_csharp_solutions -- <problem> [judge options]");
    return 2;
}

var judgeArgs = args[1..];
return args[0] switch
{
    "anagrams" => Anagrams.Run(judgeArgs),
    "count_bits" => CountBits.Run(judgeArgs),
    _ => 2,
};
