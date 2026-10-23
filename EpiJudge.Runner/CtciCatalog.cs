using System.Text.Json;
using System.Text.RegularExpressions;

namespace EpiJudge.Runner;

// Only the explicitly reviewed/exported practice snapshot enters the library.
// Unfinished authoring rows in ctci6/staged* never register themselves here.
public static class CtciCatalog
{
    private static readonly JsonSerializerOptions Json = new() { PropertyNameCaseInsensitive = true };
    public static IReadOnlyList<CtciStagingDefinition> Definitions { get; } = Read<CtciStagingDefinition[]>("runtime");
    public static IReadOnlyList<Problem> Problems { get; } = LoadProblems();

    private static T Read<T>(string resource) where T : class
    {
        using var stream = typeof(CtciCatalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.ctci6-" + resource + ".json")
            ?? throw new InvalidOperationException("Missing CtCI practice resource: " + resource);
        return JsonSerializer.Deserialize<T>(stream, Json) ?? throw new InvalidOperationException("Invalid CtCI practice resource.");
    }

    private static Problem[] LoadProblems()
    {
        var rows = Read<Problem[]>("problems");
        var coverage = Read<PracticeCoverage>("coverage");
        if (rows.Length == 0 || rows.Length != coverage.Questions || coverage.SolutionPairs != rows.Length * SolutionCatalog.Languages.Length ||
            rows.Select(row => row.Id).Distinct().Count() != rows.Length || Definitions.Count != rows.Length ||
            !rows.Select(row => row.Id).ToHashSet().SetEquals(Definitions.Select(row => row.Id)) ||
            !rows.Select(row => row.Position).SequenceEqual(Enumerable.Range(1, rows.Length)))
            throw new InvalidOperationException("Incomplete reviewed CtCI practice snapshot.");
        foreach (var definition in Definitions)
        {
            var problem = rows.Single(row => row.Id == definition.Id);
            if (!Regex.IsMatch(definition.Ref, @"^[1-9]\d*\.[1-9]\d*$") || definition.Id != "ctci6_" + definition.Ref.Replace('.', '_') ||
                definition.StagingDirectory != "" || problem.Collection != "ctci6" || problem.TestCount != definition.TestCount ||
                definition.TestCount < 1 || !definition.Languages.Keys.ToHashSet().SetEquals(SolutionCatalog.Languages) ||
                definition.Languages.Values.Any(value => new[] { value.Signature, value.StarterCode, value.SolutionCode, value.Harness }.Any(string.IsNullOrWhiteSpace)))
                throw new InvalidOperationException("Invalid reviewed CtCI entry: " + definition.Id);
        }
        return rows;
    }

    public static CtciStagingDefinition? Find(string id) => Definitions.FirstOrDefault(row => row.Id == id);
    public static List<TestCase> LoadTests(string root, string id, bool examplesOnly) =>
        (Find(id) ?? throw new ArgumentException("Unknown CtCI coding problem.", nameof(id))).Tests(root, examplesOnly);
    public static NativeStarter NativeStarter(string id, string language)
    {
        var definition = Find(id) ?? throw new ArgumentException("Unknown CtCI coding problem.", nameof(id));
        var callable = definition.Callable(language);
        return new(callable.Signature, callable.Prefix + callable.StarterCode + callable.Suffix, callable.Filename, language == "cpp" ? "C++17" : "Java 21");
    }

    private sealed record PracticeCoverage(int Questions, int SolutionPairs);
}
