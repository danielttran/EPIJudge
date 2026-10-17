using System.Diagnostics;

namespace EpiJudge.Web;

// Kestrel starts listening only after this service reports that React is ready.
// The browser stays on the ASP.NET Core origin; YARP forwards frontend traffic.
internal sealed class FrontendDevelopmentServer(
    IConfiguration configuration,
    IWebHostEnvironment environment,
    ILogger<FrontendDevelopmentServer> logger) : IHostedService, IDisposable
{
    private Process? process;
    private readonly Queue<string> recentOutput = new();
    private readonly object outputLock = new();

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        var port = configuration.GetValue("Frontend:Port", 5173);
        var address = $"http://127.0.0.1:{port}";
        using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(1) };
        if (await IsReady(client, address, cancellationToken))
        {
            logger.LogInformation("Using the EPI React development server already running on port {Port}.", port);
            return;
        }

        var directory = Path.GetFullPath(Path.Combine(environment.ContentRootPath, "../epijudge.client"));
        var vite = Path.Combine(directory, "node_modules", "vite", "bin", "vite.js");
        if (!File.Exists(vite))
            throw new InvalidOperationException("React dependencies are missing. Run 'npm ci' in epijudge.client, then start Website again.");

        var info = new ProcessStartInfo(FindNode())
        {
            WorkingDirectory = directory,
            UseShellExecute = false,
            CreateNoWindow = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        };
        foreach (var argument in new[] { vite, "--host", "127.0.0.1", "--port", port.ToString(), "--strictPort" })
            info.ArgumentList.Add(argument);
        var publicUrl = (configuration["urls"] ?? "http://localhost:5178").Split(';')[0];
        info.Environment["EPI_WEB_PORT"] = new Uri(publicUrl).Port.ToString();
        process = new Process { StartInfo = info };
        process.OutputDataReceived += CaptureOutput;
        process.ErrorDataReceived += CaptureOutput;
        process.Start();
        process.BeginOutputReadLine();
        process.BeginErrorReadLine();

        try
        {
            var deadline = Stopwatch.StartNew();
            while (deadline.Elapsed < TimeSpan.FromSeconds(30))
            {
                cancellationToken.ThrowIfCancellationRequested();
                if (process.HasExited)
                    throw new InvalidOperationException($"React could not start on port {port}. {LastOutput()}");
                if (await IsReady(client, address, cancellationToken))
                {
                    logger.LogInformation("React is ready. The website will be served directly at {Url}.", publicUrl);
                    return;
                }
                await Task.Delay(200, cancellationToken);
            }
            throw new TimeoutException($"React did not become ready within 30 seconds. {LastOutput()}");
        }
        catch { StopProcess(); throw; }
    }

    private string FindNode()
    {
        var configuredPath = configuration["Frontend:NodePath"];
        if (!string.IsNullOrWhiteSpace(configuredPath))
            return File.Exists(configuredPath) ? configuredPath : throw new FileNotFoundException("Frontend:NodePath does not point to node.exe.", configuredPath);

        // Visual Studio can retain an old PATH after Node is installed. Read
        // the current user PATH too, without requiring the IDE to restart.
        var paths = Environment.GetEnvironmentVariable("PATH") ?? "";
        if (OperatingSystem.IsWindows())
            paths += ";" + Environment.GetEnvironmentVariable("PATH", EnvironmentVariableTarget.User)
                + ";" + Environment.GetEnvironmentVariable("PATH", EnvironmentVariableTarget.Machine);
        var filename = OperatingSystem.IsWindows() ? "node.exe" : "node";
        foreach (var path in paths.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries))
        {
            var candidate = Path.Combine(Environment.ExpandEnvironmentVariables(path.Trim().Trim('"')), filename);
            if (File.Exists(candidate)) return candidate;
        }
        throw new FileNotFoundException("Node.js could not be found. Install Node.js 24 LTS or set Frontend:NodePath in appsettings.Development.json.");
    }

    private static async Task<bool> IsReady(HttpClient client, string address, CancellationToken cancellationToken)
    {
        try
        {
            // A marker distinguishes this application from an unrelated server
            // that happens to be using the same development port.
            var marker = await client.GetStringAsync(address + "/epi-client.json", cancellationToken);
            return marker.Contains("\"epijudge-client\"", StringComparison.Ordinal);
        }
        catch (HttpRequestException) { return false; }
        catch (OperationCanceledException) when (!cancellationToken.IsCancellationRequested) { return false; }
    }

    private void CaptureOutput(object sender, DataReceivedEventArgs arguments)
    {
        if (arguments.Data is not { Length: > 0 } line) return;
        lock (outputLock)
        {
            recentOutput.Enqueue(line);
            while (recentOutput.Count > 8) recentOutput.Dequeue();
        }
        logger.LogDebug("Vite: {Output}", line);
    }

    private string LastOutput() { lock (outputLock) return string.Join(Environment.NewLine, recentOutput); }
    private void StopProcess()
    {
        try { if (process is { HasExited: false }) process.Kill(entireProcessTree: true); }
        catch (InvalidOperationException) { }
    }
    public Task StopAsync(CancellationToken cancellationToken) { StopProcess(); return Task.CompletedTask; }
    public void Dispose() { StopProcess(); process?.Dispose(); }
}
