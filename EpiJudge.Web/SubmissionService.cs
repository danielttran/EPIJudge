using EpiJudge.Runner;

namespace EpiJudge.Web;

// These two boundaries allow tests to exercise process and storage failures.
// The normal application still uses the concrete runner and SQLite store.
public interface IAttemptStore
{
    SavedAttempt BeginAttempt(string problem, string language, string code, string mode,
        string codeFormat = "legacy-v1");
    void CompleteAttempt(string id, SubmissionResult result);
}

public enum SubmissionFailure { Busy, Interrupted, Execution, Storage }
public sealed record SubmissionOutcome(SubmissionResult? Result, SubmissionFailure? Failure = null);

public sealed class SubmissionService(IAttemptStore store, ISubmissionRunner runner, ILogger<SubmissionService> logger)
{
    public async Task<SubmissionOutcome> Execute(Problem problem, string language, string code, string mode,
        CancellationToken cancellation, string codeFormat = "legacy-v1")
    {
        SavedAttempt attempt;
        try
        {
            attempt = store.BeginAttempt(problem.Id, language, code, mode, codeFormat);
        }
        catch (Exception exception)
        {
            logger.LogError(exception, "Could not capture submission source; execution was not started");
            return new(null, SubmissionFailure.Storage);
        }

        SubmissionResult result;
        SubmissionFailure? failure = null;
        try
        {
            var prepared = CallableCodeCatalog.Prepare(problem.Id, language, code, codeFormat);
            var executed = await runner.RunAsync(problem, prepared.Code, mode == "run", language, cancellation);
            if (executed is null)
            {
                result = new(attempt.Id, "Not run", 0, 0, 0, "The runner was busy.", []);
                failure = SubmissionFailure.Busy;
            }
            else
            {
                result = CallableCodeCatalog.MapResult(executed, prepared) with { Id = attempt.Id };
            }
        }
        catch (OperationCanceledException) when (cancellation.IsCancellationRequested)
        {
            result = new(attempt.Id, "Interrupted", 0, 0, 0, "The request was interrupted. Your source code was saved.", []);
            failure = SubmissionFailure.Interrupted;
        }
        catch (Exception exception)
        {
            logger.LogError(exception, "Submission execution failed");
            result = new(attempt.Id, "Runner error", 0, 0, 0, "The runner could not start. Your source code was saved.", []);
            failure = SubmissionFailure.Execution;
        }

        try
        {
            store.CompleteAttempt(attempt.Id, result);
        }
        catch (Exception exception)
        {
            // Do not retry a failed write as a fabricated runner error. The
            // snapshot remains available and startup recovery handles Running.
            logger.LogError(exception, "Execution finished but its result could not be saved for {AttemptId}", attempt.Id);
            return new(result, SubmissionFailure.Storage);
        }
        return new(result, failure);
    }
}
