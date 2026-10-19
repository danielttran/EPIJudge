using System.Text.Json;

namespace EpiJudge.Web;

// Reading documents use the existing revisioned draft store and backup format.
// Their internal language discriminator is never accepted by the code runner.
public static class ReadingCatalog
{
    private static readonly Dictionary<string, JsonElement> Lessons = Load();

    private static Dictionary<string, JsonElement> Load()
    {
        using var stream = typeof(ReadingCatalog).Assembly.GetManifestResourceStream("EpiJudge.Web.reading-lessons.json")
            ?? throw new InvalidOperationException("Reading lesson manifest is missing.");
        using var document = JsonDocument.Parse(stream);
        return document.RootElement.EnumerateArray().ToDictionary(
            lesson => lesson.GetProperty("id").GetString()!, lesson => lesson.Clone());
    }

    public static bool ValidDocument(string id, string? code)
    {
        if (!Lessons.TryGetValue(id, out var lesson) || code is null || code.Length > 128_000) return false;
        try
        {
            using var document = JsonDocument.Parse(code);
            var value = document.RootElement;
            if (value.ValueKind != JsonValueKind.Object
                || !value.TryGetProperty("version", out var version) || !version.TryGetInt32(out var number) || number != 1
                || !value.TryGetProperty("notes", out var notes) || notes.ValueKind != JsonValueKind.String || notes.GetString()!.Length > 20_000
                || !value.TryGetProperty("reviewed", out var reviewed) || reviewed.ValueKind is not (JsonValueKind.True or JsonValueKind.False)
                || !value.TryGetProperty("checkpoints", out var checkpoints) || checkpoints.ValueKind != JsonValueKind.Array
                || !value.TryGetProperty("answers", out var answers) || answers.ValueKind != JsonValueKind.Object) return false;
            var knownCheckpoints = lesson.GetProperty("checkpoints").EnumerateArray().Select(c => c.GetProperty("id").GetString()).ToHashSet();
            if (checkpoints.GetArrayLength() > knownCheckpoints.Count
                || checkpoints.EnumerateArray().Any(c => c.ValueKind != JsonValueKind.String || !knownCheckpoints.Contains(c.GetString()))) return false;
            var quizzes = lesson.GetProperty("quizzes").EnumerateArray().ToDictionary(q => q.GetProperty("id").GetString()!);
            foreach (var answer in answers.EnumerateObject())
                if (!quizzes.TryGetValue(answer.Name, out var quiz) || !answer.Value.TryGetInt32(out var index)
                    || index < 0 || index >= quiz.GetProperty("options").GetArrayLength()) return false;
            return true;
        }
        catch (JsonException) { return false; }
        catch (InvalidOperationException) { return false; }
    }
}
