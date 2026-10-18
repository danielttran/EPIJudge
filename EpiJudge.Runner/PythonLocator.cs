namespace EpiJudge.Runner;

public static class PythonLocator
{
    public static string FindPython(string? configuredPath = null)
    {
        configuredPath ??= Environment.GetEnvironmentVariable("EPI_PYTHON_PATH");
        if (!string.IsNullOrWhiteSpace(configuredPath) && File.Exists(configuredPath)) return configuredPath;
        return ToolchainConfiguration.FindOnPath(OperatingSystem.IsWindows() ? "python.exe" : "python3")
            ?? throw new FileNotFoundException("Python could not be found. Install Python 3.10+ on PATH, or configure EPI_PYTHON_PATH.");
    }
}
