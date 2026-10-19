using System.Text.Json;
using static EpiJudge.Web.PracticeDatabase;
using EpiJudge.Runner;
using Microsoft.Data.Sqlite;

namespace EpiJudge.Web;

// One local profile. All writes use parameterized SQL and short transactions;
// grading never holds a database transaction open.
public sealed class PracticeStore(PracticeDatabase database) : IAttemptStore
{
    private const string AttemptColumns = "sequence,id,problem,language,code,mode,status,passed,total,elapsed,timestamp,result,legacy";
    private static readonly JsonSerializerOptions Json = new(JsonSerializerDefaults.Web);
    private SqliteConnection Open() => database.Open();

    private static Draft ReadDraft(SqliteDataReader reader) => new(reader.GetString(0), reader.GetString(1),
        reader.GetString(2), reader.GetInt64(3), reader.GetString(4));

    private static SavedAttempt ReadAttempt(SqliteDataReader r) => new(r.GetString(1), r.GetString(2),
        r.IsDBNull(3) ? null : r.GetString(3), r.IsDBNull(4) ? null : r.GetString(4), r.GetString(5),
        r.GetString(6), r.GetInt32(7), r.GetInt32(8), r.GetDouble(9), r.GetString(10),
        r.IsDBNull(11) ? null : JsonSerializer.Deserialize<SubmissionResult>(r.GetString(11), Json),
        r.GetBoolean(12), r.GetInt64(0));

    public Draft[] Drafts()
    {
        using var db = Open();
        using var command = Command(db, null, "SELECT problem,language,code,revision,updated FROM drafts");
        using var reader = command.ExecuteReader();
        var results = new List<Draft>();
        while (reader.Read()) results.Add(ReadDraft(reader));
        return results.ToArray();
    }

    public (bool Saved, Draft? Draft) SaveDraft(string problem, string language, DraftWrite write)
    {
        using var db = Open();
        using var tx = db.BeginTransaction();
        Draft? current = null;
        using (var find = Command(db, tx, "SELECT problem,language,code,revision,updated FROM drafts WHERE problem=$p AND language=$l",
            ("$p", problem), ("$l", language)))
        using (var reader = find.ExecuteReader())
        {
            if (reader.Read()) current = ReadDraft(reader);
        }
        if (current?.Code == write.Code) return (true, current);
        if ((current?.Revision ?? 0) != write.Revision) return (false, current);
        var draft = new Draft(problem, language, write.Code, write.Revision + 1, DateTimeOffset.UtcNow.ToString("O"));
        using var command = Command(db, tx, """
            INSERT INTO drafts VALUES ($p,$l,$c,$r,$t) ON CONFLICT(problem,language)
            DO UPDATE SET code=$c, revision=$r, updated=$t
            """, ("$p", problem), ("$l", language), ("$c", draft.Code), ("$r", draft.Revision), ("$t", draft.UpdatedAt));
        command.ExecuteNonQuery();
        tx.Commit();
        return (true, draft);
    }

    public SavedAttempt BeginAttempt(string problem, string language, string code, string mode)
    {
        var attempt = new SavedAttempt(Guid.NewGuid().ToString("N"), problem, language, code,
            mode, "Running", 0, 0, 0, DateTimeOffset.UtcNow.ToString("O"), null);
        using var db = Open();
        InsertAttempt(db, null, attempt);
        return attempt;
    }

    // Keep only visible examples in stored results; hidden inputs never enter a backup.
    public void CompleteAttempt(string id, SubmissionResult result)
    {
        var visible = result with { Id = id, Cases = result.Cases.Where(c => !c.Hidden).Take(3).ToArray() };
        using var db = Open();
        using var command = Command(db, null, """
            UPDATE attempts SET status=$s, passed=$p, total=$t, elapsed=$e, result=$r WHERE id=$id
            """, ("$s", result.Status), ("$p", result.Passed), ("$t", result.Total),
            ("$e", result.ElapsedMs), ("$r", JsonSerializer.Serialize(visible, Json)), ("$id", id));
        command.ExecuteNonQuery();
    }

    public SavedAttempt[] History(string? problem = null, long before = long.MaxValue, int limit = 50, bool includeCode = false)
    {
        using var db = Open();
        using var command = Command(db, null, $"""
            SELECT sequence,id,problem,language,{(includeCode ? "code" : "NULL")},mode,status,passed,total,elapsed,timestamp,{(includeCode ? "result" : "NULL")},legacy
            FROM attempts WHERE ($p IS NULL OR problem=$p) AND sequence < $before
            ORDER BY sequence DESC LIMIT $limit
            """, ("$p", problem), ("$before", before), ("$limit", limit));
        using var reader = command.ExecuteReader();
        var results = new List<SavedAttempt>();
        while (reader.Read())
        {
            var attempt = ReadAttempt(reader);
            results.Add(attempt);
        }
        return results.ToArray();
    }

    public SavedAttempt? Attempt(string id)
    {
        using var db = Open();
        using var command = Command(db, null, $"SELECT {AttemptColumns} FROM attempts WHERE id=$id", ("$id", id));
        using var reader = command.ExecuteReader();
        return reader.Read() ? ReadAttempt(reader) : null;
    }

    public ProblemProgress[] Progress()
    {
        using var db = Open();
        using var command = Command(db, null, """
            SELECT problem,language,mode,status FROM attempts WHERE status NOT IN ('Running','Not run')
            UNION ALL SELECT problem,NULL,'submit','Accepted' FROM legacy_solved
            """);
        using var reader = command.ExecuteReader();
        var entries = new List<ProgressEntry>();
        while (reader.Read())
            entries.Add(new(reader.GetString(0), reader.IsDBNull(1) ? null : reader.GetString(1), reader.GetString(2), reader.GetString(3)));
        return PracticeProgress.Calculate(entries);
    }

    private static void InsertAttempt(SqliteConnection db, SqliteTransaction? tx, SavedAttempt a)
    {
        var result = a.Result is null ? null : a.Result with { Cases = a.Result.Cases.Where(c => !c.Hidden).Take(3).ToArray() };
        using var command = Command(db, tx, """
            INSERT OR IGNORE INTO attempts(id,problem,language,code,mode,status,passed,total,elapsed,timestamp,result,legacy,owner)
            VALUES($id,$p,$l,$c,$m,$s,$pass,$total,$e,$t,$r,$legacy,$owner)
            """, ("$id", a.Id), ("$p", a.ProblemId), ("$l", a.Language), ("$c", a.Code),
            ("$m", a.Mode), ("$s", a.Status), ("$pass", a.Passed), ("$total", a.Total),
            ("$e", a.ElapsedMs), ("$t", a.Timestamp), ("$r", result is null ? null : JsonSerializer.Serialize(result, Json)),
            ("$legacy", a.Legacy), ("$owner", a.Status == "Running" ? Owner : null));
        command.ExecuteNonQuery();
    }

    public PracticeBackup Export()
    {
        using var db = Open();
        using var tx = db.BeginTransaction();
        var drafts = new List<Draft>();
        var attempts = new List<SavedAttempt>();
        var solved = new HashSet<string>();
        using (var command = Command(db, tx, "SELECT problem,language,code,revision,updated FROM drafts"))
        using (var reader = command.ExecuteReader())
        {
            while (reader.Read()) drafts.Add(ReadDraft(reader));
        }
        using (var command = Command(db, tx, $"SELECT {AttemptColumns} FROM attempts ORDER BY sequence DESC"))
        using (var reader = command.ExecuteReader())
        {
            while (reader.Read()) attempts.Add(ReadAttempt(reader));
        }
        using (var command = Command(db, tx, "SELECT problem FROM legacy_solved"))
        using (var reader = command.ExecuteReader())
        {
            while (reader.Read()) solved.Add(reader.GetString(0));
        }
        foreach (var attempt in attempts.Where(a => a.Mode == "submit" && a.Status == "Accepted")) solved.Add(attempt.ProblemId);
        tx.Commit();
        return new(1, drafts.ToArray(), attempts.ToArray(), solved.ToArray());
    }

    // Merge, never replace: existing drafts and historical code snapshots remain intact.
    public bool Import(PracticeBackup backup, string? migrationId = null)
    {
        using var db = Open();
        using var tx = db.BeginTransaction();
        if (migrationId is not null)
        {
            using var marker = Command(db, tx, "INSERT OR IGNORE INTO migrations VALUES($id)", ("$id", migrationId));
            if (marker.ExecuteNonQuery() == 0) return false;
        }
        foreach (var draft in backup.Drafts)
        {
            using var command = Command(db, tx, "INSERT OR IGNORE INTO drafts VALUES($p,$l,$c,1,$t)",
                ("$p", draft.ProblemId), ("$l", draft.Language), ("$c", draft.Code), ("$t", draft.UpdatedAt));
            command.ExecuteNonQuery();
        }
        // Preserve chronological order for pagination even when the export was newest-first.
        foreach (var attempt in backup.Attempts.OrderBy(a => a.Timestamp).ThenBy(a => a.Sequence))
            InsertAttempt(db, tx, attempt.Status == "Running" ? attempt with { Status = "Interrupted" } : attempt);
        foreach (var id in backup.SolvedIds)
        {
            using var command = Command(db, tx, "INSERT OR IGNORE INTO legacy_solved VALUES($p)", ("$p", id));
            command.ExecuteNonQuery();
        }
        tx.Commit();
        return true;
    }
}
