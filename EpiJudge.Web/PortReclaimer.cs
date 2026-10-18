using System.Diagnostics;
using System.Net.Sockets;
using System.Text.Json;

namespace EpiJudge.Web;

public static class PortReclaimer
{
    public static async Task EnsurePortAvailableAsync(int port, TimeSpan? timeout = null)
    {
        var waitTimeout = timeout ?? TimeSpan.FromSeconds(5);
        if (IsPortAvailable(port)) return;

        // Try graceful HTTP shutdown if it's an existing EpiJudge.Web instance
        var graceful = await TryGracefulShutdownAsync(port);
        if (graceful && await WaitForPortAvailableAsync(port, TimeSpan.FromSeconds(3)))
            return;

        // If still not available, find listening process and kill if it's an EpiJudge process
        var pid = FindListeningPid(port);
        if (pid > 0 && pid != Environment.ProcessId)
        {
            try
            {
                var process = Process.GetProcessById(pid);
                var processName = process.ProcessName.ToLowerInvariant();
                if (processName.Contains("epijudge") || processName.Contains("dotnet") || processName.Contains("node"))
                {
                    process.Kill(entireProcessTree: true);
                    process.WaitForExit(3000);
                }
            }
            catch (Exception)
            {
                // Process may have already exited or access denied
            }
        }

        // Final poll loop to ensure port is released
        await WaitForPortAvailableAsync(port, waitTimeout);
    }

    private static bool IsPortAvailable(int port)
    {
        try
        {
            using var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            socket.ExclusiveAddressUse = true;
            socket.Bind(new System.Net.IPEndPoint(System.Net.IPAddress.Loopback, port));
            return true;
        }
        catch (SocketException)
        {
            return false;
        }
    }

    private static async Task<bool> WaitForPortAvailableAsync(int port, TimeSpan timeout)
    {
        var stopwatch = Stopwatch.StartNew();
        while (stopwatch.Elapsed < timeout)
        {
            if (IsPortAvailable(port)) return true;
            await Task.Delay(100);
        }
        return IsPortAvailable(port);
    }

    private static async Task<bool> TryGracefulShutdownAsync(int port)
    {
        try
        {
            using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(1) };
            var health = await client.GetStringAsync($"http://127.0.0.1:{port}/api/health");
            using var doc = JsonDocument.Parse(health);
            if (doc.RootElement.TryGetProperty("execution", out var exec) &&
                exec.GetString() == "trusted-local-only")
            {
                using var response = await client.PostAsync($"http://127.0.0.1:{port}/api/internal/shutdown", null);
                return response.IsSuccessStatusCode;
            }
        }
        catch (Exception)
        {
            // Host unreachable, not EpiJudge, or port not HTTP
        }
        return false;
    }

    private static int FindListeningPid(int port)
    {
        if (!OperatingSystem.IsWindows()) return -1;

        try
        {
            var startInfo = new ProcessStartInfo("netstat", "-ano -p tcp")
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            using var process = Process.Start(startInfo);
            if (process is null) return -1;

            var portStr = $":{port}";
            while (!process.StandardOutput.EndOfStream)
            {
                var line = process.StandardOutput.ReadLine();
                if (string.IsNullOrWhiteSpace(line)) continue;

                var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length >= 5 && parts[0].Equals("TCP", StringComparison.OrdinalIgnoreCase))
                {
                    var localAddress = parts[1];
                    var state = parts[3];
                    var pidStr = parts[4];

                    if (localAddress.EndsWith(portStr, StringComparison.OrdinalIgnoreCase) &&
                        state.Equals("LISTENING", StringComparison.OrdinalIgnoreCase) &&
                        int.TryParse(pidStr, out var pid))
                    {
                        return pid;
                    }
                }
            }
            process.WaitForExit(1000);
        }
        catch (Exception)
        {
            // Ignore netstat inspection failure
        }
        return -1;
    }
}
