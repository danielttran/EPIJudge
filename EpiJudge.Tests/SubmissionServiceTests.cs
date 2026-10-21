using EpiJudge.Runner;
using EpiJudge.Web;
using Microsoft.Extensions.Logging.Abstractions;

namespace EpiJudge.Tests;

public sealed class SubmissionServiceTests
{
    private static readonly Problem Problem = new("count_bits", "Count bits", "Bits", "Unrated", "", [], "", "", [], "");
    private sealed class History : IAttemptStore
    {
        public readonly List<string> Events = [];
        public bool FailBegin, FailComplete;
        public SavedAttempt? Snapshot;
        public SubmissionResult? Completed;
        public int Writes;
        public SavedAttempt BeginAttempt(string problem, string language, string code, string mode,
            string codeFormat = "legacy-v1")
        {
            Events.Add("begin");
            if (FailBegin) throw new IOException("disk unavailable");
            return Snapshot = new("saved-id", problem, language, code, mode, "Running", 0, 0, 0, "now", null, CodeFormat: codeFormat);
        }
        public void CompleteAttempt(string id, SubmissionResult result)
        {
            Events.Add("complete"); Writes++;
            Assert.Equal("saved-id", id);
            if (FailComplete) throw new IOException("disk full");
            Completed = result;
        }
    }
    private sealed class Runner(History history) : ISubmissionRunner
    {
        public Func<CancellationToken, Task<SubmissionResult?>> Execute = _ => Task.FromResult<SubmissionResult?>(new("runner-id", "Accepted", 3, 3, 1, null, []));
        public bool ExamplesOnly;
        public string? Language;
        public string? ExecutedCode;
        public Task<SubmissionResult?> RunAsync(Problem problem, string code, bool examplesOnly, string language, CancellationToken cancellation)
        {
            history.Events.Add("run");
            ExecutedCode = code;
            if (history.Snapshot!.CodeFormat == "legacy-v1") Assert.Equal(history.Snapshot.Code, code);
            ExamplesOnly = examplesOnly; Language = language;
            return Execute(cancellation);
        }
    }

    [Fact]
    public async Task CallableSubmissionSnapshotsUserCodeAndComposesOnlyTheExecutionCopy()
    {
        var definition = CallableCodeCatalog.Find("count_bits", "csharp")!;
        var history = new History();
        var runner = new Runner(history);
        var service = new SubmissionService(history, runner, NullLogger<SubmissionService>.Instance);
        var outcome = await service.Execute(Problem, "csharp", definition.SolutionCode, "submit", default, "callable-v1");
        Assert.Null(outcome.Failure);
        Assert.Equal(definition.SolutionCode, history.Snapshot!.Code);
        Assert.Equal("callable-v1", history.Snapshot.CodeFormat);
        Assert.Equal(CallableCodeCatalog.Prepare("count_bits", "csharp", definition.SolutionCode, "callable-v1").Code, runner.ExecutedCode);
        Assert.Contains(definition.SolutionCode, runner.ExecutedCode);
        Assert.Contains("#line 1", runner.ExecutedCode);
        Assert.Equal(new[] { "begin", "run", "complete" }, history.Events);
    }

    [Theory]
    [InlineData("run", true)]
    [InlineData("submit", false)]
    public async Task CapturesSourceBeforeExecutionAndReturnsPersistentId(string mode, bool examplesOnly)
    {
        var history = new History(); var runner = new Runner(history);
        var service = new SubmissionService(history, runner, NullLogger<SubmissionService>.Instance);
        var outcome = await service.Execute(Problem, "python", "exact source", mode, default);
        Assert.Null(outcome.Failure); Assert.Equal("saved-id", outcome.Result!.Id);
        Assert.Equal(new[] { "begin", "run", "complete" }, history.Events);
        Assert.Equal(examplesOnly, runner.ExamplesOnly); Assert.Equal("python", runner.Language);
        Assert.Equal("exact source", history.Snapshot!.Code); Assert.Equal(outcome.Result, history.Completed);
    }

    [Fact]
    public async Task FailedSnapshotPreventsExecution()
    {
        var history = new History { FailBegin = true }; var runner = new Runner(history);
        var outcome = await new SubmissionService(history, runner, NullLogger<SubmissionService>.Instance).Execute(Problem, "java", "code", "submit", default);
        Assert.Equal(SubmissionFailure.Storage, outcome.Failure); Assert.Equal(new[] { "begin" }, history.Events);
    }

    [Theory]
    [InlineData("busy", "Not run", SubmissionFailure.Busy)]
    [InlineData("cancel", "Interrupted", SubmissionFailure.Interrupted)]
    [InlineData("error", "Runner error", SubmissionFailure.Execution)]
    [InlineData("unrelated-cancel", "Runner error", SubmissionFailure.Execution)]
    public async Task FinalizesEveryExecutionOutcome(string scenario, string status, SubmissionFailure failure)
    {
        var history = new History(); var runner = new Runner(history);
        using var cancellation = new CancellationTokenSource();
        if (scenario == "cancel") cancellation.Cancel();
        runner.Execute = _ => scenario switch
        {
            "busy" => Task.FromResult<SubmissionResult?>(null),
            "cancel" or "unrelated-cancel" => Task.FromException<SubmissionResult?>(new OperationCanceledException()),
            _ => Task.FromException<SubmissionResult?>(new InvalidOperationException("compiler missing")),
        };
        var outcome = await new SubmissionService(history, runner, NullLogger<SubmissionService>.Instance).Execute(Problem, "java", "code", "submit", cancellation.Token);
        Assert.Equal(failure, outcome.Failure); Assert.Equal(status, history.Completed!.Status); Assert.Equal(1, history.Writes);
    }

    [Theory]
    [InlineData(false)]
    [InlineData(true)]
    public async Task ResultWriteFailureIsStorageFailureAndIsNeverRetriedAsRunnerError(bool executionFailed)
    {
        var history = new History { FailComplete = true }; var runner = new Runner(history);
        if (executionFailed) runner.Execute = _ => Task.FromException<SubmissionResult?>(new IOException("compiler failed"));
        var outcome = await new SubmissionService(history, runner, NullLogger<SubmissionService>.Instance).Execute(Problem, "python", "code", "submit", default);
        Assert.Equal(SubmissionFailure.Storage, outcome.Failure); Assert.Equal(1, history.Writes);
        Assert.Equal(executionFailed ? "Runner error" : "Accepted", outcome.Result!.Status);
    }
}
