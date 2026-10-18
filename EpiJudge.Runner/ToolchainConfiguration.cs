using System.Text.Json;

namespace EpiJudge.Runner;

public static class ToolchainConfiguration
{
    public static void ApplyLocalOverrides(string repositoryRoot)
    {
        var path = Path.Combine(repositoryRoot, ".epijudge-tools.json");
        if (!File.Exists(path)) return;
        var values = JsonSerializer.Deserialize<Dictionary<string, string>>(File.ReadAllText(path)) ?? [];
        foreach (var name in new[] { "EPI_NODE_PATH", "EPI_PYTHON_PATH", "EPI_JAVA_HOME", "EPI_CPP_COMPILER", "EPI_VCVARS64" })
            if (values.TryGetValue(name, out var value) && !string.IsNullOrWhiteSpace(value) &&
                string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable(name)))
                Environment.SetEnvironmentVariable(name, value);
    }

    internal static string? FindOnPath(string filename)
    {
        var paths = Environment.GetEnvironmentVariable("PATH") ?? "";
        if (OperatingSystem.IsWindows())
            paths += ";" + Environment.GetEnvironmentVariable("PATH", EnvironmentVariableTarget.User)
                  + ";" + Environment.GetEnvironmentVariable("PATH", EnvironmentVariableTarget.Machine);
        foreach (var directory in paths.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries))
        {
            var folder = Environment.ExpandEnvironmentVariables(directory.Trim().Trim('"'));
            if (filename == "python.exe" && folder.Contains(@"\Microsoft\WindowsApps", StringComparison.OrdinalIgnoreCase)) continue;
            var path = Path.Combine(folder, filename);
            if (File.Exists(path)) return path;
        }
        return null;
    }
}
