using System.Diagnostics;
using System.Text.Json;

namespace EpiJudge.Runner;

// This separate runner leaves every EPI wrapper, TSV, and grading contract intact.
internal static class Blind75SubmissionRunner
{
    internal static async Task<SubmissionResult> RunAsync(string root, string directory, string id,
        Problem problem, Blind75Definition definition, string code, bool examplesOnly, string language, CancellationToken cancellation)
    {
        language = language switch { "js" => "javascript", "py" => "python", _ => language };
        var clock = Stopwatch.StartNew();
        var tests = Blind75Catalog.LoadTests(root, problem.Id, examplesOnly);
        SubmissionResult Failure(string status, string? diagnostics) => new(id, status, 0, tests.Count, clock.Elapsed.TotalMilliseconds, diagnostics, []);
        string Sanitize(string diagnostic) => diagnostic.Replace(directory, "submission");
        if (!definition.Starters.TryGetValue(language, out var starter)) return Failure("Unsupported language", "Choose a supported programming language.");
        Directory.CreateDirectory(directory);
        await File.WriteAllTextAsync(Path.Combine(directory, starter.Filename), code, cancellation);
        await File.WriteAllTextAsync(Path.Combine(directory, "cases.json"), JsonSerializer.Serialize(tests.Select(t => t.Arguments)), cancellation);
        var harness = Blind75Catalog.Harness(definition, language);
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
            var isCodec = definition.Mode is "strings_codec" or "tree_codec";
            var executionLimit = TimeSpan.FromSeconds(language is "python" or "javascript" ? 30 : 60);
            var executionClock = Stopwatch.StartNew();
            ExecutionResult[]? values = null;
            foreach (var phase in isCodec ? new[] { "encode", "decode" } : new[] { "normal" })
            {
                if (isCodec) await File.WriteAllTextAsync(Path.Combine(directory, "codec-phase.txt"), phase, cancellation);
                var remaining = executionLimit - executionClock.Elapsed;
                if (remaining <= TimeSpan.Zero) return Failure("Time limit exceeded", "Execution exceeded its time limit.");
                var execution = await ProcessHost.RunAsync(executable, arguments, directory, null, remaining, cancellation);
                if (execution.TimedOut) return Failure("Time limit exceeded", "Execution exceeded its time limit.");
                if (execution.OutputLimitExceeded) return Failure("Output limit exceeded", "Program output exceeded its limit.");
                if (execution.ExitCode != 0) return Failure("Runtime error", examplesOnly ? Sanitize(execution.Error) : "The program exited on a hidden case.");
                var report = Path.Combine(directory, "results.json");
                if (!File.Exists(report)) return Failure("Runtime error", "The program did not produce judge results.");
                if (new FileInfo(report).Length > 16_000_000) return Failure("Output limit exceeded", "Judge results exceeded their limit.");
                values = JsonSerializer.Deserialize<ExecutionResult[]>(await File.ReadAllTextAsync(report, cancellation), new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                if (values is null || values.Length != tests.Count || values.Any(v => v is null)) return Failure("Runtime error", "The program did not finish every case.");
                if (phase == "encode")
                {
                    if (values.Any(v => v.Error is not null)) return Failure("Runtime error", "The encoder threw an exception.");
                    if (values.Any(v => v.ValidationFailed || v.Actual is not { ValueKind: JsonValueKind.String }))
                        return Failure("Wrong answer", "The encoder violates its string or input-preservation contract.");
                    // A second process receives only encoded strings. Static fields, module
                    // globals and original node references cannot stand in for serialized data.
                    await File.WriteAllTextAsync(Path.Combine(directory, "cases.json"),
                        JsonSerializer.Serialize(values.Select(v => new[] { v.Actual!.Value })), cancellation);
                    File.Delete(report);
                }
            }
            if (values is null) return Failure("Runtime error", "The program did not produce judge results.");
            var passed = 0; var cases = new List<CaseResult>();
            for (int i = 0; i < tests.Count; i++)
            {
                var value = values[i];
                var ok = !value.ValidationFailed && value.Error is null && value.Actual is { } actual &&
                    (definition.Comparison == "alien" ? AlienOrder(tests[i], actual) : SubmissionRunner.Equal(tests[i].Expected, actual, definition.Comparison));
                if (ok) passed++;
                if (cases.Count < 12 && (examplesOnly || !ok)) cases.Add(new(i + 1, ok,
                    examplesOnly ? string.Join(", ", tests[i].Arguments.Select(a => a.GetRawText())) : null,
                    examplesOnly ? tests[i].Expected.GetRawText() : null, examplesOnly ? value.Actual?.GetRawText() : null,
                    examplesOnly ? value.Error : value.Error is null ? null : "Your code threw an exception on a hidden case.", value.ElapsedMs, !examplesOnly));
            }
            return new(id, passed == tests.Count ? "Accepted" : values.Any(v => v.Error is not null) ? "Runtime error" : "Wrong answer", passed, tests.Count, values.Sum(v => v.ElapsedMs), null, cases);
        }
        catch (Exception ex) when (ex is FileNotFoundException or System.ComponentModel.Win32Exception)
        { return Failure("Toolchain unavailable", Sanitize(ex.Message)); }
        catch (JsonException) { return Failure("Runtime error", "The program produced invalid judge results."); }
    }

    private static bool AlienOrder(TestCase test, JsonElement actual)
    {
        if (actual.ValueKind != JsonValueKind.String) return false;
        var order = actual.GetString()!;
        if (test.Expected.GetString() == "") return order == "";
        var words = test.Arguments[0].EnumerateArray().Select(v => v.GetString()!).ToArray();
        var chars = words.SelectMany(w => w).ToHashSet();
        if (order.Length != chars.Count || order.Distinct().Count() != order.Length || !chars.SetEquals(order)) return false;
        var rank = order.Select((c, i) => (c, i)).ToDictionary(p => p.c, p => p.i);
        for (int i = 1; i < words.Length; i++)
        {
            var left = words[i - 1]; var right = words[i]; var j = 0;
            while (j < Math.Min(left.Length, right.Length) && left[j] == right[j]) j++;
            if (j == Math.Min(left.Length, right.Length) ? left.Length > right.Length : rank[left[j]] > rank[right[j]]) return false;
        }
        return true;
    }
}
