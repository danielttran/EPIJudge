using System.Diagnostics;
using System.Text;

namespace EpiJudge.Runner;

internal sealed record ProcessResult(int ExitCode, string Output, string Error, bool TimedOut, bool OutputLimitExceeded);

internal static class ProcessHost
{
    public static async Task<ProcessResult> RunAsync(string executable, string[] arguments, string directory,
        string? input, TimeSpan timeout, CancellationToken cancellation)
    {
        using var process = new Process
        {
            StartInfo = new ProcessStartInfo(executable)
            {
                WorkingDirectory = directory,
                RedirectStandardInput = true, RedirectStandardOutput = true, RedirectStandardError = true,
                UseShellExecute = false, CreateNoWindow = true
            }
        };
        foreach (var argument in arguments) process.StartInfo.ArgumentList.Add(argument);
        process.StartInfo.Environment["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1";
        process.StartInfo.Environment["DOTNET_SKIP_FIRST_TIME_EXPERIENCE"] = "1";
        process.StartInfo.Environment["MSBUILDDISABLENODEREUSE"] = "1";
        process.Start();
        var outputLimitExceeded = 0;
        async Task<string> ReadBoundedAsync(StreamReader reader)
        {
            var content = new StringBuilder();
            var buffer = new char[8192];
            int count;
            while ((count = await reader.ReadAsync(buffer)) > 0)
            {
                if (content.Length + count <= 16_000_000) content.Append(buffer, 0, count);
                else { Interlocked.Exchange(ref outputLimitExceeded, 1); Kill(); }
            }
            return content.ToString();
        }
        void Kill()
        {
            try { if (!process.HasExited) process.Kill(entireProcessTree: true); }
            catch (InvalidOperationException) { }
        }
        var stdout = ReadBoundedAsync(process.StandardOutput);
        var stderr = ReadBoundedAsync(process.StandardError);
        using var timer = CancellationTokenSource.CreateLinkedTokenSource(cancellation);
        timer.CancelAfter(timeout);
        var timedOut = false;
        try
        {
            if (input is not null) await process.StandardInput.WriteAsync(input.AsMemory(), timer.Token);
            process.StandardInput.Close();
            await process.WaitForExitAsync(timer.Token);
        }
        catch (OperationCanceledException)
        {
            Kill();
            await process.WaitForExitAsync(CancellationToken.None);
            cancellation.ThrowIfCancellationRequested();
            timedOut = true;
        }
        catch (IOException) when (process.HasExited) { }
        return new(process.ExitCode, await stdout, await stderr, timedOut, outputLimitExceeded != 0);
    }
}
