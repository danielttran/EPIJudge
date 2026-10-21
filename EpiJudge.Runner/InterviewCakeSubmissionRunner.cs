using System.Diagnostics;
using System.Text.Json;

namespace EpiJudge.Runner;

// Independent collection runner: existing EPI and Blind 75 contracts are unchanged.
internal static class InterviewCakeSubmissionRunner
{
    internal static async Task<SubmissionResult> RunAsync(string root, string directory, string id,
        Problem problem, InterviewCakeDefinition definition, string code, bool examplesOnly, string language, CancellationToken cancellation)
    {
        language = language switch { "js" => "javascript", "py" => "python", _ => language };
        var clock = Stopwatch.StartNew();
        var tests = InterviewCakeCatalog.LoadTests(root, problem.Id, examplesOnly);
        SubmissionResult Failure(string status, string? diagnostics) => new(id, status, 0, tests.Count, clock.Elapsed.TotalMilliseconds, diagnostics, []);
        string Sanitize(string diagnostic) => diagnostic.Replace(directory, "submission");
        if (!definition.Starters.TryGetValue(language, out var starter)) return Failure("Unsupported language", "Choose a supported programming language.");
        Directory.CreateDirectory(directory);
        await File.WriteAllTextAsync(Path.Combine(directory, starter.Filename), code, cancellation);
        var wireArguments = PrepareArguments(directory, tests, definition);
        await File.WriteAllTextAsync(Path.Combine(directory, "cases.json"), JsonSerializer.Serialize(wireArguments), cancellation);
        var harness = InterviewCakeCatalog.Harness(definition, language);
        string executable;
        string[] arguments;
        ProcessResult? build = null;
        try
        {
            switch (language)
            {
                case "csharp":
                    await File.WriteAllTextAsync(Path.Combine(directory, "Harness.cs"), harness, cancellation);
                    await File.WriteAllTextAsync(Path.Combine(directory, "NuGet.Config"), "<configuration><packageSources><clear /></packageSources></configuration>", cancellation);
                    await File.WriteAllTextAsync(Path.Combine(directory, "Submission.csproj"), """
                        <Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>
                        <OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework>
                        <ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable>
                        <EnableDefaultCompileItems>false</EnableDefaultCompileItems><StartupObject>Harness</StartupObject>
                        </PropertyGroup><ItemGroup><Compile Include="Solution.cs"/><Compile Include="Harness.cs"/></ItemGroup></Project>
                        """, cancellation);
                    build = await ProcessHost.RunAsync("dotnet", ["build", "Submission.csproj", "-c", "Release", "--nologo", "-v", "quiet", "--disable-build-servers", "--maxcpucount:1"], directory, null, TimeSpan.FromSeconds(45), cancellation);
                    executable = "dotnet"; arguments = ["bin/Release/net10.0/Submission.dll"];
                    break;
                case "javascript":
                    await File.WriteAllTextAsync(Path.Combine(directory, "harness.js"), harness, cancellation);
                    executable = NodeLocator.FindNode(); arguments = ["harness.js"];
                    break;
                case "python":
                    await File.WriteAllTextAsync(Path.Combine(directory, "harness.py"), harness, cancellation);
                    executable = PythonLocator.FindPython(); arguments = ["harness.py"];
                    break;
                case "java":
                    await File.WriteAllTextAsync(Path.Combine(directory, "Harness.java"), harness, cancellation);
                    build = await ProcessHost.RunAsync(NativeToolchain.JavaTool("javac"), ["--release", "21", "-encoding", "UTF-8", "-d", "classes", "-sourcepath", Path.Combine(root, "epi_judge_java"), starter.Filename, "Harness.java"], directory, null, TimeSpan.FromSeconds(45), cancellation);
                    executable = NativeToolchain.JavaTool("java"); arguments = ["-Xmx512m", "-cp", "classes", "Harness"];
                    break;
                default:
                    await File.WriteAllTextAsync(Path.Combine(directory, "harness.cpp"), harness, cancellation);
                    executable = Path.Combine(directory, OperatingSystem.IsWindows() ? "submission.exe" : "submission"); arguments = [];
                    var compiler = NativeToolchain.CppCompiler();
                    if (compiler is not null)
                        build = await ProcessHost.RunAsync(compiler, ["-std=c++17", "-O1", "-I", Path.Combine(root, "epi_judge_cpp"), "harness.cpp", "-o", executable], directory, null, TimeSpan.FromSeconds(60), cancellation);
                    else if (OperatingSystem.IsWindows())
                    {
                        var setup = NativeToolchain.VisualStudioSetup();
                        if (setup.IndexOfAny(['\r', '\n', '%', '"']) >= 0) throw new InvalidOperationException("Invalid compiler setup path.");
                        await File.WriteAllTextAsync(Path.Combine(directory, "compile.rsp"), "/nologo /std:c++17 /EHsc /O1 /bigobj /utf-8 /I\"" + Path.Combine(root, "epi_judge_cpp") + "\" harness.cpp /Fesubmission.exe", cancellation);
                        await File.WriteAllTextAsync(Path.Combine(directory, "compile.cmd"), "@echo off\r\ncall \"" + setup + "\" >nul\r\nif errorlevel 1 exit /b %errorlevel%\r\ncl @compile.rsp\r\n", cancellation);
                        build = await ProcessHost.RunAsync("cmd.exe", ["/d", "/c", "compile.cmd"], directory, null, TimeSpan.FromSeconds(60), cancellation);
                    }
                    else throw new FileNotFoundException("Install g++ or clang++ for C++ submissions.");
                    break;
            }
            if (build is { TimedOut: true }) return Failure("Compilation timed out", "The compiler exceeded its time limit.");
            if (build is { OutputLimitExceeded: true }) return Failure("Output limit exceeded", "Compiler output exceeded its limit.");
            if (build is { ExitCode: not 0 }) return Failure("Compilation error", Sanitize(build.Output + build.Error));
            var executionLimit = TimeSpan.FromSeconds(language is "python" or "javascript" ? 30 : 60);
            var execution = await ProcessHost.RunAsync(executable, arguments, directory, null, executionLimit, cancellation);
            if (execution.TimedOut) return Failure("Time limit exceeded", "Execution exceeded its time limit.");
            if (execution.OutputLimitExceeded) return Failure("Output limit exceeded", "Program output exceeded its limit.");
            if (execution.ExitCode != 0) return Failure("Runtime error", examplesOnly ? Sanitize(execution.Error) : "The program exited on a hidden case.");
            var report = Path.Combine(directory, "results.json");
            if (!File.Exists(report)) return Failure("Runtime error", "The program did not produce judge results.");
            if (new FileInfo(report).Length > 16_000_000) return Failure("Output limit exceeded", "Judge results exceeded their limit.");
            var reportText = await File.ReadAllTextAsync(report, cancellation);
            using (var shape = JsonDocument.Parse(reportText))
                if (shape.RootElement.ValueKind != JsonValueKind.Array || shape.RootElement.EnumerateArray().Any(row => row.ValueKind != JsonValueKind.Object || !row.EnumerateObject().Any(p => p.Name.Equals("Actual", StringComparison.OrdinalIgnoreCase)))) return Failure("Runtime error", "The program produced incomplete judge results.");
            var values = JsonSerializer.Deserialize<ExecutionResult[]>(reportText, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            if (values is null || values.Length != tests.Count || values.Any(v => v is null)) return Failure("Runtime error", "The program did not finish every case.");
            var passed = 0; var cases = new List<CaseResult>();
            for (int i = 0; i < tests.Count; i++)
            {
                var value = values[i];
                var actual = value.Actual ?? JsonSerializer.SerializeToElement<object?>(null);
                var ok = !value.ValidationFailed && value.Error is null && Matches(tests[i], actual, definition, wireArguments[i]);
                if (ok) passed++;
                if (cases.Count < 12 && (examplesOnly || !ok)) cases.Add(new(i + 1, ok,
                    examplesOnly ? string.Join(", ", tests[i].Arguments.Select(a => a.GetRawText())) : null,
                    examplesOnly ? tests[i].Expected.GetRawText() : null, examplesOnly ? value.Actual?.GetRawText() : null,
                    examplesOnly ? value.Error : value.Error is null ? null : "Your code threw an exception on a hidden case.", value.ElapsedMs, !examplesOnly));
            }
            return new(id, passed == tests.Count ? "Accepted" : values.Any(v => v.Error is not null && !v.ValidationFailed) ? "Runtime error" : "Wrong answer", passed, tests.Count, values.Sum(v => v.ElapsedMs), null, cases);
        }
        catch (Exception ex) when (ex is FileNotFoundException or System.ComponentModel.Win32Exception)
        { return Failure("Toolchain unavailable", Sanitize(ex.Message)); }
        catch (JsonException) { return Failure("Runtime error", "The program produced invalid judge results."); }
    }

    private static JsonElement[][] PrepareArguments(string directory, List<TestCase> tests, InterviewCakeDefinition definition)
    {
        var result = tests.Select(t => t.Arguments.ToArray()).ToArray();
        if (definition.Mode != "files") return result;
        for (int i = 0; i < tests.Count; i++)
        {
            var fixture = Path.Combine(directory, "filesystem", i.ToString(System.Globalization.CultureInfo.InvariantCulture)); Directory.CreateDirectory(fixture);
            foreach (var file in tests[i].Arguments[0].EnumerateArray())
            {
                var relative = file.GetProperty("path").GetString()!;
                if (Path.IsPathRooted(relative) || relative.Split('/', '\\').Any(part => part is ".." or "." or "")) throw new InvalidOperationException("Unsafe filesystem fixture path.");
                var path = Path.GetFullPath(Path.Combine(fixture, relative));
                if (!path.StartsWith(Path.GetFullPath(fixture) + Path.DirectorySeparatorChar, StringComparison.Ordinal)) throw new InvalidOperationException("Fixture escapes its directory.");
                Directory.CreateDirectory(Path.GetDirectoryName(path)!);
                File.WriteAllBytes(path, file.TryGetProperty("base64", out var encoded) ? Convert.FromBase64String(encoded.GetString()!) : System.Text.Encoding.UTF8.GetBytes(file.GetProperty("content").GetString()!));
                File.SetLastWriteTimeUtc(path, DateTimeOffset.FromUnixTimeSeconds(file.GetProperty("modified").GetInt64()).UtcDateTime);
            }
            result[i] = [JsonSerializer.SerializeToElement(fixture)];
        }
        return result;
    }
    private static bool Matches(TestCase test, JsonElement actual, InterviewCakeDefinition definition, JsonElement[] wire)
    {
        try
        {
            if (definition.Mode == "duplicate") return actual.ValueKind == JsonValueKind.Number && actual.TryGetInt32(out int v) && test.Arguments[0].EnumerateArray().Count(x => x.GetInt32() == v) >= 2;
            if (definition.Mode == "path") return ValidPath(test, actual);
            if (definition.Mode == "temperature") return ValidTemperatures(test, actual);
            if (definition.Mode == "files") return ValidFilePairs(test, actual, wire[0].GetString()!);
            return Equivalent(test.Expected, actual, definition.Comparison == "unordered");
        }
        catch (Exception ex) when (ex is InvalidOperationException or ArgumentException or JsonException or IOException or OverflowException or NotSupportedException) { return false; }
    }
    private static bool Equivalent(JsonElement expected, JsonElement actual, bool unordered = false)
    {
        if (expected.ValueKind != actual.ValueKind) return false;
        if (expected.ValueKind == JsonValueKind.Object)
        {
            var left = expected.EnumerateObject().ToArray(); var right = actual.EnumerateObject().ToArray();
            if (left.Length != right.Length || left.Select(p => p.Name).Distinct(StringComparer.Ordinal).Count() != left.Length || right.Select(p => p.Name).Distinct(StringComparer.Ordinal).Count() != right.Length) return false;
            return left.All(p => actual.TryGetProperty(p.Name, out var value) && Equivalent(p.Value, value));
        }
        if (expected.ValueKind == JsonValueKind.Array)
        {
            var left = expected.EnumerateArray().ToArray(); var right = actual.EnumerateArray().ToList(); if (left.Length != right.Count) return false;
            if (!unordered) return left.Select((value, i) => Equivalent(value, right[i])).All(v => v);
            foreach (var value in left) { int index = right.FindIndex(v => Equivalent(value, v)); if (index < 0) return false; right.RemoveAt(index); }
            return true;
        }
        return SubmissionRunner.Equal(expected, actual, "ordered");
    }
    private static bool ValidPath(TestCase test, JsonElement actual)
    {
        var map = test.Arguments[0]; var start = test.Arguments[1].GetString()!; var end = test.Arguments[2].GetString()!;
        var distance = new Dictionary<string, int> { { start, 0 } }; var queue = new Queue<string>(); queue.Enqueue(start);
        while (queue.TryDequeue(out var node)) foreach (var next in map.GetProperty(node).EnumerateArray().Select(x => x.GetString()!)) if (distance.TryAdd(next, distance[node] + 1)) queue.Enqueue(next);
        if (!distance.TryGetValue(end, out int d)) return actual.ValueKind == JsonValueKind.Null;
        if (actual.ValueKind != JsonValueKind.Array) return false; var path = actual.EnumerateArray().Select(x => x.ValueKind == JsonValueKind.String ? x.GetString() : null).ToArray();
        return path.Length == d + 1 && path[0] == start && path[^1] == end && path.Zip(path.Skip(1)).All(pair => pair.First is not null && map.TryGetProperty(pair.First, out var neighbors) && neighbors.EnumerateArray().Any(x => x.GetString() == pair.Second));
    }
    private static bool ValidTemperatures(TestCase test, JsonElement actual)
    {
        if (actual.ValueKind != JsonValueKind.Array) return false; var ops = test.Arguments[0].EnumerateArray().ToArray(); var args = test.Arguments[1].EnumerateArray().ToArray(); var values = actual.EnumerateArray().ToArray(); if (values.Length != ops.Length) return false;
        var counts = new int[111]; long sum = 0; int count = 0;
        for (int i = 0; i < ops.Length; i++)
        {
            var op = ops[i].GetString(); if (op == "Insert") { int t = args[i][0].GetInt32(); counts[t]++; sum += t; count++; if (values[i].ValueKind != JsonValueKind.Null) return false; continue; }
            if (count == 0) { if (values[i].ValueKind != JsonValueKind.Null) return false; continue; }
            if (op == "GetMean") { if (values[i].ValueKind != JsonValueKind.Number || !values[i].TryGetDouble(out double mean) || !double.IsFinite(mean) || Math.Abs(mean - (double)sum / count) > 1e-9 * Math.Max(1, Math.Abs((double)sum / count))) return false; }
            else if (values[i].ValueKind != JsonValueKind.Number || !values[i].TryGetInt32(out int v) || v < 0 || v > 110 || (op == "GetMode" ? counts[v] != counts.Max() : op == "GetMin" ? v != Array.FindIndex(counts, x => x > 0) : v != Array.FindLastIndex(counts, x => x > 0))) return false;
        }
        return true;
    }
    private static bool ValidFilePairs(TestCase test, JsonElement actual, string fixture)
    {
        if (actual.ValueKind != JsonValueKind.Array) return false;
        static byte[] Bytes(JsonElement file) => file.TryGetProperty("base64", out var b) ? Convert.FromBase64String(b.GetString()!) : System.Text.Encoding.UTF8.GetBytes(file.GetProperty("content").GetString()!);
        static string Fingerprint(byte[] bytes) { int last = Math.Max(0, bytes.Length - 64); return bytes.Length + ":" + string.Join(":", new[] { 0, last / 2, last }.Select(offset => Convert.ToHexString(bytes.AsSpan(offset, Math.Min(64, bytes.Length - offset))))); }
        var files = test.Arguments[0].EnumerateArray().ToDictionary(v => v.GetProperty("path").GetString()!, v => v, StringComparer.Ordinal);
        var expected = files.GroupBy(p => Fingerprint(Bytes(p.Value))).Where(g => g.Count() == 2).Select(g => g.Select(p => p.Key).Order(StringComparer.Ordinal).ToArray()).ToArray();
        var seen = new HashSet<string>(StringComparer.Ordinal);
        foreach (var pair in actual.EnumerateArray())
        {
            if (pair.ValueKind != JsonValueKind.Array || pair.GetArrayLength() != 2 || pair[0].ValueKind != JsonValueKind.String || pair[1].ValueKind != JsonValueKind.String) return false;
            var paths = pair.EnumerateArray().Select(p => p.GetString()!).ToArray(); if (paths.Any(p => !Path.IsPathRooted(p))) return false;
            var names = paths.Select(p => Path.GetRelativePath(fixture, p).Replace('\\', '/')).ToArray(); if (names[0] == names[1] || names.Any(p => !files.ContainsKey(p))) return false;
            if (Fingerprint(Bytes(files[names[0]])) != Fingerprint(Bytes(files[names[1]]))) return false;
            if (files[names[0]].GetProperty("modified").GetInt64() > files[names[1]].GetProperty("modified").GetInt64()) return false;
            if (!seen.Add(string.Join("\0", names.Order(StringComparer.Ordinal)))) return false;
        }
        return seen.SetEquals(expected.Select(p => string.Join("\0", p)));
    }
}
