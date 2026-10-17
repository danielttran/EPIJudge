using System.Diagnostics;
using System.Text.Json;

namespace EpiJudge.Runner;

public sealed record CaseResult(int Number, bool Passed, string? Input, string? Expected,
    string? Actual, string? Error, double ElapsedMs, bool Hidden);
public sealed record SubmissionResult(string Id, string Status, int Passed, int Total,
    double ElapsedMs, string? Diagnostics, IReadOnlyList<CaseResult> Cases);
internal sealed record ExecutionResult(JsonElement? Actual, string? Error, double ElapsedMs);

public sealed class SubmissionRunner(string repositoryRoot)
{
    private readonly SemaphoreSlim gate = new(1, 1);
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };
    public bool Busy => gate.CurrentCount == 0;

    public async Task<SubmissionResult?> RunAsync(Problem problem, string code, bool examplesOnly, CancellationToken cancellation)
    {
        if (!await gate.WaitAsync(0, cancellation)) return null;
        var id = Guid.NewGuid().ToString("N");
        var directory = Path.Combine(repositoryRoot, ".epi-runs", id);
        var clock = Stopwatch.StartNew();
        try
        {
            var tests = ProblemCatalog.LoadTests(repositoryRoot, problem.Id, examplesOnly);
            Directory.CreateDirectory(directory);
            await File.WriteAllTextAsync(Path.Combine(directory, "Submission.csproj"), ProjectSource, cancellation);
            await File.WriteAllTextAsync(Path.Combine(directory, "NuGet.Config"), "<configuration><packageSources><clear /></packageSources></configuration>", cancellation);
            await File.WriteAllTextAsync(Path.Combine(directory, "Solution.cs"), code, cancellation);
            await File.WriteAllTextAsync(Path.Combine(directory, "Harness.cs"), CreateHarness(problem), cancellation);
            var build = await ProcessHost.RunAsync("dotnet", ["build", "Submission.csproj", "--configuration", "Release", "--nologo", "--verbosity", "quiet", "--disable-build-servers"], directory, null, TimeSpan.FromSeconds(45), cancellation);
            if (build.TimedOut) return Result("Compilation timed out", tests.Count, "The compiler exceeded its 45-second limit.");
            if (build.ExitCode != 0)
                return Result("Compilation error", tests.Count, Sanitize(build.Output + build.Error));
            var input = JsonSerializer.Serialize(tests.Select(test => test.Arguments));
            var execution = await ProcessHost.RunAsync("dotnet", ["bin/Release/net10.0/Submission.dll"], directory, input, TimeSpan.FromSeconds(5), cancellation);
            if (execution.TimedOut) return Result("Time limit exceeded", tests.Count, "Execution exceeded the 5-second limit. Check for an infinite loop.");
            if (execution.OutputLimitExceeded) return Result("Output limit exceeded", tests.Count, "The process produced too much output.");
            if (execution.ExitCode != 0) return Result("Runtime error", tests.Count, Sanitize(execution.Error));
            List<ExecutionResult>? values;
            try { values = JsonSerializer.Deserialize<List<ExecutionResult>>(execution.Output, JsonOptions); }
            catch (JsonException) { return Result("Runtime error", tests.Count, "The submitted program exited without valid judge results."); }
            if (values is null || values.Count != tests.Count)
                return Result("Runtime error", tests.Count, "The submitted program did not finish every test case.");

            var passed = 0;
            var cases = new List<CaseResult>();
            var runtimeError = false;
            for (var i = 0; i < tests.Count; ++i)
            {
                var value = values[i];
                var correct = value.Error is null && value.Actual is { } actual && Equal(tests[i].Expected, actual, problem.Unordered);
                if (correct) ++passed;
                runtimeError |= value.Error is not null;
                // Hidden submissions return counts and a generic failure only; no case contents.
                var hidden = !examplesOnly;
                if (cases.Count < 12 && (examplesOnly || !correct))
                    cases.Add(new(i + 1, correct,
                        hidden ? null : string.Join(", ", tests[i].Arguments.Select(argument => argument.GetRawText())),
                        hidden ? null : tests[i].Expected.GetRawText(),
                        hidden ? null : value.Actual?.GetRawText(),
                        hidden && value.Error is not null ? "Your code threw an exception on this hidden case." : value.Error,
                        value.ElapsedMs, hidden));
            }
            var status = passed == tests.Count ? "Accepted" : runtimeError ? "Runtime error" : "Wrong answer";
            return new(id, status, passed, tests.Count, values.Sum(value => value.ElapsedMs), null, cases);

            SubmissionResult Result(string status, int total, string? diagnostics) =>
                new(id, status, 0, total, clock.Elapsed.TotalMilliseconds, diagnostics, []);
            string Sanitize(string message) => message.Replace(directory + Path.DirectorySeparatorChar, "").Replace(directory, "submission");
        }
        finally
        {
            try { if (Directory.Exists(directory)) Directory.Delete(directory, recursive: true); }
            catch (IOException) { /* A later local cleanup can remove locked build output. */ }
            catch (UnauthorizedAccessException) { }
            gate.Release();
        }
    }

    private static bool Equal(JsonElement expected, JsonElement actual, bool unordered)
    {
        if (expected.ValueKind != actual.ValueKind) return false;
        if (expected.ValueKind != JsonValueKind.Array) return expected.ToString() == actual.ToString();
        var left = expected.EnumerateArray().ToList();
        var right = actual.EnumerateArray().ToList();
        if (left.Count != right.Count) return false;
        if (!unordered) return left.Select((item, i) => Equal(item, right[i], false)).All(match => match);
        foreach (var item in left)
        {
            var index = right.FindIndex(candidate => Equal(item, candidate, true));
            if (index < 0) return false;
            right.RemoveAt(index);
        }
        return true;
    }

    private const string ProjectSource = """
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework>
            <ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable>
            <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
            <StartupObject>JudgeEntryPoint</StartupObject>
          </PropertyGroup>
          <ItemGroup><Compile Include="Solution.cs" /><Compile Include="Harness.cs" /></ItemGroup>
        </Project>
        """;

    private static string CreateHarness(Problem problem) => """
        using System.Diagnostics;
        using System.Text.Json;

        internal static class JudgeEntryPoint
        {
            private static void Main()
            {
                var input = Console.In.ReadToEnd();
                using var document = JsonDocument.Parse(input);
                var output = Console.Out;
                var results = new List<object>();
                foreach (var test in document.RootElement.EnumerateArray())
                {
                    var arguments = test.EnumerateArray().ToArray();
                    var clock = Stopwatch.StartNew();
                    JsonElement? actual = null;
                    string? error = null;
                    try
                    {
                        Console.SetOut(TextWriter.Null);
                        actual = JsonSerializer.SerializeToElement(INVOKE_SOLUTION);
                    }
                    catch (Exception exception)
                    {
                        error = exception.GetType().Name + ": " + exception.Message;
                        if (error.Length > 2000) error = error[..2000];
                    }
                    finally { Console.SetOut(output); }
                    results.Add(new { actual, error, elapsedMs = clock.Elapsed.TotalMilliseconds });
                }
                output.Write(JsonSerializer.Serialize(results));
            }
        }
        """.Replace("INVOKE_SOLUTION", problem.Invocation);
}
