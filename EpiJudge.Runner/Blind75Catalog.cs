using System.Text.Json;

namespace EpiJudge.Runner;

public sealed record Blind75Parameter(string Name, string Type);
public sealed record Blind75Definition(string Id, string Title, string Topic, string Difficulty,
    string Description, string[] Constraints, Example[] Examples, int Position, int TestCount,
    string Method, Blind75Parameter[] Params, string Result, string Mode, string Comparison,
    Dictionary<string, NativeStarter> Starters, Dictionary<string, string> HarnessConfigs,
    string? Diagram = null, string? DiagramAlt = null);

public static class Blind75Catalog
{
    private static readonly JsonSerializerOptions Json = new() { PropertyNameCaseInsensitive = true };
    public static IReadOnlyList<Blind75Definition> Definitions { get; } = Load();
    public static IReadOnlyList<Problem> Problems { get; } = Definitions.Select(d => new Problem(
        d.Id, d.Title, d.Topic, d.Difficulty, d.Description, d.Constraints,
        d.Starters["csharp"].Signature, d.Starters["csharp"].StarterCode, d.Examples, "",
        ArgumentCount: d.Params.Length + (d.Mode == "list_cycle" ? 1 : 0), TestCount: d.TestCount,
        Comparison: d.Comparison, ResultType: "json",
        JsSignature: d.Starters["javascript"].Signature, JsStarterCode: d.Starters["javascript"].StarterCode,
        PySignature: d.Starters["python"].Signature, PyStarterCode: d.Starters["python"].StarterCode,
        Collection: "blind75", Position: d.Position, Diagram: d.Diagram, DiagramAlt: d.DiagramAlt)).ToArray();

    private static Blind75Definition[] Load()
    {
        using var stream = typeof(Blind75Catalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.blind75.json")
            ?? throw new InvalidOperationException("The Blind 75 catalog is missing.");
        var definitions = JsonSerializer.Deserialize<Blind75Definition[]>(stream, Json)
            ?? throw new InvalidOperationException("The Blind 75 catalog is invalid.");
        if (definitions.Length != 75 || definitions.Select(d => d.Id).Distinct().Count() != 75 ||
            !definitions.Select(d => d.Position).SequenceEqual(Enumerable.Range(1, 75)))
            throw new InvalidOperationException("The Blind 75 catalog must contain exactly 75 distinct ordered entries.");
        return definitions;
    }

    public static Blind75Definition? Find(string id) => Definitions.FirstOrDefault(d => d.Id == id);

    public static List<TestCase> LoadTests(string root, string id, bool examplesOnly)
    {
        using var document = JsonDocument.Parse(File.ReadAllText(Path.Combine(root, "blind75", "cases", id + ".json")));
        var rows = document.RootElement.EnumerateArray().Select(row => new TestCase(
            row.GetProperty("arguments").EnumerateArray().Select(a => a.Clone()).ToArray(), row.GetProperty("expected").Clone()));
        return (examplesOnly ? rows.Take(3) : rows).ToList();
    }

    internal static string Harness(Blind75Definition problem, string language)
    {
        var file = language switch { "csharp" => "Harness.cs", "java" => "Harness.java", "cpp" => "harness.cpp", "python" => "harness.py", _ => "harness.js" };
        using var stream = typeof(Blind75Catalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.Blind75Runtime." + file)
            ?? throw new InvalidOperationException("Missing Blind 75 harness " + file);
        using var reader = new StreamReader(stream);
        var source = reader.ReadToEnd();
        var generated = language switch
        {
            "csharp" or "java" => source.Replace("// CONFIGURATION", problem.HarnessConfigs[language]),
            "cpp" => source.Replace("// EXECUTE", problem.HarnessConfigs[language]),
            _ => problem.HarnessConfigs[language] + source
        };
        return problem.Mode is "strings_codec" or "tree_codec"
            ? Blind75CodecHarness.Isolate(generated, problem.Mode, language) : generated;
    }
}
