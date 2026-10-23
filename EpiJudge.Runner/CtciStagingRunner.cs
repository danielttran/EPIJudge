using System.Diagnostics;
using System.Text.Json;

namespace EpiJudge.Runner;

// Explicit staging execution. This never registers partially authored questions
// in the website or changes the existing collection runners.
public static class CtciStagingRunner
{
    public static async Task<SubmissionResult> RunAsync(string root, string parentDirectory, string id,
        CtciStagingDefinition definition, string code, bool examplesOnly, string language,
        CancellationToken cancellation, string? codeFormat = CallableCodeCatalog.CallableFormat)
    {
        language = language switch { "js" => "javascript", "py" => "python", _ => language };
        var clock = Stopwatch.StartNew();
        var tests = definition.Tests(root, examplesOnly);
        SubmissionResult Failure(string status, string? message) => new(id, status, 0, tests.Count, clock.Elapsed.TotalMilliseconds, message, []);
        if (!definition.Languages.TryGetValue(language, out var source)) return Failure("Unsupported language", "Choose a supported programming language.");
        if (!CallableCodeCatalog.ValidFormat(codeFormat)) return Failure("Invalid code format", "Choose a supported code format.");
        if (string.IsNullOrWhiteSpace(code) || code.Length > 40_000) return Failure("Invalid code", "Code must contain between 1 and 40,000 characters.");
        var callable = definition.Callable(language);
        var prepared = codeFormat is null or CallableCodeCatalog.LegacyFormat ? code : CallableCodeCatalog.PrepareCallable(callable, code).Code;
        // Fresh modules also prevent a cached Python import or old results file
        // from being reused when an audit retries the same question/language.
        var directory = Path.Combine(parentDirectory, Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(directory);
        string Sanitize(string text) => text.Replace(directory, "submission");
        await File.WriteAllTextAsync(Path.Combine(directory, callable.Filename), prepared, cancellation);
        await File.WriteAllTextAsync(Path.Combine(directory, "cases.json"), JsonSerializer.Serialize(tests.Select(test =>
            new { @ref = definition.Ref, arguments = test.Arguments })), cancellation);
        string executable;
        string[] arguments;
        ProcessResult? compilation = null;
        try
        {
            switch (language)
            {
                case "csharp":
                    await File.WriteAllTextAsync(Path.Combine(directory, "Harness.cs"), source.Harness, cancellation);
                    await File.WriteAllTextAsync(Path.Combine(directory, "NuGet.Config"), "<configuration><packageSources><clear /></packageSources></configuration>", cancellation);
                    await File.WriteAllTextAsync(Path.Combine(directory, "Submission.csproj"), """
                        <Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>
                        <OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework>
                        <ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable>
                        <EnableDefaultCompileItems>false</EnableDefaultCompileItems><StartupObject>Harness</StartupObject>
                        </PropertyGroup><ItemGroup><Compile Include="Solution.cs"/><Compile Include="Harness.cs"/></ItemGroup></Project>
                        """, cancellation);
                    compilation = await ProcessHost.RunAsync("dotnet", ["build", "Submission.csproj", "-c", "Release", "--nologo", "-v", "quiet", "--disable-build-servers", "--maxcpucount:1"], directory, null, TimeSpan.FromSeconds(45), cancellation);
                    executable = "dotnet"; arguments = ["bin/Release/net10.0/Submission.dll"];
                    break;
                case "javascript":
                    await File.WriteAllTextAsync(Path.Combine(directory, "harness.js"), source.Harness, cancellation);
                    executable = NodeLocator.FindNode(); arguments = ["harness.js"];
                    break;
                case "python":
                    await File.WriteAllTextAsync(Path.Combine(directory, "harness.py"), source.Harness, cancellation);
                    executable = PythonLocator.FindPython(); arguments = ["harness.py"];
                    break;
                case "java":
                    await File.WriteAllTextAsync(Path.Combine(directory, "Harness.java"), source.Harness, cancellation);
                    compilation = await ProcessHost.RunAsync(NativeToolchain.JavaTool("javac"), ["--release", "21", "-encoding", "UTF-8", "-d", "classes", "-sourcepath", Path.Combine(root, "epi_judge_java"), callable.Filename, "Harness.java"], directory, null, TimeSpan.FromSeconds(45), cancellation);
                    executable = NativeToolchain.JavaTool("java"); arguments = ["-Xmx512m", "-cp", "classes", "Harness"];
                    break;
                default:
                    await File.WriteAllTextAsync(Path.Combine(directory, "harness.cpp"), source.Harness, cancellation);
                    executable = Path.Combine(directory, OperatingSystem.IsWindows() ? "submission.exe" : "submission"); arguments = [];
                    var compiler = NativeToolchain.CppCompiler();
                    if (compiler is not null)
                        compilation = await ProcessHost.RunAsync(compiler, ["-std=c++17", "-O1", "-I", Path.Combine(root, "epi_judge_cpp"), "harness.cpp", "-o", executable], directory, null, TimeSpan.FromSeconds(60), cancellation);
                    else if (OperatingSystem.IsWindows())
                    {
                        var setup = NativeToolchain.VisualStudioSetup();
                        if (setup.IndexOfAny(['\r', '\n', '%', '"']) >= 0) throw new InvalidOperationException("Invalid compiler setup path.");
                        await File.WriteAllTextAsync(Path.Combine(directory, "compile.rsp"), "/nologo /std:c++17 /EHsc /O1 /bigobj /utf-8 /I\"" + Path.Combine(root, "epi_judge_cpp") + "\" harness.cpp /Fesubmission.exe", cancellation);
                        await File.WriteAllTextAsync(Path.Combine(directory, "compile.cmd"), "@echo off\r\ncall \"" + setup + "\" >nul\r\nif errorlevel 1 exit /b %errorlevel%\r\ncl @compile.rsp\r\n", cancellation);
                        compilation = await ProcessHost.RunAsync("cmd.exe", ["/d", "/c", "compile.cmd"], directory, null, TimeSpan.FromSeconds(60), cancellation);
                    }
                    else throw new FileNotFoundException("Install g++ or clang++ for C++ submissions.");
                    break;
            }
            if (compilation is { TimedOut: true }) return Failure("Compilation timed out", "The compiler exceeded its time limit.");
            if (compilation is { OutputLimitExceeded: true }) return Failure("Output limit exceeded", "Compiler output exceeded its limit.");
            if (compilation is { ExitCode: not 0 }) return Failure("Compilation error", Sanitize(compilation.Output + compilation.Error));
            var execution = await ProcessHost.RunAsync(executable, arguments, directory, null, TimeSpan.FromSeconds(60), cancellation);
            if (execution.TimedOut) return Failure("Time limit exceeded", "Execution exceeded its time limit.");
            if (execution.OutputLimitExceeded) return Failure("Output limit exceeded", "Program output exceeded its limit.");
            if (execution.ExitCode != 0) return Failure("Runtime error", examplesOnly ? Sanitize(execution.Error) : "The program exited on a hidden case.");
            var report = Path.Combine(directory, "results.json");
            if (!File.Exists(report)) return Failure("Runtime error", "The program did not finish the judge report.");
            if (new FileInfo(report).Length > 16_000_000) return Failure("Output limit exceeded", "Judge results exceeded their limit.");
            using var results = JsonDocument.Parse(await File.ReadAllTextAsync(report, cancellation));
            if (results.RootElement.ValueKind != JsonValueKind.Array || results.RootElement.GetArrayLength() != tests.Count)
                return Failure("Runtime error", "The program did not finish every case.");
            int passed = 0; double elapsed = 0; bool runtimeError = false;
            var cases = new List<CaseResult>();
            for (int i = 0; i < tests.Count; i++)
            {
                var row = results.RootElement[i];
                var observed = row.GetProperty("observation");
                double milliseconds = row.GetProperty("elapsedMs").GetDouble();
                if (!double.IsFinite(milliseconds) || milliseconds < 0) return Failure("Runtime error", "The judge report contains an invalid measured time.");
                elapsed += milliseconds;
                bool threw = observed.TryGetProperty("error", out var error) && error.ValueKind != JsonValueKind.Null;
                runtimeError |= threw;
                var reason = CtciStagingGrader.FailureReason(definition, tests[i], observed);
                if (reason is null) passed++;
                if (cases.Count < 12 && (examplesOnly || reason is not null))
                    cases.Add(new(i + 1, reason is null,
                        examplesOnly ? string.Join(", ", tests[i].Arguments.Select(value => value.GetRawText())) : null,
                        examplesOnly ? tests[i].Expected.GetRawText() : null,
                        examplesOnly ? CtciStagingGrader.Display(definition, tests[i], observed).GetRawText() : null,
                        threw ? examplesOnly ? Sanitize(error.ToString()) : "Your code threw an exception on a hidden case." : reason,
                        milliseconds, !examplesOnly));
            }
            return new(id, passed == tests.Count ? "Accepted" : runtimeError ? "Runtime error" : "Wrong answer", passed, tests.Count, elapsed, null, cases);
        }
        catch (Exception error) when (error is FileNotFoundException or System.ComponentModel.Win32Exception)
        {
            return Failure("Toolchain unavailable", Sanitize(error.Message));
        }
        catch (Exception error) when (error is JsonException or InvalidOperationException or KeyNotFoundException)
        {
            return Failure("Runtime error", "The program produced an invalid or incomplete judge report.");
        }
    }
}
