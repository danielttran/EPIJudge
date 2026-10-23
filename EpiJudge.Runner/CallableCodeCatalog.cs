using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace EpiJudge.Runner;

public sealed record CodeReference(string Title, string Code, string[] Names);

public sealed record CallableCodeDefinition(string ProblemId, string Language, string Filename,
    string Signature, string StarterCode, string SolutionCode, string Prefix, string Suffix,
    CodeReference[] References);

public sealed record PreparedCode(string Code, int PrefixLines, int UserLineCount,
    string Filename, string CodeFormat, IReadOnlyDictionary<int, int>? LineMap = null);

/// <summary>
/// Versioned bank-owned envelopes. Legacy programs never pass through source
/// inference, stripping, duplicate-type injection, or code migration.
/// </summary>
public static class CallableCodeCatalog
{
    public const string LegacyFormat = "legacy-v1";
    public const string CallableFormat = "callable-v1";
    private static readonly Lazy<Dictionary<(string, string), CallableCodeDefinition>> Entries = new(Load);

    public static bool ValidFormat(string? codeFormat) => codeFormat is null or LegacyFormat or CallableFormat;

    public static IReadOnlyCollection<CallableCodeDefinition> All => Entries.Value.Values;

    public static CallableCodeDefinition? Find(string problemId, string language) =>
        Entries.Value.GetValueOrDefault((problemId, NormalizeLanguage(language)));

    private static string NormalizeLanguage(string language) => language switch
    {
        "js" => "javascript",
        "py" => "python",
        _ => language
    };

    private static Dictionary<(string, string), CallableCodeDefinition> Load()
    {
        using var stream = typeof(CallableCodeCatalog).Assembly.GetManifestResourceStream("EpiJudge.Runner.callable-code.json")
            ?? throw new InvalidOperationException("The callable code catalog is missing.");
        var document = JsonSerializer.Deserialize<CallableDocument>(stream,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
            ?? throw new InvalidOperationException("The callable code catalog is invalid.");
        if (document.SchemaVersion != 1 || document.CodeFormat != CallableFormat ||
            document.Entries.Length != 334 * 5)
            throw new InvalidOperationException("Callable code must cover all 334 questions in all five languages.");
        var result = new Dictionary<(string, string), CallableCodeDefinition>();
        foreach (var item in document.Entries)
        {
            if (!SolutionCatalog.Languages.Contains(item.Language, StringComparer.Ordinal) ||
                new[] { item.ProblemId, item.Filename, item.Signature, item.StarterCode, item.SolutionCode }.Any(string.IsNullOrWhiteSpace) ||
                Path.GetFileName(item.Filename) != item.Filename || item.References is null ||
                item.References.Any(reference => string.IsNullOrWhiteSpace(reference.Title) ||
                    string.IsNullOrWhiteSpace(reference.Code) || reference.Names is null) ||
                !result.TryAdd((item.ProblemId, item.Language), item))
                throw new InvalidOperationException("Invalid callable code metadata: " + item.ProblemId + "/" + item.Language);
        }
        if (result.Keys.Select(key => key.Item1).Distinct().Count() != 334 ||
            result.Keys.GroupBy(key => key.Item1).Any(group => group.Count() != 5))
            throw new InvalidOperationException("Incomplete callable code coverage.");
        return result;
    }

    public static PreparedCode Prepare(string problemId, string language, string code, string? codeFormat)
    {
        if (!ValidFormat(codeFormat)) throw new ArgumentException("Choose a supported code format.", nameof(codeFormat));
        if (codeFormat is null or LegacyFormat)
            return new(code, 0, CountLines(code), "", LegacyFormat);
        language = NormalizeLanguage(language);
        var entry = Find(problemId, language)
            ?? throw new ArgumentException("No callable code contract exists for this question and language.");
        return PrepareCallable(entry, code);
    }

    // Also used to execute explicitly supplied, unpublished collection entries
    // through the same envelope without changing the live catalog inventory.
    public static PreparedCode PrepareCallable(CallableCodeDefinition entry, string code)
    {
        ArgumentNullException.ThrowIfNull(entry);
        var language = entry.Language;
        if (!SolutionCatalog.Languages.Contains(language, StringComparer.Ordinal) ||
            string.IsNullOrWhiteSpace(entry.Filename) || entry.Prefix is null || entry.Suffix is null ||
            Path.GetFileName(entry.Filename) != entry.Filename ||
            entry.Filename.IndexOfAny(['"', '\r', '\n']) >= 0)
            throw new ArgumentException("Invalid callable code definition.", nameof(entry));
        var prefix = entry.Prefix;
        Dictionary<int, int>? lineMap = null;
        if (prefix.Length > 0 && !prefix.EndsWith('\n')) prefix += "\n";
        if (language == "python")
        {
            // Compile the exact UTF-8 editor source as its own code object. This
            // permits future imports and keeps its traceback lines at one while
            // sharing the supplied model identities with the hidden adapter.
            var encoded = Convert.ToBase64String(Encoding.UTF8.GetBytes(code));
            return new(prefix + "\nexec(compile(__import__('base64').b64decode('" + encoded +
                "'), 'solution.py', 'exec'), globals())\n" + entry.Suffix,
                0, CountLines(code), entry.Filename, CallableFormat);
        }
        if (language == "java")
        {
            var (body, imports, importLines) = JavaImports(code);
            code = body;
            if (imports.Length > 0)
            {
                // The package belongs to the recorded envelope; user imports
                // belong before its outer class, never inside that class.
                var insertion = prefix.StartsWith("package ", StringComparison.Ordinal)
                    ? prefix.IndexOf(';') + 1 : 0;
                var lineOffset = prefix[..insertion].Count(character => character == '\n') + 1;
                lineMap = importLines.ToDictionary(pair => pair.Key + lineOffset, pair => pair.Value);
                prefix = prefix[..insertion] + "\n" + imports + prefix[insertion..];
            }
        }
        if (language == "javascript")
        {
            // Give submission declarations their own lexical scope. Normal
            // require bindings and helper names may shadow hidden support;
            // the recorded exports resolve the submitted functions here.
            return new(prefix + "(() => {\n" + code + "\n" + entry.Suffix + "\n})();\n",
                prefix.Count(character => character == '\n') + 1,
                CountLines(code), entry.Filename, CallableFormat);
        }
        if (language is "csharp" or "cpp")
        {
            var directive = "#line 1 \"" + entry.Filename + "\"\n";
            var reset = language == "csharp" ? "\n#line default\n" : "\n#line 1 \"bank-support.cpp\"\n";
            return new(prefix + directive + code + reset + entry.Suffix,
                0, CountLines(code), entry.Filename, CallableFormat);
        }
        return new(prefix + code + "\n" + entry.Suffix,
            prefix.Count(character => character == '\n'), CountLines(code), entry.Filename, CallableFormat, lineMap);
    }

    private static int CountLines(string code) => code.Count(character => character == '\n') + 1;

    private static (string Body, string Imports, Dictionary<int, int> Lines) JavaImports(string source)
    {
        var spans = new List<(int Start, int End)>();
        var position = 0;
        bool Trivia()
        {
            while (position < source.Length)
            {
                if (char.IsWhiteSpace(source[position])) { position++; continue; }
                if (position + 1 < source.Length && source[position] == '/' && source[position + 1] == '/')
                {
                    position += 2;
                    while (position < source.Length && source[position] != '\n') position++;
                    continue;
                }
                if (position + 1 < source.Length && source[position] == '/' && source[position + 1] == '*')
                {
                    var end = source.IndexOf("*/", position + 2, StringComparison.Ordinal);
                    if (end < 0) return false;
                    position = end + 2;
                    continue;
                }
                break;
            }
            return true;
        }
        while (Trivia())
        {
            var start = position;
            const string keyword = "import";
            if (!source.AsSpan(position).StartsWith(keyword, StringComparison.Ordinal) ||
                position + keyword.Length < source.Length &&
                (char.IsLetterOrDigit(source[position + keyword.Length]) || source[position + keyword.Length] is '_' or '$')) break;
            position += keyword.Length;
            var completed = false;
            while (Trivia() && position < source.Length)
            {
                var character = source[position++];
                if (character == ';') { spans.Add((start, position)); completed = true; break; }
                if (!char.IsLetterOrDigit(character) && character is not ('_' or '$' or '.' or '*')) break;
            }
            if (!completed) break;
        }
        if (spans.Count == 0) return (source, "", []);
        var body = source.ToCharArray();
        var imports = new StringBuilder();
        var lineMap = new Dictionary<int, int>();
        var importedLine = 1;
        foreach (var (start, end) in spans)
        {
            var originalLine = source[..start].Count(character => character == '\n') + 1;
            var lineCount = source[start..end].Count(character => character == '\n') + 1;
            for (var line = 0; line < lineCount; line++)
                lineMap.Add(importedLine + line, originalLine + line);
            importedLine += lineCount;
            imports.Append(source.AsSpan(start, end - start)).Append('\n');
            for (var index = start; index < end; index++)
                if (body[index] is not ('\r' or '\n')) body[index] = ' ';
        }
        return (new string(body), imports.ToString(), lineMap);
    }

    public static SubmissionResult MapResult(SubmissionResult result, PreparedCode prepared)
    {
        if (prepared.CodeFormat == LegacyFormat || prepared.PrefixLines == 0 && prepared.LineMap is null) return result;
        string? Map(string? text)
        {
            if (text is null) return null;
            // These patterns translate diagnostics only; user source is untouched.
            var filename = Regex.Escape(prepared.Filename);
            string Adjust(Match match)
            {
                if (!int.TryParse(match.Groups["line"].Value, System.Globalization.NumberStyles.None,
                    System.Globalization.CultureInfo.InvariantCulture, out var line)) return match.Value;
                if (prepared.LineMap is not null && prepared.LineMap.TryGetValue(line, out var originalLine))
                    return match.Groups["before"].Value + originalLine.ToString(System.Globalization.CultureInfo.InvariantCulture);
                var visibleLine = line - prepared.PrefixLines;
                if (visibleLine < 1 || visibleLine > prepared.UserLineCount) return match.Value;
                return match.Groups["before"].Value + visibleLine.ToString(System.Globalization.CultureInfo.InvariantCulture);
            }
            text = Regex.Replace(text, "(?<before>" + filename + @":)(?<line>\d+)", Adjust);
            return Regex.Replace(text, "(?<before>File \\\"[^\\\"\\r\\n]*" + filename + "\\\", line )(?<line>\\d+)", Adjust);
        }
        return result with
        {
            Diagnostics = Map(result.Diagnostics),
            Cases = result.Cases.Select(item => item with { Error = Map(item.Error) }).ToArray()
        };
    }

    private sealed record CallableDocument(int SchemaVersion, string CodeFormat, CallableCodeDefinition[] Entries);
}
