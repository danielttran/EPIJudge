using EpiJudge.Runner;

namespace EpiJudge.Web;

public sealed record Draft(string ProblemId, string Language, string Code, long Revision, string UpdatedAt,
    string CodeFormat = "legacy-v1");
public sealed record DraftWrite(string Code, long Revision, string CodeFormat = "legacy-v1");
public sealed record ProblemProgress(string ProblemId, string Status, string[] AcceptedLanguages);
public sealed record SavedAttempt(string Id, string ProblemId, string? Language, string? Code,
    string Mode, string Status, int Passed, int Total, double ElapsedMs, string Timestamp,
    SubmissionResult? Result, bool Legacy = false, long Sequence = 0, string CodeFormat = "legacy-v1");
public sealed record PracticeBackup(int Version, Draft[] Drafts, SavedAttempt[] Attempts, string[] SolvedIds);
public sealed record LegacyImport(string MigrationId, Draft[] Drafts, SavedAttempt[] Attempts, string[] SolvedIds);
