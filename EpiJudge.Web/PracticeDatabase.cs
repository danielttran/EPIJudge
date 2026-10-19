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
            if (Convert.ToInt32(version.ExecuteScalar()) > 1)
                throw new InvalidOperationException("This answer database was created by a newer EPI Practice version.");
        }
        using var command = db.CreateCommand();
        command.CommandText = """
            PRAGMA journal_mode=WAL;
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
            PRAGMA user_version=1;
            """;
        command.ExecuteNonQuery();
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
                if (parts.Length == 2 && int.TryParse(parts[0], out var pid) && long.TryParse(parts[1], out var ticks))
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
