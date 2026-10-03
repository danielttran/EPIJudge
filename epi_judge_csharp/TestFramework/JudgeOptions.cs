using System.Text.Json;

namespace EpiJudge.TestFramework;

internal sealed class JudgeOptions
{
    public required string TestDataDirectory { get; init; }
    public double TimeoutSeconds { get; init; }
    public int FailureLimit { get; init; } = 1;

    public static JudgeOptions Parse(string[] args)
    {
        string? testDataDirectory = null;
        for (var i = 0; i < args.Length; ++i)
        {
            if (args[i] == "--test-data-dir" && i + 1 < args.Length)
            {
                testDataDirectory = args[++i];
            }
            else if (args[i] is "--no-tty" or "--no-color" or "--no-update-js" or "--no-complexity")
            {
                // Accepted for command-line compatibility with the other judges.
            }
            else
            {
                throw new ArgumentException($"Unknown or incomplete option: {args[i]}");
            }
        }

        var root = FindRepositoryRoot();
        testDataDirectory ??= Path.Combine(root, "test_data");
        if (!Directory.Exists(testDataDirectory))
        {
            throw new DirectoryNotFoundException($"Test data directory does not exist: {testDataDirectory}");
        }

        var configPath = Path.Combine(root, "config.json");
        using var config = JsonDocument.Parse(File.ReadAllText(configPath));
        return new JudgeOptions
        {
            TestDataDirectory = Path.GetFullPath(testDataDirectory),
            TimeoutSeconds = config.RootElement.GetProperty("timeoutSeconds").GetDouble(),
            FailureLimit = config.RootElement.GetProperty("numFailedTestsBeforeStop").GetInt32(),
        };
    }

    private static string FindRepositoryRoot()
    {
        for (var directory = new DirectoryInfo(AppContext.BaseDirectory);
             directory is not null;
             directory = directory.Parent)
        {
            if (File.Exists(Path.Combine(directory.FullName, "config.json")) &&
                Directory.Exists(Path.Combine(directory.FullName, "test_data")))
            {
                return directory.FullName;
            }
        }

        for (var directory = new DirectoryInfo(Environment.CurrentDirectory);
             directory is not null;
             directory = directory.Parent)
        {
            if (File.Exists(Path.Combine(directory.FullName, "config.json")) &&
                Directory.Exists(Path.Combine(directory.FullName, "test_data")))
            {
                return directory.FullName;
            }
        }

        throw new DirectoryNotFoundException("Could not find the EPIJudge repository root.");
    }
}
