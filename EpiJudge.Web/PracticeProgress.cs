namespace EpiJudge.Web;

public sealed record ProgressEntry(string ProblemId, string? Language, string Mode, string Status);

public static class PracticeProgress
{
    public static ProblemProgress[] Calculate(IEnumerable<ProgressEntry> entries)
    {
        var states = new Dictionary<string, (bool Solved, HashSet<string> Languages)>();
        foreach (var entry in entries)
        {
            if (entry.Status is "Running" or "Not run") continue;
            if (!states.TryGetValue(entry.ProblemId, out var state)) state = (false, new());
            if (entry.Mode == "submit" && entry.Status == "Accepted")
            {
                state.Solved = true;
                if (entry.Language is not null) state.Languages.Add(entry.Language);
            }
            states[entry.ProblemId] = state;
        }
        return states.Select(p => new ProblemProgress(p.Key, p.Value.Solved ? "solved" : "attempted",
            p.Value.Languages.Order(StringComparer.Ordinal).ToArray())).ToArray();
    }
}
