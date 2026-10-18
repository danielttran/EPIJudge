namespace EpiJudge.Runner;

public static class NodeLocator
{
    public static string FindNode(string? configuredPath = null)
    {
        configuredPath ??= Environment.GetEnvironmentVariable("EPI_NODE_PATH");
        if (!string.IsNullOrWhiteSpace(configuredPath) && File.Exists(configuredPath)) return configuredPath;
        return ToolchainConfiguration.FindOnPath(OperatingSystem.IsWindows() ? "node.exe" : "node")
            ?? throw new FileNotFoundException("Node.js could not be found. Install Node.js 24 LTS on PATH, or configure EPI_NODE_PATH.");
    }
}
