using System.Diagnostics;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using EpiJudge.Runner;

var root = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
ToolchainConfiguration.ApplyLocalOverrides(root);
var positional = args.Where(value => !value.StartsWith("--", StringComparison.Ordinal)).ToArray();
var language = positional.ElementAtOrDefault(0) ?? "all";
var kind = positional.ElementAtOrDefault(1) ?? "all";
var selected = positional.ElementAtOrDefault(2)?.Split(',').ToHashSet();
var format = args.Contains("--legacy") ? CallableCodeCatalog.LegacyFormat : CallableCodeCatalog.CallableFormat;
if (language != "all" && !SolutionCatalog.Languages.Contains(language)) throw new ArgumentException("Choose all or a supported language.");
if (kind is not ("all" or "correct" or "starter")) throw new ArgumentException("Choose all, correct, or starter.");
var definitions = CtciStagingCatalog.Load(root);
if (selected is not null && selected.Any(reference => definitions.All(definition => definition.Ref != reference))) throw new ArgumentException("Unknown staged reference.");
string Sha(string text) => Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text)));
string JsonSha<T>(T value) => Sha(JsonSerializer.Serialize(value));
var assembly = typeof(CtciStagingRunner).Assembly;
foreach (var name in new[] { "CtciStagingCatalog", "CtciStagingGrader", "CtciStagingRunner", "CallableCodeCatalog" })
{
    using var resource = assembly.GetManifestResourceStream("EpiJudge.Runner." + name + ".source") ?? throw new InvalidOperationException("Missing compiled source evidence.");
    using var reader = new StreamReader(resource);
    if (Sha(reader.ReadToEnd()) != Sha(File.ReadAllText(Path.Combine(root, "EpiJudge.Runner", name + ".cs"))))
        throw new InvalidOperationException("Compiled staging code is stale; rebuild the audit project: " + name);
}
string Version(string executable, string argument)
{
    var start = new ProcessStartInfo(executable) { RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false };
    start.ArgumentList.Add(argument);
    using var process = Process.Start(start) ?? throw new InvalidOperationException("Could not inspect toolchain.");
    var output = process.StandardOutput.ReadToEndAsync(); var error = process.StandardError.ReadToEndAsync();
    if (!process.WaitForExit(10000)) { process.Kill(true); throw new TimeoutException("Toolchain version query timed out."); }
    return (output.GetAwaiter().GetResult() + error.GetAwaiter().GetResult()).Trim();
}
var javaHome = Environment.GetEnvironmentVariable("EPI_JAVA_HOME") ?? Environment.GetEnvironmentVariable("JAVA_HOME");
string? OnPath(string name) => (Environment.GetEnvironmentVariable("PATH") ?? "").Split(Path.PathSeparator)
    .Select(directory => Path.Combine(directory, name + (OperatingSystem.IsWindows() ? ".exe" : ""))).FirstOrDefault(File.Exists);
var compiler = Environment.GetEnvironmentVariable("EPI_CPP_COMPILER") ?? OnPath("g++") ?? OnPath("clang++");
var toolchain = new
{
    Platform = RuntimeInformation.OSDescription,
    Framework = RuntimeInformation.FrameworkDescription,
    Dotnet = Version("dotnet", "--version"),
    Node = Version(NodeLocator.FindNode(), "--version"),
    Python = Version(PythonLocator.FindPython(), "--version"),
    Java = Version(javaHome is null ? "java" : Path.Combine(javaHome, "bin", OperatingSystem.IsWindows() ? "java.exe" : "java"), "--version"),
    Cpp = compiler is null ? "MSVC selected by the runner" : Version(compiler, "--version"),
};
var assemblyHash = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(assembly.Location)));
var destination = Path.Combine(root, "ctci6", "runtime", "application-validation.json");
var records = File.Exists(destination)
    ? (JsonSerializer.Deserialize<AuditReport>(File.ReadAllText(destination))?.Executions ?? []).ToDictionary(row => row.Key)
    : new Dictionary<string, AuditExecution>();
var packets = new List<AuditPacket>();
foreach (var definition in definitions)
foreach (var lang in SolutionCatalog.Languages)
foreach (var packetFormat in new[] { CallableCodeCatalog.CallableFormat, CallableCodeCatalog.LegacyFormat })
foreach (var variant in new[] { "correct", "starter" })
{
    var source = definition.Languages[lang];
    var visible = variant == "correct" ? source.SolutionCode : source.StarterCode;
    var code = packetFormat == CallableCodeCatalog.LegacyFormat ? source.Prefix + visible + source.Suffix : visible;
    var key = definition.Ref + "/" + lang + "/" + packetFormat + "/" + variant;
    var fingerprint = JsonSha(new { definition.Ref, definition.Batch, code, source.Prefix, source.Suffix, source.Harness,
        Cases = Sha(File.ReadAllText(Path.Combine(root, "ctci6", definition.StagingDirectory, "cases", definition.Id + ".json"))), assemblyHash, toolchain });
    if (records.TryGetValue(key, out var old) && old.Fingerprint != fingerprint) records.Remove(key);
    packets.Add(new(definition, lang, packetFormat, variant, key, code, fingerprint));
}
var knownKeys = packets.Select(packet => packet.Key).ToHashSet();
foreach (var key in records.Keys.Where(key => !knownKeys.Contains(key)).ToArray()) records.Remove(key);
AuditReport Save(string status)
{
    var current = records.Values.OrderBy(row => row.Key).ToArray();
    var report = new AuditReport(status, "application-runner-staging-only", "pending", definitions.Count * SolutionCatalog.Languages.Length,
        current.Count(row => row.Variant == "correct" && row.Format == CallableCodeCatalog.CallableFormat && row.Status == "Accepted"),
        current.Count(row => row.Variant == "correct" && row.Format == CallableCodeCatalog.LegacyFormat && row.Status == "Accepted"), current);
    File.WriteAllText(destination, JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }) + "\n");
    return report;
}
Save("running");
foreach (var packet in packets.Where(packet => packet.Format == format && (language == "all" || packet.Language == language) &&
    (kind == "all" || packet.Variant == kind) && (selected is null || selected.Contains(packet.Definition.Ref))))
{
    bool Correct(AuditExecution value) => packet.Variant == "correct" ? value.Status == "Accepted" && value.Passed == value.Total : value.Status == "Wrong answer" && value.Passed < value.Total;
    if (records.TryGetValue(packet.Key, out var existing) && Correct(existing)) { Console.WriteLine("REUSE " + packet.Key); continue; }
    Console.WriteLine("RUN " + packet.Key);
    var directory = Path.Combine(root, ".epi-runs", "ctci6-application", packet.Key.Replace('/', '-'));
    var result = await CtciStagingRunner.RunAsync(root, directory, Guid.NewGuid().ToString("N"), packet.Definition, packet.Code, false, packet.Language, CancellationToken.None, packet.Format);
    var record = new AuditExecution(packet.Key, packet.Definition.Ref, packet.Language, packet.Format, packet.Variant, packet.Fingerprint, result.Status, result.Passed, result.Total, result.ElapsedMs);
    records[packet.Key] = record;
    Save("running");
    if (!Correct(record))
    {
        Directory.CreateDirectory(directory);
        File.WriteAllText(Path.Combine(directory, "failure.json"), JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
        Save("failed");
        throw new InvalidOperationException($"{packet.Key}: {result.Status} ({result.Passed}/{result.Total}); see {directory}");
    }
    Console.WriteLine($"PASS {packet.Key}: {record.Passed}/{record.Total}");
}
var final = Save(language == "all" && selected is null ? "passed-selected-format-and-variants" : "passed-selected-scope");
Console.WriteLine(JsonSerializer.Serialize(new { final.Status, final.Stage, final.ExpectedSolutionPairs, final.CallableSolutionPairs, final.LegacySolutionPairs,
    CorrectCaseExecutions = final.Executions.Where(row => row.Variant == "correct" && row.Status == "Accepted").Sum(row => row.Total),
    RejectedStarterExecutions = final.Executions.Count(row => row.Variant == "starter" && row.Status == "Wrong answer") }));

record AuditPacket(CtciStagingDefinition Definition, string Language, string Format, string Variant, string Key, string Code, string Fingerprint);
record AuditExecution(string Key, string Ref, string Language, string Format, string Variant, string Fingerprint, string Status, int Passed, int Total, double ElapsedMs);
record AuditReport(string Status, string Stage, string Publication, int ExpectedSolutionPairs, int CallableSolutionPairs, int LegacySolutionPairs, AuditExecution[] Executions);
