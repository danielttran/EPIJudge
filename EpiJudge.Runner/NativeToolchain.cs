namespace EpiJudge.Runner;

internal static class NativeToolchain
{
    public static string JavaTool(string name)
    {
        var executable = name + (OperatingSystem.IsWindows() ? ".exe" : "");
        var javaHome = Environment.GetEnvironmentVariable("EPI_JAVA_HOME") ?? Environment.GetEnvironmentVariable("JAVA_HOME");
        if (javaHome is not null && File.Exists(Path.Combine(javaHome, "bin", executable))) return Path.Combine(javaHome, "bin", executable);
        var onPath = FindOnPath(executable);
        if (onPath is not null) return onPath;
        throw new FileNotFoundException("Install JDK 21 or set EPI_JAVA_HOME to its installation folder.");
    }

    public static string? CppCompiler()
    {
        var configured = Environment.GetEnvironmentVariable("EPI_CPP_COMPILER");
        if (!string.IsNullOrWhiteSpace(configured)) return configured;
        return FindOnPath(OperatingSystem.IsWindows() ? "g++.exe" : "g++")
            ?? FindOnPath(OperatingSystem.IsWindows() ? "clang++.exe" : "clang++");
    }

    public static string VisualStudioSetup()
    {
        var configured = Environment.GetEnvironmentVariable("EPI_VCVARS64");
        if (!string.IsNullOrWhiteSpace(configured) && File.Exists(configured)) return configured;
        foreach (var root in new[] { Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86) })
        {
            var vs = Path.Combine(root, "Microsoft Visual Studio");
            if (!Directory.Exists(vs)) continue;
            foreach (var year in Directory.GetDirectories(vs).OrderDescending())
                foreach (var edition in Directory.GetDirectories(year))
                {
                    var setup = Path.Combine(edition, "VC", "Auxiliary", "Build", "vcvars64.bat");
                    if (File.Exists(setup)) return setup;
                }
        }
        throw new FileNotFoundException("Install Visual Studio C++ build tools, or put g++/clang++ on PATH (EPI_CPP_COMPILER can select one).");
    }

    private static string? FindOnPath(string name)
    {
        return ToolchainConfiguration.FindOnPath(name);
    }
}
