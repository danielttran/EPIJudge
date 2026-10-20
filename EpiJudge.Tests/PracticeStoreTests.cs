using EpiJudge.Runner;
using EpiJudge.Web;
using Microsoft.Data.Sqlite;
using Microsoft.Extensions.Configuration;

namespace EpiJudge.Tests;

// These tests deliberately exercise real SQLite. SQL concurrency and transactions
// cannot be established by mocking a repository.
public sealed class PracticeStoreTests : IDisposable
{
    private readonly string directory = Path.Combine(Path.GetTempPath(), "epi-tests-" + Guid.NewGuid().ToString("N"));
    private PracticeStore CreateStore() => new(new PracticeDatabase(new ConfigurationBuilder().AddInMemoryCollection(
        new Dictionary<string, string?> { ["Practice:DataDirectory"] = directory }).Build()));
    private static SubmissionResult Result(string status = "Accepted") => new("runner-id", status, status == "Accepted" ? 3 : 0, 3, 1.5, null, []);
    private static Draft Draft(string code = "imported", string problem = "count_bits", string language = "python") => new(problem, language, code, 30, "2026-01-01T00:00:00Z");
    private static SavedAttempt Attempt(string id = "a", string status = "Accepted", string mode = "submit", string? language = "python") =>
        new(id, "count_bits", language, "immutable source", mode, status, 3, 3, 1, "2026-01-01T00:00:00Z", Result(status));

    [Fact]
    public void ReadingNotesAndReviewPersistAndRoundTripWithoutChangingCodingProgress()
    {
        const string id = "reading-shared-state";
        const string code = "{\"version\":1,\"notes\":\"my reasoning λ\",\"reviewed\":true,\"checkpoints\":[],\"answers\":{}}";
        var store = CreateStore();
        Assert.True(store.SaveDraft(id, "reading", new(code, 0)).Saved);
        var restored = CreateStore();
        Assert.Equal(code, Assert.Single(restored.Drafts()).Code);
        Assert.Empty(restored.Progress());
        Assert.Empty(restored.History());
        var backup = restored.Export();
        Assert.True(PracticeBackupValidator.Validate(backup, _ => false));
        Assert.Equal(code, Assert.Single(backup.Drafts).Code);
        // A second database receives the same reading document through normal import.
        var destination = new PracticeStore(new PracticeDatabase(new ConfigurationBuilder().AddInMemoryCollection(
            new Dictionary<string, string?> { ["Practice:DataDirectory"] = Path.Combine(directory, "imported") }).Build()));
        destination.Import(backup);
        Assert.Equal(code, Assert.Single(destination.Drafts()).Code);
        Assert.Empty(destination.Progress());
    }

    [Fact]
    public void EmptyDatabaseHasNoDraftsHistoryOrProgress()
    {
        var store = CreateStore();
        Assert.Empty(store.Drafts()); Assert.Empty(store.History()); Assert.Empty(store.Progress());
        Assert.Null(store.Attempt("missing"));
    }

    [Theory]
    [InlineData("csharp")]
    [InlineData("javascript")]
    [InlineData("python")]
    [InlineData("cpp")]
    [InlineData("java")]
    public void DraftsAreIsolatedAndPersistAcrossStoreInstances(string language)
    {
        var store = CreateStore();
        var saved = store.SaveDraft("count_bits", language, new("' quoted; --\nλ", 0));
        store.SaveDraft("parity", language, new("other problem", 0));
        store.SaveDraft("count_bits", "other", new("other language", 0));
        Assert.True(saved.Saved); Assert.Equal(1, saved.Draft!.Revision);
        Assert.Equal(saved.Draft, Assert.Single(CreateStore().Drafts(), d => d.ProblemId == "count_bits" && d.Language == language));
    }

    [Fact]
    public void EmptyDraftIsSavedAndSameCodeIsIdempotentEvenWithStaleRevision()
    {
        var store = CreateStore();
        var first = store.SaveDraft("count_bits", "python", new("", 0));
        var repeated = store.SaveDraft("count_bits", "python", new("", 0));
        Assert.Equal(first, repeated);
        Assert.Equal("", Assert.Single(store.Drafts()).Code);
    }

    [Fact]
    public void StaleWritersReceiveCurrentDraftWithoutOverwriting()
    {
        var store = CreateStore();
        var first = store.SaveDraft("count_bits", "python", new("first", 0));
        var stale = store.SaveDraft("count_bits", "python", new("stale", 0));
        Assert.False(stale.Saved); Assert.Equal(first.Draft, stale.Draft);
        Assert.Equal(2, store.SaveDraft("count_bits", "python", new("second", 1)).Draft!.Revision);
    }

    [Fact]
    public async Task CompetingConnectionsAllowExactlyOneRevisionWinner()
    {
        var a = CreateStore(); var b = CreateStore();
        using var gate = new ManualResetEventSlim();
        var tasks = new[] { a, b }.Select((s, i) => Task.Run(() => { gate.Wait(); return s.SaveDraft("count_bits", "python", new("writer" + i, 0)); })).ToArray();
        gate.Set();
        var results = await Task.WhenAll(tasks);
        Assert.Single(results, r => r.Saved); Assert.Single(results, r => !r.Saved);
        Assert.Equal(1, Assert.Single(a.Drafts()).Revision);
    }

    [Fact]
    public void SnapshotIsImmutableAndHistorySummariesOmitSourceAndResults()
    {
        var store = CreateStore();
        var attempt = store.BeginAttempt("count_bits", "python", "submitted source", "submit");
        store.SaveDraft("count_bits", "python", new("later edit", 0));
        store.CompleteAttempt(attempt.Id, Result());
        var saved = store.Attempt(attempt.Id)!;
        Assert.Equal("submitted source", saved.Code); Assert.Equal(attempt.Id, saved.Result!.Id);
        Assert.Null(Assert.Single(store.History()).Code); Assert.Null(Assert.Single(store.History()).Result);
        Assert.Equivalent(saved, Assert.Single(store.History(includeCode: true)));
    }

    [Fact]
    public void HiddenCasesNeverAppearInHistoryOrExportsAndVisibleCasesAreCapped()
    {
        var store = CreateStore();
        var a = store.BeginAttempt("count_bits", "python", "source", "submit");
        var cases = Enumerable.Range(0, 8).Select(i => new CaseResult(i, true, "input", "expected", "actual", null, 1, i % 2 == 0)).ToArray();
        store.CompleteAttempt(a.Id, Result() with { Cases = cases });
        Assert.Equal(3, store.Attempt(a.Id)!.Result!.Cases.Count);
        Assert.All(Assert.Single(store.Export().Attempts).Result!.Cases, c => Assert.False(c.Hidden));
    }

    [Theory]
    [InlineData("run", "Accepted", "attempted")]
    [InlineData("submit", "Wrong answer", "attempted")]
    [InlineData("submit", "Compilation error", "attempted")]
    [InlineData("submit", "Interrupted", "attempted")]
    [InlineData("submit", "Accepted", "solved")]
    public void ProgressDistinguishesAttemptedFromAcceptedSubmission(string mode, string status, string expected)
    {
        var store = CreateStore(); var a = store.BeginAttempt("count_bits", "python", "source", mode);
        store.CompleteAttempt(a.Id, Result(status));
        Assert.Equal(expected, Assert.Single(store.Progress()).Status);
    }

    [Theory]
    [InlineData("Running")]
    [InlineData("Not run")]
    public void NonExecutionDoesNotMarkProblemAttempted(string status)
    {
        var store = CreateStore(); var a = store.BeginAttempt("count_bits", "python", "source", "submit");
        if (status != "Running") store.CompleteAttempt(a.Id, Result(status));
        Assert.Empty(store.Progress());
    }

    [Fact]
    public void LaterFailurePreservesSolvedAndAcceptedLanguagesAreDistinctAndSorted()
    {
        var store = CreateStore();
        foreach (var language in new[] { "python", "java", "python" })
        {
            var a = store.BeginAttempt("count_bits", language, "source", "submit"); store.CompleteAttempt(a.Id, Result());
        }
        var failure = store.BeginAttempt("count_bits", "cpp", "bad", "submit"); store.CompleteAttempt(failure.Id, Result("Wrong answer"));
        var progress = Assert.Single(store.Progress());
        Assert.Equal("solved", progress.Status); Assert.Equal(new[] { "java", "python" }, progress.AcceptedLanguages);
    }

    [Fact]
    public void PaginationUsesSequenceEvenWhenTimestampsAreEqual()
    {
        var store = CreateStore();
        for (var i = 0; i < 55; i++) store.BeginAttempt("count_bits", "python", "source" + i, "run");
        store.BeginAttempt("parity", "python", "unrelated", "run");
        var first = store.History("count_bits"); var second = store.History("count_bits", first[^1].Sequence);
        Assert.Equal(50, first.Length); Assert.Equal(5, second.Length);
        Assert.Empty(first.Select(a => a.Id).Intersect(second.Select(a => a.Id)));
        Assert.True(first[0].Sequence > first[^1].Sequence);
    }

    [Fact]
    public void ImportMergesWithoutOverwritingAndMigrationIsIdempotent()
    {
        var store = CreateStore(); store.SaveDraft("count_bits", "python", new("existing", 0));
        var backup = new PracticeBackup(1, [Draft(), Draft(problem: "parity")], [Attempt()], ["parity"]);
        Assert.True(store.Import(backup, "migration")); Assert.False(store.Import(backup, "migration"));
        store.Import(backup);
        Assert.Equal("existing", Assert.Single(store.Drafts(), d => d.ProblemId == "count_bits").Code);
        Assert.Equal(1, Assert.Single(store.Drafts(), d => d.ProblemId == "parity").Revision);
        Assert.Single(store.History()); Assert.All(store.Progress(), p => Assert.Equal("solved", p.Status));
    }

    [Fact]
    public void RoundTripPreservesSnapshotsAndConvertsImportedRunningAttemptsToInterrupted()
    {
        var store = CreateStore();
        var backup = new PracticeBackup(1, [Draft()], [Attempt(), Attempt("running", "Running")], ["parity"]);
        store.Import(backup);
        var exported = store.Export();
        Assert.Equal("immutable source", store.Attempt("a")!.Code);
        Assert.Equal("Interrupted", store.Attempt("running")!.Status);
        Assert.Contains("count_bits", exported.SolvedIds); Assert.Contains("parity", exported.SolvedIds);
        store.Import(exported);
        Assert.Equal(2, store.History().Length);
    }

    [Fact]
    public void ExportRestoresIntoAFreshDatabaseIncludingLanguagesLegacyProgressAndVisibleResults()
    {
        var source = CreateStore();
        var cases = new[] { new CaseResult(1, true, "public", "1", "1", null, 1, false), new CaseResult(2, true, "secret", "2", "2", null, 1, true) };
        source.Import(new(1, [Draft(language: "cpp"), Draft(language: "java")],
            [Attempt() with { Result = Result() with { Cases = cases } }], ["parity"]));
        var restored = new PracticeStore(new PracticeDatabase(new ConfigurationBuilder().AddInMemoryCollection(
            new Dictionary<string, string?> { ["Practice:DataDirectory"] = Path.Combine(directory, "restored") }).Build()));
        restored.Import(source.Export());
        Assert.Equal(new[] { "cpp", "java" }, restored.Drafts().Select(d => d.Language).Order().ToArray());
        var answer = restored.Attempt("a")!;
        Assert.Equal("immutable source", answer.Code);
        Assert.Equal("public", Assert.Single(answer.Result!.Cases).Input);
        Assert.Equal(2, restored.Progress().Count(p => p.Status == "solved"));
    }

    [Fact]
    public void FailedImportRollsBackDraftsAndMigrationMarkerTogether()
    {
        var store = CreateStore();
        var bad = new PracticeBackup(1, [Draft(), Draft(problem: "parity")], [Attempt()], []);
        // A trigger injects a genuine write failure after the first draft insert.
        using (var db = new SqliteConnection($"Data Source={Path.Combine(directory, "practice.db")}"))
        {
            db.Open(); using var command = db.CreateCommand();
            command.CommandText = "CREATE TRIGGER reject_parity BEFORE INSERT ON drafts WHEN NEW.problem='parity' BEGIN SELECT RAISE(ABORT,'test write failure'); END";
            command.ExecuteNonQuery();
        }
        Assert.Throws<SqliteException>(() => store.Import(bad, "atomic"));
        Assert.Empty(store.Drafts());
        Assert.True(store.Import(new(1, [Draft()], [], []), "atomic"));
    }

    [Fact]
    public void OpeningAnotherStoreDoesNotInterruptALiveOwnersAttempt()
    {
        var store = CreateStore(); var a = store.BeginAttempt("count_bits", "python", "source", "run");
        Assert.Equal("Running", CreateStore().Attempt(a.Id)!.Status);
    }

    [Theory]
    [InlineData("-1:123")]
    [InlineData("0:123")]
    [InlineData("1:0")]
    [InlineData("malformed")]
    public void MalformedOwnersCannotKeepAttemptsRunning(string owner)
    {
        var store = CreateStore();
        var attempt = store.BeginAttempt("blind75_two_sum", "python", "saved source", "run");
        using var db = new SqliteConnection($"Data Source={Path.Combine(directory, "practice.db")}");
        db.Open();
        using var command = db.CreateCommand();
        command.CommandText = "UPDATE attempts SET owner=$owner";
        command.Parameters.AddWithValue("$owner", owner);
        command.ExecuteNonQuery();
        var recovered = CreateStore().Attempt(attempt.Id)!;
        Assert.Equal("Interrupted", recovered.Status);
        Assert.Equal("saved source", recovered.Code);
    }

    [Fact]
    public void BlindAndEpiDraftsHistoryAndBackupsKeepSeparateIdentities()
    {
        var store = CreateStore();
        var languages = new[] { "csharp", "javascript", "python", "cpp", "java" };
        foreach (var language in languages)
        foreach (var id in new[] { "two_sum", "blind75_two_sum" })
        {
            var source = id + ":" + language;
            Assert.True(store.SaveDraft(id, language, new(source, 0)).Saved);
            var attempt = store.BeginAttempt(id, language, source, "submit");
            store.CompleteAttempt(attempt.Id, Result());
        }
        var backup = store.Export();
        Assert.True(PracticeBackupValidator.Validate(backup, id => new ProblemCatalog().Find(id) is not null));
        Assert.Equal(10, backup.Drafts.Length);
        Assert.Equal(10, backup.Attempts.Length);
        var restored = new PracticeStore(new PracticeDatabase(new ConfigurationBuilder().AddInMemoryCollection(
            new Dictionary<string, string?> { ["Practice:DataDirectory"] = Path.Combine(directory, "blind-restored") }).Build()));
        restored.Import(backup);
        restored.Import(backup);
        Assert.Equal(10, restored.Drafts().Length);
        Assert.Equal(10, restored.History(includeCode: true).Length);
        foreach (var draft in restored.Drafts())
            Assert.Equal(draft.ProblemId + ":" + draft.Language, draft.Code);
        Assert.Equal(2, restored.Progress().Length);
    }

    [Fact]
    public void StartupRecoversDeadOwnerAndRejectsNewerSchema()
    {
        var store = CreateStore(); var a = store.BeginAttempt("count_bits", "python", "source", "run");
        using var db = new SqliteConnection($"Data Source={Path.Combine(directory, "practice.db")}"); db.Open();
        using var command = db.CreateCommand(); command.CommandText = "UPDATE attempts SET owner='-1:0'"; command.ExecuteNonQuery();
        Assert.Equal("Interrupted", CreateStore().Attempt(a.Id)!.Status);
        command.CommandText = "PRAGMA user_version=999"; command.ExecuteNonQuery();
        Assert.Throws<InvalidOperationException>(() => CreateStore());
    }

    public void Dispose() { SqliteConnection.ClearAllPools(); if (Directory.Exists(directory)) Directory.Delete(directory, true); }
}
