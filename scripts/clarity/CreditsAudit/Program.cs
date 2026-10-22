using System.Text.Json;
using System.Text.RegularExpressions;
using EpiJudge.Runner;

var root = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
var selected = args.SingleOrDefault(a => a.StartsWith("--language="))?.Split('=')[1];
var languages = SolutionCatalog.Languages.Where(l => selected is null || selected == l).ToArray();
if (languages.Length == 0) throw new ArgumentException("Unknown language.");
var temporary = Path.Combine(Path.GetTempPath(), "epijudge-credits-contract-" + Guid.NewGuid().ToString("N"));
Directory.CreateDirectory(Path.Combine(temporary, "test_data"));
void Copy(string source, string destination)
{
    Directory.CreateDirectory(destination);
    foreach (var file in Directory.GetFiles(source)) File.Copy(file, Path.Combine(destination, Path.GetFileName(file)));
    foreach (var directory in Directory.GetDirectories(source).Where(p => Path.GetFileName(p) is not ("__pycache__" or "build")))
        Copy(directory, Path.Combine(destination, Path.GetFileName(directory)));
}
var results = new List<object>();
try
{
    foreach (var folder in new[] { "epi_judge_cpp", "epi_judge_java", "epi_judge_python" }) Copy(Path.Combine(root, folder), Path.Combine(temporary, folder));
    var problem = new ProblemCatalog().Find("adding_credits")!;
    var header = File.ReadLines(Path.Combine(root, "test_data/adding_credits.tsv")).First();
    var runner = new SubmissionRunner(temporary);
    foreach (var language in languages)
    foreach (var (value, empty, accepted) in new[] { ("Nora", false, true), ("Zoe", false, true), ("Lower", false, false), ("Missing", false, false), ("", false, false), ("", true, true), ("Nora", true, false) })
    {
        // Expected IDs intentionally name Nora; Zoe is equally valid. A faulty
        // Lookup is never queried and must not serve as the Max oracle.
        var operations = empty ? "[[\"ClientsCreditsInfo\",\"\",0],[\"max\",\"\",0]]"
            : "[[\"ClientsCreditsInfo\",\"\",0],[\"insert\",\"Nora\",10],[\"insert\",\"Zoe\",10],[\"insert\",\"Lower\",2],[\"add_all\",\"\",-3],[\"max\",\"Nora\",0]]";
        File.WriteAllText(Path.Combine(temporary, "test_data/adding_credits.tsv"), header + "\n" + operations + "\tcredits regression\n");
        var entry = CallableCodeCatalog.Find(problem.Id, language)!;
        var code = entry.SolutionCode;
        var quoted = JsonSerializer.Serialize(value);
        var replacement = language switch
        {
            "csharp" => ("ranking.Count == 0 ? \"\" : ranking.Max.Id", quoted),
            "javascript" => ("return node.id;", "return " + quoted + ";"),
            "python" => ("return max(self.credits, key=self.credits.get) if self.credits else \"\"", "return " + quoted),
            "cpp" => ("return ranking_.empty() ? std::string{} : ranking_.rbegin()->second;", "return " + quoted + ";"),
            "java" => ("return ranking.isEmpty() ? \"\" : ranking.last().client;", "return " + quoted + ";"),
            _ => throw new InvalidOperationException()
        };
        if (!code.Contains(replacement.Item1, StringComparison.Ordinal)) throw new InvalidOperationException("Max source changed: update focused fixture: " + language);
        code = code.Replace(replacement.Item1, replacement.Item2, StringComparison.Ordinal);
        // JavaScript's original empty guard is appropriate for the empty test;
        // replace it for the intentionally wrong nonempty response when empty.
        if (language == "javascript" && empty && value.Length > 0) code = code.Replace("if (!node) return \"\";", "if (!node) return " + quoted + ";");
        if (language == "csharp")
            code = Regex.Replace(code, @"public int Lookup\([^;]+;", "public int Lookup(string clientId) => 7;");
        else if (language == "python")
            code = Regex.Replace(code, @"def lookup\([^\n]+\n +return[^\n]+", "def lookup(self, client_id):\n        return 7");
        else
        {
            var signature = language switch { "cpp" => "int Lookup(", "java" => "public int lookup(", _ => "lookup(clientId)" };
            var begin = code.IndexOf('{', code.IndexOf(signature, StringComparison.Ordinal));
            var end = begin + 1;
            var depth = 1;
            while (depth > 0) { if (code[end] == '{') depth++; if (code[end] == '}') depth--; end++; }
            code = code[..(begin + 1)] + " return 7; " + code[(end - 1)..];
        }
        var prepared = CallableCodeCatalog.Prepare(problem.Id, language, code, CallableCodeCatalog.CallableFormat);
        var result = await runner.RunAsync(problem with { TestCount = 1 }, prepared.Code, false, language, CancellationToken.None);
        var expectedStatus = accepted ? "Accepted" : "Wrong answer";
        if (result?.Status != expectedStatus) throw new InvalidOperationException($"{language}/{value}/empty={empty}: expected {expectedStatus}, got {result?.Status}: {result?.Diagnostics}");
        results.Add(new { language, returned = value, empty, accepted, status = result.Status });
        Console.WriteLine($"PASS credits contract {language} return={quoted} empty={empty} {expectedStatus}");
    }
    Directory.CreateDirectory(Path.Combine(root, ".epi-runs"));
    File.WriteAllText(Path.Combine(root, ".epi-runs/credits-contract-" + (selected ?? "all") + ".json"), JsonSerializer.Serialize(new { passed = true, results }, new JsonSerializerOptions { WriteIndented = true }) + "\n");
}
finally { Directory.Delete(temporary, recursive: true); }
