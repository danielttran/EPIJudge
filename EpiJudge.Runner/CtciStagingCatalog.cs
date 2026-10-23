using System.Text.Json;
using System.Text.RegularExpressions;

namespace EpiJudge.Runner;

// Unpublished authoring entries are explicit inputs to staging audits. They do
// not enter ProblemCatalog, the website library, progress, or draft inventories.
public sealed record CtciStagingLanguage(string Signature, string StarterCode, string SolutionCode,
    string Prefix, string Suffix, string Harness, string Reference);

public sealed record CtciStagingDefinition(string Id, string Ref, string Title, string Description,
    string[] Constraints, string Method, string[][] Params, string Result, string Mutation,
    int TestCount, int Batch, string StagingDirectory, JsonElement Example,
    Dictionary<string, CtciStagingLanguage> Languages)
{
    public CallableCodeDefinition Callable(string language)
    {
        var source = Languages[language];
        var extension = language switch { "csharp" => "cs", "javascript" => "js", "python" => "py", "cpp" => "cpp", _ => "java" };
        var filename = (language is "csharp" or "java" ? "Solution." : "solution.") + extension;
        CodeReference[] references = string.IsNullOrWhiteSpace(source.Reference) ? [] :
            [new(Batch == 2 ? "Required linked-list node API" : "Required state and error APIs", source.Reference, Batch == 2 ? ["LinkedListNode"] : [Method, "BankError", "Animal", "IntStack"])];
        return new(Id, language, filename, source.Signature, source.StarterCode,
            source.SolutionCode, source.Prefix, source.Suffix, references);
    }

    public List<TestCase> Tests(string root, bool examplesOnly)
    {
        var path = Path.Combine(root, "ctci6", StagingDirectory, "cases", Id + ".json");
        using var document = JsonDocument.Parse(File.ReadAllText(path));
        var rows = document.RootElement.EnumerateArray().Select(row => new TestCase(
            row.GetProperty("arguments").EnumerateArray().Select(value => value.Clone()).ToArray(),
            row.GetProperty("expected").Clone())).ToList();
        if (rows.Count != TestCount) throw new InvalidOperationException("Staged CtCI case count differs: " + Id);
        return examplesOnly ? rows.Take(1).ToList() : rows;
    }
}

public static class CtciStagingCatalog
{
    public static IReadOnlyList<CtciStagingDefinition> Load(string root)
    {
        var path = Path.Combine(root, "ctci6", "runtime", "catalog.json");
        var rows = JsonSerializer.Deserialize<CtciStagingDefinition[]>(File.ReadAllText(path),
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
            ?? throw new InvalidOperationException("Missing staged CtCI definitions.");
        if (rows.Select(row => row.Id).Distinct().Count() != rows.Length)
            throw new InvalidOperationException("Duplicate staged CtCI identity.");
        foreach (var row in rows)
        {
            if (!Regex.IsMatch(row.Ref, @"^[1-9]\d*\.[1-9]\d*$") || row.Id != "ctci6_" + row.Ref.Replace('.', '_') ||
                row.StagingDirectory != (row.Batch switch { 1 => "staged", 2 => "staged02", 3 => "staged03", _ => "" }) || row.Batch is not (1 or 2 or 3) ||
                row.TestCount < 1 || !row.Languages.Keys.ToHashSet().SetEquals(SolutionCatalog.Languages) ||
                row.Example.ValueKind != JsonValueKind.Array || row.Example.GetArrayLength() != 2 ||
                row.Languages.Values.Any(value => new[] { value.Signature, value.StarterCode, value.SolutionCode, value.Harness }.Any(string.IsNullOrWhiteSpace)))
                throw new InvalidOperationException("Invalid staged CtCI definition: " + row.Id);
        }
        return rows;
    }
}
