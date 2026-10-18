using System.Diagnostics;
using System.Text;
using System.Text.Json;

namespace EpiJudge.Runner;

internal sealed record NativeCase(int Number, string Status, string? Actual, string? Error, double ElapsedMs);

internal static class NativeSubmissionRunner
{
    internal static async Task<SubmissionResult> RunAsync(string root, string directory, string id,
        Problem problem, string code, bool examplesOnly, string language, CancellationToken cancellation)
    {
        var clock = Stopwatch.StartNew();
        var tests = ProblemCatalog.LoadTests(root, problem.Id, examplesOnly);
        SubmissionResult Failure(string status, string? diagnostic) =>
            new(id, status, 0, tests.Count, clock.Elapsed.TotalMilliseconds, diagnostic, []);
        string Sanitize(string value) => value.Replace(directory, "submission");
        try
        {
            var native = new NativeProblemCatalog(root).Get(language, problem.Id);
            Directory.CreateDirectory(directory);
            Directory.CreateDirectory(Path.Combine(directory, "test_data"));
            var lines = File.ReadLines(Path.Combine(root, "test_data", problem.Id + ".tsv"));
            await File.WriteAllLinesAsync(Path.Combine(directory, "test_data", problem.Id + ".tsv"),
                examplesOnly ? lines.Take(4) : lines, cancellation);
            await File.WriteAllTextAsync(Path.Combine(directory, "config.json"),
                "{\"timeoutSeconds\":0,\"numFailedTestsBeforeStop\":0}", cancellation);

            ProcessResult build;
            string executable;
            string[] runArguments;
            if (language == "java")
            {
                var sourcePath = Path.Combine(directory, "epi", native.Starter.Filename);
                Directory.CreateDirectory(Path.GetDirectoryName(sourcePath)!);
                await File.WriteAllTextAsync(sourcePath, code, cancellation);
                var framework = Path.Combine(directory, "epi", "test_framework", "GenericTest.java");
                Directory.CreateDirectory(Path.GetDirectoryName(framework)!);
                var original = await File.ReadAllTextAsync(Path.Combine(root, "epi_judge_java", "epi", "test_framework", "GenericTest.java"), cancellation);
                var start = original.IndexOf("  private static TestResult runTests(", StringComparison.Ordinal);
                var end = original.IndexOf("  @SuppressWarnings(\"unchecked\")", start, StringComparison.Ordinal);
                if (start < 0 || end < 0) throw new InvalidOperationException("The Java framework changed; update its web bridge.");
                await File.WriteAllTextAsync(framework, original[..start] + Resource("java_run_tests.txt") + original[end..], cancellation);
                Directory.CreateDirectory(Path.Combine(directory, "classes"));
                build = await ProcessHost.RunAsync(NativeToolchain.JavaTool("javac"),
                    ["-encoding", "UTF-8", "--release", "21", "-parameters", "-d", "classes", "-sourcepath",
                     directory + Path.PathSeparator + Path.Combine(root, "epi_judge_java"), framework, sourcePath],
                    directory, null, TimeSpan.FromSeconds(45), cancellation);
                executable = NativeToolchain.JavaTool("java");
                runArguments = ["-Xmx512m", "-cp", "classes", "epi." + Path.GetFileNameWithoutExtension(native.SourcePath),
                    "--test-data-dir", "test_data", "--no-tty", "--no-color", "--no-update-js"];
            }
            else
            {
                // The supplied wrapper stays in the editor; only its judge entry point changes in the temporary copy.
                code = code.Replace("\"test_framework/generic_test.h\"", "\"web_test.h\"")
                    .Replace("GenericTestMain(", "WebGenericTestMain(");
                await File.WriteAllTextAsync(Path.Combine(directory, "solution.cpp"), code, cancellation);
                await File.WriteAllTextAsync(Path.Combine(directory, "web_test.h"), Resource("web_test.h"), cancellation);
                executable = Path.Combine(directory, OperatingSystem.IsWindows() ? "submission.exe" : "submission");
                runArguments = [];
                var compiler = NativeToolchain.CppCompiler();
                if (compiler is not null)
                    build = await ProcessHost.RunAsync(compiler,
                        ["-std=c++17", "-O1", "-pthread", "-I", Path.Combine(root, "epi_judge_cpp"), "solution.cpp", "-o", executable],
                        directory, null, TimeSpan.FromSeconds(60), cancellation);
                else if (OperatingSystem.IsWindows())
                {
                    var setup = NativeToolchain.VisualStudioSetup();
                    // Paths go in a response file; submission source is never interpreted by a shell.
                    await File.WriteAllTextAsync(Path.Combine(directory, "compile.rsp"),
                        "/nologo /std:c++17 /EHsc /O1 /bigobj /D_WINDOWS /D_CRT_SECURE_NO_WARNINGS /utf-8 /I\"" +
                        Path.Combine(root, "epi_judge_cpp") + "\" solution.cpp /Fesubmission.exe", cancellation);
                    if (setup.IndexOfAny(['\r', '\n', '%', '"']) >= 0) throw new InvalidOperationException("Invalid Visual Studio setup path.");
                    await File.WriteAllTextAsync(Path.Combine(directory, "compile.cmd"),
                        "@echo off\r\ncall \"" + setup + "\" >nul\r\nif errorlevel 1 exit /b %errorlevel%\r\ncl @compile.rsp\r\n", Encoding.ASCII, cancellation);
                    build = await ProcessHost.RunAsync("cmd.exe", ["/d", "/c", "compile.cmd"], directory, null, TimeSpan.FromSeconds(60), cancellation);
                }
                else throw new FileNotFoundException("Install g++ or clang++ for C++ submissions.");
            }
            if (build.TimedOut) return Failure("Compilation timed out", "The native compiler exceeded its time limit.");
            if (build.OutputLimitExceeded) return Failure("Output limit exceeded", "Compiler output exceeded its limit.");
            if (build.ExitCode != 0) return Failure("Compilation error", Sanitize(build.Output + build.Error));

            var execution = await ProcessHost.RunAsync(executable, runArguments, directory, null, TimeSpan.FromSeconds(60), cancellation);
            if (execution.TimedOut) return Failure("Time limit exceeded", "Execution exceeded the 60-second limit. Check for an infinite loop.");
            if (execution.OutputLimitExceeded) return Failure("Output limit exceeded", "The process produced too much output.");
            if (execution.ExitCode != 0) return Failure("Runtime error", examplesOnly ? Sanitize(execution.Error) : "The submitted program exited on a hidden case.");
            var reportPath = Path.Combine(directory, "native-results.jsonl");
            if (!File.Exists(reportPath)) return Failure("Runtime error", "The submitted program did not produce judge results.");
            if (new FileInfo(reportPath).Length > 16_000_000) return Failure("Output limit exceeded", "Judge results exceeded their limit.");
            var results = File.ReadLines(reportPath).Select(line => JsonSerializer.Deserialize<NativeCase>(line,
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true })!).ToArray();
            if (results.Length != tests.Count || results.Where((row, i) => row is null || row.Number != i + 1).Any())
                return Failure("Runtime error", "The submitted program did not finish every test case.");
            var passed = results.Count(row => row.Status == "Accepted");
            var status = passed == tests.Count ? "Accepted"
                : results.Any(row => row.Status == "Time limit exceeded") ? "Time limit exceeded"
                : results.Any(row => row.Status == "Runtime error") ? "Runtime error" : "Wrong answer";
            var cases = results.Where(row => examplesOnly || row.Status != "Accepted").Take(12).Select(row =>
            {
                var test = tests[row.Number - 1];
                return new CaseResult(row.Number, row.Status == "Accepted",
                    examplesOnly ? string.Join(", ", test.Arguments.Select(arg => arg.GetRawText())) : null,
                    examplesOnly ? test.Expected.GetRawText() : null,
                    examplesOnly ? row.Actual : null,
                    examplesOnly ? row.Error : row.Status == "Runtime error" ? "Your code threw an exception on this hidden case." : null,
                    row.ElapsedMs, !examplesOnly);
            }).ToArray();
            return new(id, status, passed, tests.Count, results.Sum(row => row.ElapsedMs), null, cases);
        }
        catch (Exception ex) when (ex is FileNotFoundException or System.ComponentModel.Win32Exception)
        {
            return Failure("Toolchain unavailable", Sanitize(ex.Message));
        }
        catch (JsonException)
        {
            return Failure("Runtime error", "The submitted program produced invalid judge results.");
        }
    }

    private static string Resource(string name)
    {
        using var stream = typeof(NativeSubmissionRunner).Assembly.GetManifestResourceStream("EpiJudge.Runner.NativeHarnesses." + name)
            ?? throw new InvalidOperationException("Missing native harness: " + name);
        using var reader = new StreamReader(stream);
        return reader.ReadToEnd();
    }
}
