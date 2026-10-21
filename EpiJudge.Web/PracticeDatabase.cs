using System.Diagnostics;
using Microsoft.Data.Sqlite;

namespace EpiJudge.Web;

// Owns database creation and startup recovery. Each operation opens a short-lived connection.
public sealed class PracticeDatabase
{
    private readonly string connectionString;
    internal static readonly string Owner = $"{Environment.ProcessId}:{Process.GetCurrentProcess().StartTime.ToUniversalTime().Ticks}";

    public PracticeDatabase(IConfiguration configuration)
    {
        var directory = configuration["Practice:DataDirectory"] ?? Environment.GetEnvironmentVariable("EPI_DATA_DIR")
            ?? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "EPIJudge");
        Directory.CreateDirectory(directory);
        connectionString = new SqliteConnectionStringBuilder
        {
            DataSource = Path.Combine(Path.GetFullPath(directory), "practice.db"),
            DefaultTimeout = 10,
        }.ToString();
        using var db = Open();
        using (var version = Command(db, null, "PRAGMA user_version"))
        {
            if (Convert.ToInt32(version.ExecuteScalar()) > 2)
                throw new InvalidOperationException("This answer database was created by a newer EPI Practice version.");
        }
        using (var journal = Command(db, null, "PRAGMA journal_mode=WAL")) journal.ExecuteNonQuery();
        using var transaction = db.BeginTransaction();
        int schemaVersion;
        using (var version = Command(db, transaction, "PRAGMA user_version"))
        {
            schemaVersion = Convert.ToInt32(version.ExecuteScalar());
            if (schemaVersion > 2)
                throw new InvalidOperationException("This answer database was created by a newer EPI Practice version.");
        }
        using var command = db.CreateCommand();
        command.Transaction = transaction;
        command.CommandText = """
            CREATE TABLE IF NOT EXISTS drafts (
                problem TEXT NOT NULL, language TEXT NOT NULL, code TEXT NOT NULL,
                revision INTEGER NOT NULL, updated TEXT NOT NULL, PRIMARY KEY(problem, language));
            CREATE TABLE IF NOT EXISTS attempts (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL UNIQUE,
                problem TEXT NOT NULL, language TEXT, code TEXT, mode TEXT NOT NULL,
                status TEXT NOT NULL, passed INTEGER NOT NULL, total INTEGER NOT NULL,
                elapsed REAL NOT NULL, timestamp TEXT NOT NULL, result TEXT, legacy INTEGER NOT NULL, owner TEXT);
            CREATE INDEX IF NOT EXISTS attempt_problem ON attempts(problem, sequence DESC);
            CREATE TABLE IF NOT EXISTS legacy_solved (problem TEXT PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS migrations (id TEXT PRIMARY KEY);
            """;
        command.ExecuteNonQuery();
        if (schemaVersion < 2)
        {
            using var migration = Command(db, transaction, """
                ALTER TABLE drafts ADD COLUMN code_format TEXT NOT NULL DEFAULT 'legacy-v1';
                ALTER TABLE attempts ADD COLUMN code_format TEXT NOT NULL DEFAULT 'legacy-v1';
                PRAGMA user_version=2;
                """);
            migration.ExecuteNonQuery();
        }
        transaction.Commit();
        RecoverInterruptedAttempts(db);
    }

    private static void RecoverInterruptedAttempts(SqliteConnection db)
    {
        var abandoned = new List<string>();
        using (var command = Command(db, null, "SELECT id,owner FROM attempts WHERE status='Running'"))
        using (var reader = command.ExecuteReader())
        {
            while (reader.Read())
            {
                var parts = reader.IsDBNull(1) ? [] : reader.GetString(1).Split(':');
                var alive = false;
                if (parts.Length == 2 && int.TryParse(parts[0], out var pid) && pid > 0 &&
                    long.TryParse(parts[1], out var ticks) && ticks > 0)
                {
                    try
                    {
                        using var process = Process.GetProcessById(pid);
                        alive = process.StartTime.ToUniversalTime().Ticks == ticks;
                    }
                    catch (ArgumentException) { }
                    catch (InvalidOperationException) { }
                    catch (System.ComponentModel.Win32Exception) { alive = true; }
                }
                if (!alive) abandoned.Add(reader.GetString(0));
            }
        }
        foreach (var id in abandoned)
        {
            using var command = Command(db, null, "UPDATE attempts SET status='Interrupted' WHERE id=$id AND status='Running'", ("$id", id));
            command.ExecuteNonQuery();
        }
    }

    public SqliteConnection Open()
    {
        var db = new SqliteConnection(connectionString);
        db.Open();
        return db;
    }

    internal static SqliteCommand Command(SqliteConnection db, SqliteTransaction? tx, string sql,
        params (string Name, object? Value)[] values)
    {
        var command = db.CreateCommand();
        command.Transaction = tx;
        command.CommandText = sql;
        foreach (var (name, value) in values) command.Parameters.AddWithValue(name, value ?? DBNull.Value);
        return command;
    }

}
