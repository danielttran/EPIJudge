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
                execution = await ProcessHost.RunAsync(py, ["harness.py"], directory, null, TimeSpan.FromSeconds(30), cancellation);
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

    private static bool Equal(JsonElement expected, JsonElement actual, string comparison)
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

    private static readonly HashSet<string> CustomJsProblems =
    [
        "absent_value_array", "alternating_array", "even_odd_array", "dutch_national_flag",
        "gray_code", "run_length_compression", "string_integer_interconversion", "reverse_list",
        "pivot_list", "is_list_cyclic", "circular_queue", "stack_with_max", "queue_from_stacks",
        "queue_with_max", "lru_cache", "adding_credits"
    ];

    private static string CreateJsHarness(Problem problem)
    {
        var isCustom = CustomJsProblems.Contains(problem.Id);
        var targetName = problem.JsInvocation ?? "solution";

        var argConversions = new System.Text.StringBuilder();
        if (problem.ArgumentTypes is { Length: > 0 } argTypes)
        {
            for (var i = 0; i < argTypes.Length; i++)
            {
                var type = argTypes[i];
                if (type.StartsWith("linked_list"))
                    argConversions.AppendLine($"if (Array.isArray(convertedArgs[{i}])) convertedArgs[{i}] = arrayToListNode(convertedArgs[{i}]);");
                else if (type.StartsWith("binary_tree"))
                    argConversions.AppendLine($"if (Array.isArray(convertedArgs[{i}])) convertedArgs[{i}] = arrayToBinaryTree(convertedArgs[{i}]);");
                else if (type.StartsWith("set"))
                    argConversions.AppendLine($"if (Array.isArray(convertedArgs[{i}])) convertedArgs[{i}] = new Set(convertedArgs[{i}]);");
            }
        }

        var template = """
            const fs = require('fs');
            const { performance } = require('perf_hooks');

            class JudgeValidationException extends Error {
                constructor(message) {
                    super(message);
                    this.name = 'JudgeValidationException';
                }
            }

            function check(condition, message = 'The result violates the problem contract.') {
                if (!condition) throw new JudgeValidationException(message);
            }

            class ListNode {
                constructor(data = 0, next = null) {
                    this.data = data;
                    this.next = next;
                }
            }

            class BinaryTreeNode {
                constructor(data = 0, left = null, right = null, parent = null) {
                    this.data = data;
                    this.left = left;
                    this.right = right;
                    this.parent = parent;
                }
            }

            class PostingListNode {
                constructor(order = 0, next = null, jump = null) {
                    this.order = order;
                    this.next = next;
                    this.jump = jump;
                }
            }

            class GraphVertex {
                constructor(label = 0) {
                    this.label = label;
                    this.edges = [];
                }
            }

            function arrayToListNode(arr) {
                if (!arr || !arr.length) return null;
                const head = new ListNode(arr[0]);
                let curr = head;
                for (let i = 1; i < arr.length; i++) {
                    curr.next = new ListNode(arr[i]);
                    curr = curr.next;
                }
                return head;
            }

            function listNodeToArray(head) {
                const res = [];
                const seen = new Set();
                while (head && !seen.has(head)) {
                    seen.add(head);
                    res.push(head.data);
                    head = head.next;
                }
                return res;
            }

            function listNodes(head) {
                const nodes = [];
                const seen = new Set();
                while (head && !seen.has(head)) {
                    seen.add(head);
                    nodes.push(head);
                    head = head.next;
                }
                return nodes;
            }

            function arrayToBinaryTree(arr) {
                if (!arr || !arr.length || arr[0] === null) return null;
                const root = new BinaryTreeNode(arr[0]);
                const queue = [root];
                let i = 1;
                while (queue.length > 0 && i < arr.length) {
                    const curr = queue.shift();
                    if (i < arr.length && arr[i] !== null) {
                        curr.left = new BinaryTreeNode(arr[i], null, null, curr);
                        queue.push(curr.left);
                    }
                    i++;
                    if (i < arr.length && arr[i] !== null) {
                        curr.right = new BinaryTreeNode(arr[i], null, null, curr);
                        queue.push(curr.right);
                    }
                    i++;
                }
                return root;
            }

            function binaryTreeToLevelOrder(root) {
                if (!root) return [];
                const result = [];
                const queue = [root];
                while (queue.length > 0) {
                    const curr = queue.shift();
                    if (curr) {
                        result.push(curr.data);
                        queue.push(curr.left);
                        queue.push(curr.right);
                    } else {
                        result.push(null);
                    }
                }
                while (result.length > 0 && result[result.length - 1] === null) {
                    result.pop();
                }
                return result;
            }

            global.ListNode = ListNode;
            global.BinaryTreeNode = BinaryTreeNode;
            global.PostingListNode = PostingListNode;
            global.GraphVertex = GraphVertex;

            const mod = require('./solution.js');

            function resolveTarget(name) {
                if (name && typeof mod[name] === 'function') return mod[name];
                if (typeof mod === 'function') return mod;
                if (mod && typeof mod === 'object') {
                    if (typeof mod.Solution === 'function') return mod.Solution;
                    for (const k of Object.keys(mod)) {
                        if (typeof mod[k] === 'function') return mod[k];
                    }
                }
                if (name && typeof global[name] === 'function') return global[name];
                throw new Error('Could not find function or class ' + name);
            }

            function invokeCustom(id, args, mod) {
                switch (id) {
                    case 'absent_value_array': {
                        const fn = resolveTarget('findMissingElement');
                        const missing = fn(args[0]);
                        check(missing >= 0 && !args[0].includes(missing));
                        return true;
                    }
                    case 'alternating_array': {
                        const values = [...args[0]];
                        const fn = resolveTarget('rearrange');
                        fn(values);
                        for (let i = 1; i < values.length; i++) {
                            check(i % 2 === 1 ? values[i-1] <= values[i] : values[i-1] >= values[i]);
                        }
                        return true;
                    }
                    case 'even_odd_array': {
                        const values = [...args[0]];
                        const fn = resolveTarget('evenOdd');
                        fn(values);
                        let seenOdd = false;
                        for (const v of values) {
                            if ((v & 1) !== 0) seenOdd = true;
                            else check(!seenOdd, 'Even values must precede odd values.');
                        }
                        return true;
                    }
                    case 'dutch_national_flag': {
                        const values = [...args[0]];
                        const pivot = values[args[1]];
                        const fn = resolveTarget('dutchFlagPartition');
                        fn(args[1], values);
                        let state = 0;
                        for (const v of values) {
                            const group = v < pivot ? 0 : v === pivot ? 1 : 2;
                            check(group >= state, 'Partition order violated.');
                            state = group;
                        }
                        return true;
                    }
                    case 'gray_code': {
                        const fn = resolveTarget('grayCode');
                        const res = fn(args[0]);
                        check(res.length === (1 << args[0]));
                        check(new Set(res).size === res.length);
                        return true;
                    }
                    case 'run_length_compression': {
                        const enc = resolveTarget('encoding')(args[1]);
                        const dec = resolveTarget('decoding')(args[0]);
                        check(enc === args[0] && dec === args[1]);
                        return true;
                    }
                    case 'string_integer_interconversion': {
                        const s = resolveTarget('intToString')(args[0]);
                        const n = resolveTarget('stringToInt')(args[1]);
                        check(String(s) === String(args[0]) && Number(n) === Number(args[0]));
                        return true;
                    }
                    case 'reverse_list': {
                        const head = arrayToListNode(args[0]);
                        const fn = resolveTarget('reverseList');
                        return listNodeToArray(fn(head));
                    }
                    case 'pivot_list': {
                        const head = arrayToListNode(args[0]);
                        const fn = resolveTarget('listPivoting');
                        const res = fn(head, args[1]);
                        return listNodeToArray(res);
                    }
                    case 'is_list_cyclic': {
                        const head = arrayToListNode(args[0]);
                        const nodes = listNodes(head);
                        const cycleVal = args[1];
                        let start = null;
                        if (cycleVal !== -1) {
                            start = nodes.find(n => n.data === cycleVal);
                            if (start && nodes.length > 0) nodes[nodes.length - 1].next = start;
                        }
                        const fn = resolveTarget('hasCycle');
                        const res = fn(head);
                        check(res === start, 'Return node at beginning of cycle or null.');
                        return true;
                    }
                    case 'circular_queue': {
                        const Cls = resolveTarget('CircularQueue');
                        let q = null;
                        for (const [op, val] of args[0]) {
                            if (op === 'Queue') q = new Cls(val);
                            else if (op === 'enqueue') q.enqueue(val);
                            else if (op === 'dequeue') check(q.dequeue() === val);
                            else if (op === 'size') check(q.size() === val);
                        }
                        return true;
                    }
                    case 'stack_with_max': {
                        const Cls = resolveTarget('StackWithMax');
                        const s = new Cls();
                        for (const [op, val] of args[0]) {
                            if (op === 'Stack') {}
                            else if (op === 'push') s.push(val);
                            else if (op === 'pop') check(s.pop() === val);
                            else if (op === 'max') check(s.max() === val);
                            else if (op === 'empty') check(Boolean(s.empty()) === (val === 1));
                        }
                        return true;
                    }
                    case 'queue_from_stacks': {
                        const Cls = resolveTarget('QueueFromStacks');
                        const q = new Cls();
                        for (const [op, val] of args[0]) {
                            if (op === 'Queue') {}
                            else if (op === 'enqueue') q.enqueue(val);
                            else if (op === 'dequeue') check(q.dequeue() === val);
                        }
                        return true;
                    }
                    case 'queue_with_max': {
                        const Cls = resolveTarget('QueueWithMax');
                        const q = new Cls();
                        for (const [op, val] of args[0]) {
                            if (op === 'QueueWithMax') {}
                            else if (op === 'enqueue') q.enqueue(val);
                            else if (op === 'dequeue') check(q.dequeue() === val);
                            else if (op === 'max') check(q.max() === val);
                        }
                        return true;
                    }
                    case 'lru_cache': {
                        const Cls = resolveTarget('LruCache');
                        let c = null;
                        for (const [op, k, v] of args[0]) {
                            if (op === 'LruCache') c = new Cls(k);
                            else if (op === 'lookup') check(c.lookup(k) === v);
                            else if (op === 'insert') c.insert(k, v);
                            else if (op === 'erase') check(Boolean(c.erase(k)) === (v === 1));
                        }
                        return true;
                    }
                    case 'adding_credits': {
                        const Cls = resolveTarget('AddingCredits');
                        const db = new Cls();
                        for (const [op, text, val] of args[0]) {
                            if (op === 'ClientsCreditsInfo') {}
                            else if (op === 'insert') db.insert(text, val);
                            else if (op === 'remove') check(Boolean(db.remove(text)) === (val === 1));
                            else if (op === 'lookup') check(db.lookup(text) === val);
                            else if (op === 'add_all') db.addAll(val);
                            else if (op === 'max') check(db.max() === text);
                        }
                        return true;
                    }
                    default:
                        throw new Error('Unknown custom problem: ' + id);
                }
            }

            function runAllTests() {
                const input = fs.readFileSync(0, 'utf-8');
                const tests = JSON.parse(input);
                const results = [];
                const isCustom = IS_CUSTOM_BOOL;
                const targetName = "TARGET_NAME_STR";

                for (const test of tests) {
                    const start = performance.now();
                    let actual = null;
                    let error = null;
                    let validationFailed = false;
                    let validationMessage = null;

                    try {
                        if (isCustom) {
                            actual = invokeCustom("PROBLEM_ID_STR", test, mod);
                        } else {
                            const fn = resolveTarget(targetName);
                            const convertedArgs = test.slice();
                            ARG_CONVERSIONS
                            let res = fn(...convertedArgs);
                            if (res instanceof ListNode) res = listNodeToArray(res);
                            else if (res instanceof BinaryTreeNode) res = binaryTreeToLevelOrder(res);
                            actual = res;
                        }
                    } catch (err) {
                        if (err instanceof JudgeValidationException) {
                            validationFailed = true;
                            validationMessage = (err.message || '').slice(0, 2000);
                        } else {
                            error = (err.name || 'Error') + ': ' + (err.message || String(err));
                            if (error.length > 2000) error = error.slice(0, 2000);
                        }
                    }
                    const elapsedMs = performance.now() - start;
                    results.push({ actual, error, validationFailed, validationMessage, elapsedMs });
                }
                process.stdout.write(JSON.stringify(results));
            }

            runAllTests();
            """;

        return template
            .Replace("IS_CUSTOM_BOOL", isCustom ? "true" : "false")
            .Replace("TARGET_NAME_STR", targetName)
            .Replace("PROBLEM_ID_STR", problem.Id)
            .Replace("ARG_CONVERSIONS", argConversions.ToString());
    }

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
            handler = GenericTestHandler(target_fn, None)
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
