using System.Text.Json;

namespace EpiJudge.Runner;

public sealed record ProblemSolution(string ProblemId, string Collection, string Language, string Code,
    string Explanation, string TimeComplexity, string SpaceComplexity, string Attribution,
    string? Correctness = null, string? Walkthrough = null, string[]? EdgeCases = null);

public sealed class SolutionCatalog
{
    public static readonly string[] Languages = ["csharp", "javascript", "python", "cpp", "java"];
    private readonly Dictionary<(string ProblemId, string Language), ProblemSolution> solutions;

    public SolutionCatalog(ProblemCatalog problems)
    {
        using var stream=typeof(SolutionCatalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.solutions.json")
            ?? throw new InvalidOperationException("The solution catalog is missing.");
        var entries=JsonSerializer.Deserialize<ProblemSolution[]>(stream,new JsonSerializerOptions {PropertyNameCaseInsensitive=true})
            ?? throw new InvalidOperationException("The solution catalog is invalid.");
        solutions=Validate(problems,entries);
    }

    public static Dictionary<(string ProblemId,string Language),ProblemSolution> Validate(ProblemCatalog problems, IReadOnlyList<ProblemSolution> entries)
    {
        if(entries.Count!=problems.Problems.Count*Languages.Length || entries.Select(e=>(e.ProblemId,e.Language)).Distinct().Count()!=entries.Count)
            throw new InvalidOperationException("Every coding question must have one solution in each supported language.");
        foreach(var entry in entries)
        {
            var problem=problems.Find(entry.ProblemId);
            if(problem is null || entry.Collection!=problem.Collection || !Languages.Contains(entry.Language,StringComparer.Ordinal) ||
                entry.Code.Length>40_000 ||
                new[]{entry.Code,entry.Explanation,entry.TimeComplexity,entry.SpaceComplexity,entry.Attribution}.Any(string.IsNullOrWhiteSpace) ||
                (string.IsNullOrWhiteSpace(entry.Correctness) || string.IsNullOrWhiteSpace(entry.Walkthrough) ||
                    entry.EdgeCases is not {Length:>0} || entry.EdgeCases.Any(string.IsNullOrWhiteSpace)))
                throw new InvalidOperationException("Incomplete solution metadata: "+entry.ProblemId);
        }
        return entries.ToDictionary(e=>(e.ProblemId,e.Language));
    }

    public ProblemSolution? Find(string problemId,string language="csharp")=>solutions.GetValueOrDefault((problemId,language));
}
