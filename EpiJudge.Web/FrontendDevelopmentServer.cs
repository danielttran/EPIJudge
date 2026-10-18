using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using EpiJudge.Runner;

namespace EpiJudge.Web;

// Kestrel starts listening only after this service reports that React is ready.
// The browser stays on the ASP.NET Core origin; YARP forwards frontend traffic.
internal sealed class FrontendDevelopmentServer(
    IConfiguration configuration,
    IWebHostEnvironment environment,
    ILogger<FrontendDevelopmentServer> logger) : IHostedService, IDisposable
{
    private Process? process;
    private string? ownedCacheDirectory;
    private readonly Queue<string> recentOutput = new();
    private readonly object outputLock = new();

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        var port = configuration.GetValue<int>("Frontend:Port");
        var address = $"http://127.0.0.1:{port}";
        using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };
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
        if (string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable("EPI_VITE_CACHE_DIR")))
        {
            ownedCacheDirectory = Path.GetFullPath(Path.Combine(directory, "../.epi-runs", "vite-" + Guid.NewGuid().ToString("N")));
            info.Environment["EPI_VITE_CACHE_DIR"] = ownedCacheDirectory;
        }
        process = new Process { StartInfo = info };
        process.OutputDataReceived += CaptureOutput;
        process.ErrorDataReceived += CaptureOutput;
        process.Start();
        process.BeginOutputReadLine();
        process.BeginErrorReadLine();

        try
        {
            var deadline = Stopwatch.StartNew();
            while (deadline.Elapsed < TimeSpan.FromSeconds(60))
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
            throw new TimeoutException($"React modules did not become ready within 60 seconds. {LastOutput()}");
        }
        catch { StopProcess(); throw; }
    }

    private string FindNode() => NodeLocator.FindNode(configuration["Frontend:NodePath"]);

    private static async Task<bool> IsReady(HttpClient client, string address, CancellationToken cancellationToken)
    {
        try
        {
            // A marker distinguishes this application from an unrelated server
            // that happens to be using the same development port.
            var marker = await client.GetStringAsync(address + "/epi-client.json", cancellationToken);
            if (!marker.Contains("\"epijudge-client\"", StringComparison.Ordinal)) return false;
            // A static marker can respond while Vite is still optimizing JS.
            // Wait for the actual app and eager editor modules, not just HTML.
            var modules = await Task.WhenAll(
                client.GetStringAsync(address + "/src/main.tsx", cancellationToken),
                client.GetStringAsync(address + "/src/Editor.tsx", cancellationToken));
            return modules[0].Contains("createRoot", StringComparison.Ordinal) &&
                   modules[1].Contains("monaco.editor.create", StringComparison.Ordinal);
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
    internal static int FindAvailablePort()
    {
        using var listener = new TcpListener(IPAddress.Loopback, 0);
        listener.Start();
        return ((IPEndPoint)listener.LocalEndpoint).Port;
    }
    private void StopProcess()
    {
        try
        {
            if (process is { HasExited: false })
            {
                process.Kill(entireProcessTree: true);
                process.WaitForExit(3000);
            }
            if (ownedCacheDirectory is not null && Directory.Exists(ownedCacheDirectory))
                Directory.Delete(ownedCacheDirectory, recursive: true);
        }
        catch (InvalidOperationException) { }
        catch (IOException) { }
        catch (UnauthorizedAccessException) { }
    }
    public Task StopAsync(CancellationToken cancellationToken) { StopProcess(); return Task.CompletedTask; }
    public void Dispose() { StopProcess(); process?.Dispose(); }
}
