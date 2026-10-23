using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using System.ComponentModel;
using System.Text.Json;

namespace EpiJudge.Runner;

public sealed record FormatResult(string? Code, string? Error, string? Message);

// Only the formatter process receives source, on stdin. It never executes or saves it.
public sealed class CodeFormatter(string repositoryRoot)
{
    private readonly SemaphoreSlim gate = new(2);

    public async Task<FormatResult> FormatAsync(string language, string code, string codeFormat, CancellationToken cancellation)
    {
        if (language is not ("csharp" or "javascript" or "python" or "cpp" or "java") ||
            codeFormat is not ("callable-v1" or "legacy-v1") || string.IsNullOrWhiteSpace(code) || code.Length > 40_000)
            return new(null, "invalid", "Choose a supported language and code format, with 1–40,000 characters of code.");
        if (!await gate.WaitAsync(0, cancellation)) return new(null, "busy", "The local formatter is busy. Try again shortly.");
        try
        {
            if (language == "csharp")
            {
                var root = CSharpSyntaxTree.ParseText(code, cancellationToken: cancellation).GetRoot(cancellation);
                if (root.GetDiagnostics().FirstOrDefault(d => d.Severity == DiagnosticSeverity.Error) is { } error)
                    return new(null, "invalid", $"Invalid or incomplete C# syntax: {error.GetMessage()} Code was not changed.");
                var formatted = root.NormalizeWhitespace(indentation: "    ", eol: "\n").ToFullString() + "\n";
                var checkedRoot = CSharpSyntaxTree.ParseText(formatted, cancellationToken: cancellation).GetRoot(cancellation);
                if (checkedRoot.ContainsDiagnostics && checkedRoot.GetDiagnostics().Any(d => d.Severity == DiagnosticSeverity.Error) ||
                    !root.DescendantTokens(descendIntoTrivia: true).Select(t => (t.RawKind, t.Text))
                        .SequenceEqual(checkedRoot.DescendantTokens(descendIntoTrivia: true).Select(t => (t.RawKind, t.Text))))
                    return new(null, "invalid", "Formatting changed the syntax tree. Code was not changed.");
                return formatted.Length <= 40_000 ? new(formatted, null, null) : new(null, "invalid", "Formatted code exceeds 40,000 characters. Code was not changed.");
            }
            var script = Path.Combine(repositoryRoot, "scripts", "code_workspace", "formatter.py");
            var result = await ProcessHost.RunAsync(PythonLocator.FindPython(), [script], repositoryRoot,
                JsonSerializer.Serialize(new { language, code, codeFormat }), TimeSpan.FromSeconds(10), cancellation);
            if (result.TimedOut || result.OutputLimitExceeded)
                return new(null, "timeout", "Formatting exceeded its local limit. Code was not changed.");
            if (result.ExitCode != 0) return Unavailable();
            var reply = JsonSerializer.Deserialize<FormatResult>(result.Output, new JsonSerializerOptions(JsonSerializerDefaults.Web));
            if (reply?.Error is "invalid" or "unavailable") return reply;
            return reply?.Code is { Length: > 0 and <= 40_000 } && reply.Error is null ? reply : Unavailable();
        }
        catch (Exception error) when (error is FileNotFoundException or Win32Exception or JsonException or IOException)
        {
            return Unavailable();
        }
        finally { gate.Release(); }
    }

    private static FormatResult Unavailable() => new(null, "unavailable",
        "Local formatter unavailable. Install scripts/code_workspace/requirements.txt with the server's Python and run npm ci in epijudge.client. Code was not changed.");
}
