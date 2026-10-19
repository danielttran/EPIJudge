using System.Text.Json;
using EpiJudge.Runner;
using Microsoft.AspNetCore.Http.Features;
using Microsoft.Data.Sqlite;

namespace EpiJudge.Web;

public static class PracticeEndpoints
{
    public static bool ValidLanguage(string? language) => language is "csharp" or "javascript" or "python" or "cpp" or "java";

    public static void MapPractice(this WebApplication app)
    {
        var group = app.MapGroup("/api/practice");
        group.AddEndpointFilter(async (context, next) =>
        {
            var http = context.HttpContext;
            http.Response.Headers.CacheControl = "no-store";
            if (http.Request.Method != "GET" && http.Request.Headers["X-EpiJudge-Client"] != "local-editor")
                return Results.StatusCode(403);
            try { return await next(context); }
            catch (SqliteException exception)
            {
                app.Logger.LogError(exception, "Practice database operation failed");
                return Results.Problem("Could not access saved answers. Your browser recovery copy is still available.", statusCode: 503);
            }
        });
        group.MapGet("", (PracticeStore store) => Results.Ok(new { drafts = store.Drafts(), progress = store.Progress() }));
        group.MapPut("/drafts/{problemId}/{language}", (string problemId, string language,
            DraftWrite write, ProblemCatalog catalog, PracticeStore store) =>
        {
            if (catalog.Find(problemId) is null || !ValidLanguage(language) || write.Code is null || write.Code.Length > 40_000 || write.Revision < 0)
                return Results.BadRequest(new { message = "Invalid problem, language, draft, or revision." });
            var result = store.SaveDraft(problemId, language, write);
            return result.Saved ? Results.Ok(result.Draft) : Results.Conflict(new
            {
                message = "This answer was changed in another tab. Your local copy is preserved; choose which version to keep.", draft = result.Draft,
            });
        });
        group.MapGet("/history", (string problemId, long? before, PracticeStore store) =>
            Results.Ok(store.History(problemId, before ?? long.MaxValue)));
        group.MapGet("/history/{id}", (string id, PracticeStore store) =>
            store.Attempt(id) is { } attempt ? Results.Ok(attempt) : Results.NotFound());
        group.MapGet("/export", (PracticeStore store) => Results.File(
            JsonSerializer.SerializeToUtf8Bytes(store.Export(), new JsonSerializerOptions(JsonSerializerDefaults.Web)),
            "application/json", $"epi-answers-{DateTime.UtcNow:yyyy-MM-dd}.json"));
        group.MapPost("/import", (PracticeBackup backup, ProblemCatalog catalog, PracticeStore store) =>
        {
            if (!PracticeBackupValidator.Validate(backup, id => catalog.Find(id) is not null)) return Results.BadRequest(new { message = "This is not a valid EPI Practice version 1 backup." });
            store.Import(backup);
            return Results.Ok(new { message = "Imported answers and history. Existing drafts were kept." });
        });
        group.MapPost("/migrate", (LegacyImport legacy, ProblemCatalog catalog, PracticeStore store) =>
        {
            var backup = new PracticeBackup(1, legacy.Drafts, legacy.Attempts, legacy.SolvedIds);
            if (string.IsNullOrWhiteSpace(legacy.MigrationId) || legacy.MigrationId.Length > 100 || !PracticeBackupValidator.Validate(backup, id => catalog.Find(id) is not null))
                return Results.BadRequest(new { message = "Browser data could not be migrated. Your original browser data has been retained." });
            // Legacy summaries have no recoverable source code or language.
            var imported = store.Import(backup with { Attempts = backup.Attempts.Select(a => a with { Legacy = true }).ToArray() }, legacy.MigrationId);
            return Results.Ok(new { imported });
        });
    }

}
