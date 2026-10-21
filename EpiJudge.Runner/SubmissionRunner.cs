using System.Diagnostics;
using System.Text.Json;
using EpiJudge.TestFramework;

namespace EpiJudge.Runner;

public sealed record CaseResult(int Number, bool Passed, string? Input, string? Expected,
    string? Actual, string? Error, double ElapsedMs, bool Hidden);
public sealed record SubmissionResult(string Id, string Status, int Passed, int Total,
    double ElapsedMs, string? Diagnostics, IReadOnlyList<CaseResult> Cases);
internal sealed record ExecutionResult(JsonElement? Actual, string? Error, double ElapsedMs,
    bool ValidationFailed = false, string? ValidationMessage = null);

public interface ISubmissionRunner
{
    Task<SubmissionResult?> RunAsync(Problem problem, string code, bool examplesOnly, string language, CancellationToken cancellation);
}

public sealed class SubmissionRunner(string repositoryRoot) : ISubmissionRunner
{
    private readonly SemaphoreSlim gate = new(1, 1);
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };
    public bool Busy => gate.CurrentCount == 0;

    public Task<SubmissionResult?> RunAsync(Problem problem, string code, bool examplesOnly, CancellationToken cancellation) =>
        RunAsync(problem, code, examplesOnly, "csharp", cancellation);

    public async Task<SubmissionResult?> RunAsync(Problem problem, string code, bool examplesOnly, string language, CancellationToken cancellation)
    {
        if (!await gate.WaitAsync(0, cancellation)) return null;
        var id = Guid.NewGuid().ToString("N");
        var directory = Path.Combine(repositoryRoot, ".epi-runs", id);
        var clock = Stopwatch.StartNew();
        try
        {
            if (Blind75Catalog.Find(problem.Id) is { } blind)
                return await Blind75SubmissionRunner.RunAsync(repositoryRoot, directory, id, problem, blind, code, examplesOnly, language, cancellation);
            if (InterviewCakeCatalog.Find(problem.Id) is { } cake)
                return await InterviewCakeSubmissionRunner.RunAsync(repositoryRoot, directory, id, problem, cake, code, examplesOnly, language, cancellation);
            if (language is "cpp" or "java")
                return await NativeSubmissionRunner.RunAsync(repositoryRoot, directory, id, problem, code, examplesOnly, language, cancellation);
            if (language is not ("csharp" or "javascript" or "js" or "python" or "py"))
                return new(id, "Unsupported language", 0, 0, 0, "Choose a supported programming language.", []);
            var tests = ProblemCatalog.LoadTests(repositoryRoot, problem.Id, examplesOnly);
            Directory.CreateDirectory(directory);
            var isJs = language.Equals("javascript", StringComparison.OrdinalIgnoreCase) ||
                       language.Equals("js", StringComparison.OrdinalIgnoreCase);
            var isPy = language.Equals("python", StringComparison.OrdinalIgnoreCase) ||
                       language.Equals("py", StringComparison.OrdinalIgnoreCase);

            ProcessResult execution;
            if (isJs)
            {
                var wrappedCode = code + "\n" +
                    $"if (typeof {problem.JsInvocation} !== 'undefined' && (!module.exports || !module.exports.{problem.JsInvocation})) {{ module.exports.{problem.JsInvocation} = {problem.JsInvocation}; }}";
                await File.WriteAllTextAsync(Path.Combine(directory, "solution.js"), wrappedCode, cancellation);
                await File.WriteAllTextAsync(Path.Combine(directory, "harness.js"), CreateJsHarness(problem), cancellation);
                var input = JsonSerializer.Serialize(tests.Select(test => test.Arguments));
                var node = NodeLocator.FindNode();
                execution = await ProcessHost.RunAsync(node, ["harness.js"], directory, input, TimeSpan.FromSeconds(30), cancellation);
            }
            else if (isPy)
            {
                await File.WriteAllTextAsync(Path.Combine(directory, "solution.py"), code, cancellation);
                await File.WriteAllTextAsync(Path.Combine(directory, "harness.py"), CreatePyHarness(problem, repositoryRoot, examplesOnly), cancellation);
                var py = PythonLocator.FindPython();
                execution = await ProcessHost.RunAsync(py, ["harness.py"], directory, null, PythonExecutionBudget(problem.Id), cancellation);
            }
            else
            {
                await File.WriteAllTextAsync(Path.Combine(directory, "Submission.csproj"), CreateProject(), cancellation);
                await File.WriteAllTextAsync(Path.Combine(directory, "NuGet.Config"), "<configuration><packageSources><clear /></packageSources></configuration>", cancellation);
                await File.WriteAllTextAsync(Path.Combine(directory, "Solution.cs"), code, cancellation);
                await File.WriteAllTextAsync(Path.Combine(directory, "Harness.cs"), CreateHarness(problem), cancellation);
                var build = await ProcessHost.RunAsync("dotnet", ["build", "Submission.csproj", "--configuration", "Release", "--nologo", "--verbosity", "quiet", "--disable-build-servers", "--maxcpucount:1"], directory, null, TimeSpan.FromSeconds(45), cancellation);
                if (build.TimedOut) return Result("Compilation timed out", tests.Count, "The compiler exceeded its 45-second limit.");
                if (build.ExitCode != 0)
                    return Result("Compilation error", tests.Count, Sanitize(build.Output + build.Error));
                var input = JsonSerializer.Serialize(tests.Select(test => test.Arguments));
                execution = await ProcessHost.RunAsync("dotnet", ["bin/Release/net10.0/Submission.dll"], directory, input, TimeSpan.FromSeconds(60), cancellation);
            }

            if (execution.TimedOut) return Result("Time limit exceeded", tests.Count, "Execution exceeded the time limit. Check for an infinite loop.");
            if (execution.OutputLimitExceeded) return Result("Output limit exceeded", tests.Count, "The process produced too much output.");
            if (execution.ExitCode != 0) return Result("Runtime error", tests.Count, Sanitize(execution.Error));
            List<ExecutionResult>? values;
            try { values = JsonSerializer.Deserialize<List<ExecutionResult>>(execution.Output, JsonOptions); }
            catch (JsonException) { return Result("Runtime error", tests.Count, "The submitted program exited without valid judge results: " + Sanitize(execution.Error)); }
            if (values is null || values.Count != tests.Count)
                return Result("Runtime error", tests.Count, "The submitted program did not finish every test case.");

            var passed = 0;
            var cases = new List<CaseResult>();
            var runtimeError = false;
            for (var i = 0; i < tests.Count; ++i)
            {
                var value = values[i];
                var correct = !value.ValidationFailed && value.Error is null && value.Actual is { } actual && Equal(tests[i].Expected, actual,
                    problem.Unordered ? "nested" : problem.Comparison);
                if (correct) ++passed;
                runtimeError |= value.Error is not null;
                // Hidden submissions return counts and a generic failure only; no case contents.
                var hidden = !examplesOnly;
                if (cases.Count < 12 && (examplesOnly || !correct))
                    cases.Add(new(i + 1, correct,
                        hidden ? null : string.Join(", ", tests[i].Arguments.Select(argument => argument.GetRawText())),
                        hidden ? null : tests[i].Expected.GetRawText(),
                        hidden ? null : value.Actual?.GetRawText(),
                        hidden ? value.Error is not null ? "Your code threw an exception on this hidden case."
                            : value.ValidationFailed ? "The result violates the problem contract on this hidden case." : null
                            : value.Error ?? value.ValidationMessage,
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

    internal static bool Equal(JsonElement expected, JsonElement actual, string comparison)
    {
        if (expected.ValueKind != actual.ValueKind) return false;
        if (expected.ValueKind == JsonValueKind.Number)
        {
            if (expected.TryGetInt64(out long e) && actual.TryGetInt64(out long a)) return e == a;
            double leftNumber = expected.GetDouble(), rightNumber = actual.GetDouble();
            return double.IsFinite(rightNumber) && Math.Abs(leftNumber-rightNumber) <= 1e-9*Math.Max(1, Math.Abs(leftNumber));
        }
        if (expected.ValueKind != JsonValueKind.Array) return expected.ToString() == actual.ToString();
        var left = expected.EnumerateArray().ToList();
        var right = actual.EnumerateArray().ToList();
        if (left.Count != right.Count) return false;
        if (comparison == "ordered") return left.Select((item, i) => Equal(item, right[i], "ordered")).All(match => match);
        foreach (var item in left)
        {
            var index = right.FindIndex(candidate => Equal(item, candidate, comparison == "nested" ? "nested" : "ordered"));
            if (index < 0) return false;
            right.RemoveAt(index);
        }
        return true;
    }

    private static string CreateProject() => """
        <Project Sdk="Microsoft.NET.Sdk">
          <PropertyGroup>
            <OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework>
            <ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable>
            <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
            <StartupObject>JudgeEntryPoint</StartupObject>
          </PropertyGroup>
          <ItemGroup><Compile Include="Solution.cs" /><Compile Include="Harness.cs" /></ItemGroup>
          <ItemGroup>
            <Reference Include="EpiJudge.Runner"><HintPath>RUNNER_PATH</HintPath></Reference>
            <Reference Include="EpiJudge.TestFramework"><HintPath>FRAMEWORK_PATH</HintPath></Reference>
          </ItemGroup>
        </Project>
        """.Replace("RUNNER_PATH", System.Security.SecurityElement.Escape(typeof(SubmissionRunner).Assembly.Location))
           .Replace("FRAMEWORK_PATH", System.Security.SecurityElement.Escape(typeof(JudgeJson).Assembly.Location));

    private static string CreateHarness(Problem problem) => """
        using System.Diagnostics;
        using System.Text.Json;
        using EpiJudge.Runner;
        using EpiJudge.TestFramework;

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
                    bool validationFailed = false;
                    string? validationMessage = null;
                    try
                    {
                        Console.SetOut(TextWriter.Null);
                        actual = JsonSerializer.SerializeToElement(INVOKE_SOLUTION, JudgeJson.Options);
                    }
                    catch (JudgeValidationException exception)
                    {
                        validationFailed = true;
                        validationMessage = exception.Message.Length > 2000 ? exception.Message[..2000] : exception.Message;
                    }
                    catch (Exception exception)
                    {
                        error = exception.GetType().Name + ": " + exception.Message;
                        if (error.Length > 2000) error = error[..2000];
                    }
                    finally { Console.SetOut(output); }
                    results.Add(new { actual, error, validationFailed, validationMessage, elapsedMs = clock.Elapsed.TotalMilliseconds });
                }
                output.Write(JsonSerializer.Serialize(results));
            }
        }
        """.Replace("INVOKE_SOLUTION", problem.Invocation);

    private static string CreateJsHarness(Problem problem)
    {
        using var stream=typeof(SubmissionRunner).Assembly.GetManifestResourceStream("EpiJudge.Runner.EpiJavascriptHarness.js")
            ?? throw new InvalidOperationException("The JavaScript protocol harness is missing.");
        using var reader=new StreamReader(stream);
        return reader.ReadToEnd()
            .Replace("__TARGET_NAME__",JsonSerializer.Serialize(problem.JsInvocation ?? "solution"))
            .Replace("__PROBLEM_ID__",JsonSerializer.Serialize(problem.Id))
            .Replace("__ARGUMENT_TYPES_JSON__",JsonSerializer.Serialize(problem.ArgumentTypes ?? []))
            .Replace("__RESULT_TYPE__",JsonSerializer.Serialize(problem.ResultType));
    }

    // These original EPI wrappers deliberately perform 100,000 to 1,000,000
    // statistical trials per case, including validation outside the timed algorithm.
    // Retain their full sample sizes while keeping ordinary Python submissions bounded.
    internal static TimeSpan PythonExecutionBudget(string problemId) => TimeSpan.FromSeconds(problemId is
        "random_permutation" or "random_subset" or "online_sampling" or "offline_sampling" or
        "nonuniform_random_number" or "uniform_random_number" ? 180 : 30);

    private static string CreatePyHarness(Problem problem, string repositoryRoot, bool examplesOnly)
    {
        var pySourceFile = problem.PySourceFile ?? $"{problem.Id}.py";
        var pyInvocation = problem.PyInvocation ?? problem.Id;
        var limit = examplesOnly ? "[:3]" : "";
        var repoRootEscaped = repositoryRoot.Replace("\\", "/");

        return $$"""
            import sys, os, time, json, ast, importlib.util
            from pathlib import Path

            sys.path.insert(0, "{{repoRootEscaped}}/epi_judge_python")

            from test_framework.test_utils import split_tsv_file
            from test_framework.generic_test_handler import GenericTestHandler
            from test_framework.test_failure import TestFailure

            # Load the reference problem module
            ref_path = Path("{{repoRootEscaped}}/epi_judge_python/{{pySourceFile}}")
            spec = importlib.util.spec_from_file_location("ref_problem_mod", ref_path)
            ref_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ref_mod)

            # Preserve the original task comparator before user symbols are overlaid.
            comparator = None
            for call in ast.walk(ast.parse(ref_path.read_text(encoding="utf-8"))):
                if not isinstance(call, ast.Call):
                    continue
                called = call.func.attr if isinstance(call.func, ast.Attribute) else call.func.id if isinstance(call.func, ast.Name) else ""
                if called != "generic_test_main":
                    continue
                expression = call.args[3] if len(call.args) > 3 else next((item.value for item in call.keywords if item.arg == "comparator"), None)
                if expression is not None:
                    comparator = eval(compile(ast.Expression(expression), str(ref_path), "eval"), ref_mod.__dict__)
                break

            # Execute user's solution
            sol_path = Path("solution.py")
            user_env = {}
            with open(sol_path, "r", encoding="utf-8") as f:
                user_code = f.read()

            try:
                exec(user_code, user_env)
            except Exception as e:
                # If syntax error or import error on user code, report failure
                err_msg = f"{type(e).__name__}: {e}"
                print(json.dumps([{"actual": None, "error": err_msg, "validationFailed": False, "validationMessage": None, "elapsedMs": 0}]))
                sys.exit(0)

            # Override symbols from user code into reference module
            for k, v in user_env.items():
                if not k.startswith("_"):
                    setattr(ref_mod, k, v)

            # Find target function/wrapper
            target_name = "{{pyInvocation}}"
            target_fn = getattr(ref_mod, target_name, None)
            if target_fn is None:
                # Fallback: check if generic_test_main target was something else
                for attr in dir(ref_mod):
                    if attr.endswith("_wrapper") or attr.endswith("_tester") or attr == target_name:
                        target_fn = getattr(ref_mod, attr)
                        break

            if target_fn is None:
                target_fn = getattr(ref_mod, "{{problem.Id}}", None)

            if target_fn is None:
                err_msg = f"Error: Could not find function {target_name} in solution."
                print(json.dumps([{"actual": None, "error": err_msg, "validationFailed": False, "validationMessage": None, "elapsedMs": 0}]))
                sys.exit(0)

            tsv_path = Path("{{repoRootEscaped}}/test_data/{{problem.Id}}.tsv")
            test_data = split_tsv_file(str(tsv_path))
            handler = GenericTestHandler(target_fn, comparator)
            handler.parse_signature(test_data[0])

            def serialize_val(v):
                if v is None or isinstance(v, (bool, int, float, str)):
                    return v
                if isinstance(v, (list, tuple)):
                    return [serialize_val(x) for x in v]
                if isinstance(v, set):
                    return sorted([serialize_val(x) for x in v])
                if hasattr(v, '__iter__') and not isinstance(v, dict):
                    return [serialize_val(x) for x in v]
                return str(v)

            results = []
            selected_rows = test_data[1:]{{limit}}
            for row in selected_rows:
                t0 = time.perf_counter()
                actual = None
                error = None
                validation_failed = False
                validation_message = None

                try:
                    # GenericTestHandler handles conversion, comparison, and raises TestFailure
                    test_out = handler.run_test(15, lambda m, *args: m, row[:-1])
                    # If it passed without TestFailure, get expected value as actual
                    expected_raw = row[-2] if not handler.expected_is_void() else "true"
                    try:
                        actual = json.loads(expected_raw)
                    except Exception:
                        actual = True
                    # EPI allows trailing nulls in level-order tree fixtures. Match
                    # the outer judge's canonical representation after the original
                    # framework has checked the actual returned tree structurally.
                    if {{(problem.ResultType.StartsWith("binary_tree(", StringComparison.Ordinal) ? "True" : "False")}} and isinstance(actual, list):
                        while actual and actual[-1] is None:
                            actual.pop()
                except TestFailure as tf:
                    validation_failed = True
                    validation_message = str(tf)[:2000]
                    # Check if result property exists on TestFailure
                    for p in getattr(tf, '_properties', []):
                        if callable(getattr(p, 'name', None)) and p.name() == 'result':
                            actual = serialize_val(p.value())
                            break
                except Exception as ex:
                    error = f"{type(ex).__name__}: {ex}"[:2000]

                dt = (time.perf_counter() - t0) * 1000
                results.append({
                    "actual": actual,
                    "error": error,
                    "validationFailed": validation_failed,
                    "validationMessage": validation_message,
                    "elapsedMs": dt
                })

            print(json.dumps(results))
            """;
    }
}
