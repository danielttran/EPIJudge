using System.Text.Json;
namespace EpiJudge.Runner;

public sealed record InterviewCakeParameter(string Name, string Type);
public sealed record InterviewCakeDefinition(string Id, string SourceId, string Title, string SourceUrl, string Topic, string Difficulty,
    string Description, string[] Constraints, Example[] Examples, int Position, int TestCount, string ClassName, string Method,
    InterviewCakeParameter[] Params, string Result, string Mode, string Comparison, string BankConventions,
    Dictionary<string, NativeStarter> Starters, Dictionary<string, string> HarnessConfigs, string? Diagram = null, string? DiagramAlt = null);

public static class InterviewCakeCatalog
{
    private static readonly JsonSerializerOptions Json = new() { PropertyNameCaseInsensitive = true };
    public static IReadOnlyList<InterviewCakeDefinition> Definitions { get; } = Load();
    public static IReadOnlyList<Problem> Problems { get; } = Definitions.Select(d => new Problem(
        d.Id, d.Title, d.Topic, d.Difficulty, d.Description, d.Constraints, d.Starters["csharp"].Signature, d.Starters["csharp"].StarterCode, d.Examples, "",
        ArgumentCount: d.Mode is "queue" or "stack" or "trie" or "temperature" or "delete" or "cycle" ? 2 : Math.Max(1, d.Params.Length), TestCount: d.TestCount,
        Comparison: d.Comparison, ResultType: "json", JsSignature: d.Starters["javascript"].Signature, JsStarterCode: d.Starters["javascript"].StarterCode,
        PySignature: d.Starters["python"].Signature, PyStarterCode: d.Starters["python"].StarterCode, Collection: "interviewcake", Position: d.Position,
        Diagram: d.Diagram, DiagramAlt: d.DiagramAlt, SourceUrl: d.SourceUrl, SourceAttribution: "Task identity and compatibility facts: Interview Cake. Bank statements, examples, implementations, adapters and tests are independently authored; no affiliation is implied.")).ToArray();
    private static InterviewCakeDefinition[] Load()
    {
        using var stream = typeof(InterviewCakeCatalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.interviewcake.json") ?? throw new InvalidOperationException("The Interview Cake catalog is missing.");
        var all = JsonSerializer.Deserialize<InterviewCakeDefinition[]>(stream, Json) ?? throw new InvalidOperationException("Invalid Interview Cake catalog.");
        if (all.Length != 41 || all.Select(p => p.Id).Distinct().Count() != 41 || !all.Select(p => p.Position).SequenceEqual(Enumerable.Range(1, 41))) throw new InvalidOperationException("Interview Cake requires exactly 41 distinct ordered coding entries.");
        return all;
    }
    public static InterviewCakeDefinition? Find(string id) => Definitions.FirstOrDefault(d => d.Id == id);
    public static List<TestCase> LoadTests(string root, string id, bool examplesOnly)
    {
        if (Find(id) is null) throw new ArgumentException("Unknown Interview Cake problem.", nameof(id));
        using var doc = JsonDocument.Parse(File.ReadAllText(Path.Combine(root, "interviewcake", "cases", id + ".json")));
        var rows = doc.RootElement.EnumerateArray().Select(r => new TestCase(r.GetProperty("arguments").EnumerateArray().Select(v => v.Clone()).ToArray(), r.GetProperty("expected").Clone()));
        return (examplesOnly ? rows.Take(3) : rows).ToList();
    }
    internal static string Harness(InterviewCakeDefinition definition, string language)
    {
        var file = language switch { "csharp" => "Harness.cs", "java" => "Harness.java", "cpp" => "harness.cpp", "python" => "harness.py", _ => "harness.js" };
        using var stream = typeof(InterviewCakeCatalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.InterviewCakeRuntime." + file) ?? throw new InvalidOperationException("Missing Interview Cake harness " + file);
        using var reader = new StreamReader(stream); var source = reader.ReadToEnd();
        return source.Replace("// CONFIGURATION", definition.HarnessConfigs[language]).Replace("# CONFIGURATION", definition.HarnessConfigs[language]);
    }
}
