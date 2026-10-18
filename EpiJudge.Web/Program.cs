using System.Net;
using EpiJudge.Runner;
using EpiJudge.Web;
using Yarp.ReverseProxy.Configuration;

var builder = WebApplication.CreateBuilder(args);
var targetUrl = builder.Configuration["urls"] ?? "http://localhost:5178";
if (builder.Configuration["urls"] is null) builder.WebHost.UseUrls(targetUrl);
builder.WebHost.ConfigureKestrel(options => options.Limits.MaxRequestBodySize = 100_000);

if (builder.Environment.IsDevelopment())
{
    foreach (var url in targetUrl.Split(';', StringSplitOptions.RemoveEmptyEntries))
    {
        if (Uri.TryCreate(url.Replace("*", "127.0.0.1").Replace("+", "127.0.0.1"), UriKind.Absolute, out var uri))
        {
            await PortReclaimer.EnsurePortAvailableAsync(uri.Port);
        }
    }
}
var repositoryRoot = ProblemCatalog.FindRepositoryRoot(builder.Environment.ContentRootPath);
ToolchainConfiguration.ApplyLocalOverrides(repositoryRoot);
builder.Services.AddSingleton<ProblemCatalog>();
builder.Services.AddSingleton(new NativeProblemCatalog(repositoryRoot));
builder.Services.AddSingleton(new SubmissionRunner(repositoryRoot));
var serveReact = builder.Environment.IsDevelopment() && builder.Configuration.GetValue("Frontend:Enabled", true);
if (serveReact)
{
    // Each web host owns its frontend; overlapping restarts must not share a
    // Vite child that the previous host will shut down.
    var vitePort = builder.Configuration.GetValue<int?>("Frontend:Port") ?? FrontendDevelopmentServer.FindAvailablePort();
    builder.Configuration["Frontend:Port"] = vitePort.ToString();
    builder.Services.AddHostedService<FrontendDevelopmentServer>();
    builder.Services.AddReverseProxy().LoadFromMemory(
        [new RouteConfig { RouteId = "react", ClusterId = "vite", Order = 100, Match = new RouteMatch { Path = "/{**path}" } }],
        [new ClusterConfig { ClusterId = "vite", Destinations = new Dictionary<string, DestinationConfig>
            { ["local"] = new() { Address = $"http://127.0.0.1:{vitePort}/" } } }]);
}
var app = builder.Build();

// This first version executes trusted, local practice code. It is not a public sandbox.
app.Use(async (context, next) =>
{
    if (context.Connection.RemoteIpAddress is not { } address || !IPAddress.IsLoopback(address))
    {
        context.Response.StatusCode = StatusCodes.Status403Forbidden;
        return;
    }
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    await next();
});

var clientDist = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "../epijudge.client/dist"));
var hasBuiltClient = Directory.Exists(clientDist) && File.Exists(Path.Combine(clientDist, "index.html"));

if (!serveReact) app.UseDefaultFiles();
app.UseStaticFiles();
if (hasBuiltClient && (!Directory.Exists(app.Environment.WebRootPath) || !File.Exists(Path.Combine(app.Environment.WebRootPath ?? "", "index.html"))))
{
    app.UseStaticFiles(new StaticFileOptions
    {
        FileProvider = new Microsoft.Extensions.FileProviders.PhysicalFileProvider(clientDist)
    });
}

app.MapGet("/api/languages", () => new[]
{
    new { id = "csharp", name = "C#", runtime = ".NET 10", filename = "Solution.cs", monacoLanguage = "csharp" },
    new { id = "javascript", name = "JavaScript", runtime = "Node.js 24", filename = "solution.js", monacoLanguage = "javascript" },
    new { id = "python", name = "Python", runtime = "Python 3.14", filename = "solution.py", monacoLanguage = "python" },
    new { id = "cpp", name = "C++", runtime = "C++17", filename = "solution.cpp", monacoLanguage = "cpp" },
    new { id = "java", name = "Java", runtime = "Java 21", filename = "Solution.java", monacoLanguage = "java" }
});
app.MapGet("/api/problems", (ProblemCatalog catalog, NativeProblemCatalog native, string? lang) => catalog.Problems.Select(problem =>
{
    var isJs = lang is "javascript" or "js";
    var isPy = lang is "python" or "py";
    var nativeStarter = lang is "cpp" or "java" ? native.GetStarter(lang, problem.Id) : null;
    return new
    {
        problem.Id, problem.Title, problem.Topic, problem.Difficulty, problem.Description,
        problem.Constraints,
        Signature = nativeStarter?.Signature ?? (isPy ? (problem.PySignature ?? problem.Signature) : isJs ? (problem.JsSignature ?? problem.Signature) : problem.Signature),
        StarterCode = nativeStarter?.StarterCode ?? (isPy ? (problem.PyStarterCode ?? problem.StarterCode) : isJs ? (problem.JsStarterCode ?? problem.StarterCode) : problem.StarterCode),
        problem.JsSignature,
        problem.JsStarterCode,
        problem.PySignature,
        problem.PyStarterCode,
        Starters = new Dictionary<string, object>
        {
            ["csharp"] = new { signature = problem.Signature, starterCode = problem.StarterCode, filename = "Solution.cs", runtime = "C# .NET 10" },
            ["javascript"] = new { signature = problem.JsSignature ?? problem.Signature, starterCode = problem.JsStarterCode ?? problem.StarterCode, filename = "solution.js", runtime = "JavaScript Node.js 24" },
            ["python"] = new { signature = problem.PySignature ?? problem.Signature, starterCode = problem.PyStarterCode ?? problem.StarterCode, filename = "solution.py", runtime = "Python 3.14" },
            ["cpp"] = native.GetStarter("cpp", problem.Id),
            ["java"] = native.GetStarter("java", problem.Id)
        },
        problem.Examples, problem.TestCount
    };
}));
app.MapGet("/api/health", () => new { status = "ready", languages = new[] { "C#", "JavaScript", "Python", "C++", "Java" }, execution = "trusted-local-only" });
app.MapPost("/api/submissions", async (SubmissionRequest request, HttpContext context,
    ProblemCatalog catalog, SubmissionRunner runner, ILogger<Program> logger) =>
{
    if (!app.Environment.IsDevelopment()) return Results.Problem("Local code execution requires the Development environment.", statusCode: 503);
    if (context.Request.Headers["X-EpiJudge-Client"] != "local-editor") return Results.StatusCode(403);
    var problem = catalog.Find(request.ProblemId ?? "");
    if (problem is null) return Results.BadRequest(new { message = "Choose a supported problem." });
    if (request.Mode is not ("run" or "submit")) return Results.BadRequest(new { message = "Mode must be run or submit." });
    if (request.Language is not (null or "csharp" or "javascript" or "js" or "python" or "py" or "cpp" or "java"))
        return Results.BadRequest(new { message = "Choose a supported programming language." });
    if (string.IsNullOrWhiteSpace(request.Code) || request.Code.Length > 40_000)
        return Results.BadRequest(new { message = "Code must contain between 1 and 40,000 characters." });
    try
    {
        var result = await runner.RunAsync(problem, request.Code, request.Mode == "run", request.Language ?? "csharp", context.RequestAborted);
        return result is null ? Results.Json(new { message = "The runner is busy. Try again in a moment." }, statusCode: 429) : Results.Ok(result);
    }
    catch (OperationCanceledException) when (context.RequestAborted.IsCancellationRequested) { return Results.StatusCode(499); }
    catch (Exception exception)
    {
        logger.LogError(exception, "Submission execution failed");
        return Results.Problem("The local runner could not start. Check the server output and runtime dependencies.");
    }
});
app.MapPost("/api/internal/shutdown", (IHostApplicationLifetime lifetime) =>
{
    _ = Task.Run(async () =>
    {
        await Task.Delay(100);
        lifetime.StopApplication();
    });
    return Results.Ok(new { status = "shutting_down" });
});
// Unknown API routes must not be forwarded back through Vite's API proxy.
app.MapMethods("/api/{**path}", ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"], () => Results.NotFound());
if (serveReact)
{
    app.MapReverseProxy();
}
else if (hasBuiltClient)
{
    var distProvider = new Microsoft.Extensions.FileProviders.PhysicalFileProvider(clientDist);
    app.MapFallbackToFile("index.html", new StaticFileOptions { FileProvider = distProvider });
}
else
{
    app.MapFallbackToFile("index.html");
}
app.Run();

public sealed record SubmissionRequest(string? ProblemId, string? Code, string? Mode, string? Language = "csharp");
