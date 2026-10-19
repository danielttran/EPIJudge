namespace EpiJudge.Web;

public static class PracticeBackupValidator
{
    public static bool Validate(PracticeBackup? backup, Func<string, bool> knownProblem)
    {
        if (backup is not { Version: 1, Drafts: not null, Attempts: not null, SolvedIds: not null }) return false;
        if (backup.Drafts.Length > 2000 || backup.Attempts.Length > 100_000 || backup.SolvedIds.Length > 1000) return false;
        return backup.Drafts.All(d => ValidDraft(d, knownProblem))
            && backup.Attempts.All(a => ValidAttempt(a, knownProblem))
            && backup.SolvedIds.All(id => id is not null && knownProblem(id));
    }

    private static bool ValidDraft(Draft? draft, Func<string, bool> knownProblem) =>
        draft is not null && draft.ProblemId is not null
        && (draft.Language == "reading" ? ReadingCatalog.ValidDocument(draft.ProblemId, draft.Code)
            : knownProblem(draft.ProblemId) && PracticeEndpoints.ValidLanguage(draft.Language) && draft.Code is { Length: <= 40_000 })
        && draft.Revision >= 0
        && DateTimeOffset.TryParse(draft.UpdatedAt, out _);

    private static bool ValidAttempt(SavedAttempt? attempt, Func<string, bool> knownProblem)
    {
        if (attempt is null || attempt.Id is not { Length: > 0 and <= 200 }
            || attempt.ProblemId is null || !knownProblem(attempt.ProblemId)) return false;
        if (attempt.Language is not null && !PracticeEndpoints.ValidLanguage(attempt.Language)) return false;
        if (attempt.Code is { Length: > 40_000 } || attempt.Mode is not ("run" or "submit")
            || attempt.Status is not { Length: > 0 and <= 100 }) return false;
        if (attempt.Passed < 0 || attempt.Total < attempt.Passed || !ValidElapsed(attempt.ElapsedMs)
            || !DateTimeOffset.TryParse(attempt.Timestamp, out _)) return false;
        if (attempt.Result is not { } result) return true;
        return result.Cases is { Count: <= 10_001 }
            && result.Cases.All(c => c is not null && ValidElapsed(c.ElapsedMs));
    }

    private static bool ValidElapsed(double value) => double.IsFinite(value) && value >= 0;
}
