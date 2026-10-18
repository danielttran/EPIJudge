using System.Text.RegularExpressions;

namespace EpiJudge.Runner;

public sealed record NativeStarter(string Signature, string StarterCode, string Filename, string Runtime);
internal sealed record NativeProblem(string SourcePath, NativeStarter Starter);

public sealed class NativeProblemCatalog
{
    private readonly Dictionary<(string, string), NativeProblem> entries = new();

    public NativeProblemCatalog(string repositoryRoot)
    {
        foreach (var language in new[] { "cpp", "java" })
        {
            var folder = Path.Combine(repositoryRoot, language == "cpp" ? "epi_judge_cpp" : "epi_judge_java/epi");
            foreach (var path in Directory.GetFiles(folder, language == "cpp" ? "*.cc" : "*.java").Order(StringComparer.Ordinal))
            {
                var source = File.ReadAllText(path);
                foreach (Match match in Regex.Matches(source, "\"([a-z0-9_]+)\\.tsv\""))
                {
                    var id = match.Groups[1].Value;
                    var name = Path.GetFileNameWithoutExtension(path);
                    // Use the with-parent variant described by the website's LCA exercise.
                    if (id == "lowest_common_ancestor" && name is not ("lowest_common_ancestor_with_parent" or "LowestCommonAncestorWithParent")) continue;
                    if (id == "gcd" && name is ("euclidean_gcd" or "EuclideanGcd")) continue;
                    var signature = language == "cpp"
                        ? "C++17 · " + Path.GetFileName(path)
                        : "Java 21 · epi." + name;
                    var guidance = language == "cpp"
                        ? "// Implement the TODO methods. Keep the supplied wrappers and main function.\n"
                        : "// Implement the TODO methods. Keep package epi, the class name, annotations, wrappers, and main.\n";
                    entries.Add((language, id), new(path, new(signature, guidance + source, Path.GetFileName(path),
                        language == "cpp" ? "C++17" : "Java 21")));
                }
            }
        }
    }

    public NativeStarter GetStarter(string language, string problemId) => Get(language, problemId).Starter;
    internal NativeProblem Get(string language, string problemId) => entries.TryGetValue((language, problemId), out var entry)
        ? entry : throw new InvalidOperationException($"No {language} wrapper is registered for {problemId}.");
}
