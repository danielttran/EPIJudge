using System.Text.Json;

namespace EpiJudge.Runner;

/// <summary>Authored callable semantics shown before a learner opens a solution.</summary>
public static class CallableContractCatalog
{
    private static readonly Lazy<Dictionary<string, Dictionary<string, string[]>>> Entries = new(Load);

    public static string[] Find(string problemId, string language) =>
        Entries.Value.GetValueOrDefault(problemId)?.GetValueOrDefault(language) ?? [];

    private static Dictionary<string, Dictionary<string, string[]>> Load()
    {
        using var stream = typeof(CallableContractCatalog).Assembly
            .GetManifestResourceStream("EpiJudge.Runner.callable-contracts.json")
            ?? throw new InvalidOperationException("The callable contract catalog is missing.");
        var entries = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string[]>>>(stream)
            ?? throw new InvalidOperationException("The callable contract catalog is invalid.");
        if (!entries.Keys.ToHashSet().SetEquals(CallableCodeCatalog.All.Select(entry => entry.ProblemId)))
            throw new InvalidOperationException("Callable contracts must cover every runnable question.");
        foreach (var (problemId, languages) in entries)
        {
            if (languages.Count != SolutionCatalog.Languages.Length ||
                SolutionCatalog.Languages.Any(language => !languages.TryGetValue(language, out var lines) ||
                    lines.Length == 0 || lines.Any(string.IsNullOrWhiteSpace)) ||
                languages.Keys.Any(language => CallableCodeCatalog.Find(problemId, language) is null))
                throw new InvalidOperationException("Incomplete callable contract: " + problemId);
        }
        return entries;
    }
}
