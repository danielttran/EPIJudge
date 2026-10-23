using System.Net;
using EpiJudge.Runner;
using EpiJudge.Web;
using Yarp.ReverseProxy.Configuration;

var builder = WebApplication.CreateBuilder(args);
var targetUrl = builder.Configuration["urls"] ?? "http://localhost:5178";
if (builder.Configuration["urls"] is null) builder.WebHost.UseUrls(targetUrl);
builder.WebHost.ConfigureKestrel(options => options.Limits.MaxRequestBodySize = 200_000);

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
builder.Services.AddSingleton<SolutionCatalog>();
builder.Services.AddSingleton(new NativeProblemCatalog(repositoryRoot));
builder.Services.AddSingleton(new SubmissionRunner(repositoryRoot));
builder.Services.AddSingleton(new CodeFormatter(repositoryRoot));
builder.Services.AddSingleton<PracticeDatabase>();
builder.Services.AddSingleton<PracticeStore>();
builder.Services.AddSingleton<IAttemptStore>(services => services.GetRequiredService<PracticeStore>());
builder.Services.AddSingleton<ISubmissionRunner>(services => services.GetRequiredService<SubmissionRunner>());
builder.Services.AddSingleton<SubmissionService>();
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
    if (context.Request.Path is var path && (path == "/api/practice/import" || path == "/api/practice/migrate"))
    {
        var limit = context.Features.Get<Microsoft.AspNetCore.Http.Features.IHttpMaxRequestBodySizeFeature>();
        if (limit is { IsReadOnly: false }) limit.MaxRequestBodySize = 64 * 1024 * 1024;
    }
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

app.MapPost("/api/code/format", async (HttpContext http, FormatRequest request, CodeFormatter formatter) =>
{
    http.Response.Headers.CacheControl = "no-store";
    if (http.Request.Headers["X-EpiJudge-Client"] != "local-editor") return Results.StatusCode(403);
    var result = await formatter.FormatAsync(request.Language ?? "", request.Code ?? "", request.CodeFormat ?? "", http.RequestAborted);
    return result.Error switch
    {
        null => Results.Ok(new { code = result.Code }),
        "invalid" => Results.BadRequest(new { message = result.Message }),
        "busy" => Results.Json(new { message = result.Message }, statusCode: 429),
        "timeout" => Results.Json(new { message = result.Message }, statusCode: 504),
        _ => Results.Json(new { message = result.Message }, statusCode: 503)
    };
});

app.MapGet("/api/languages", () => new[]
{
    new { id = "csharp", name = "C#", runtime = ".NET 10", filename = "Solution.cs", monacoLanguage = "csharp" },
    new { id = "javascript", name = "JavaScript", runtime = "Node.js 24", filename = "solution.js", monacoLanguage = "javascript" },
    new { id = "python", name = "Python", runtime = "Python 3.14", filename = "solution.py", monacoLanguage = "python" },
    new { id = "cpp", name = "C++", runtime = "C++17", filename = "solution.cpp", monacoLanguage = "cpp" },
    new { id = "java", name = "Java", runtime = "Java 21", filename = "Solution.java", monacoLanguage = "java" }
});
app.MapGet("/api/problems", (ProblemCatalog catalog, string? lang) => catalog.Problems.Select(problem =>
{
    var selectedLanguage = lang switch { "js" => "javascript", "py" => "python", null => "csharp", _ => lang };
    var starters = SolutionCatalog.Languages.ToDictionary(language => language, language =>
        CallableCodeCatalog.Find(problem.Id, language)
        ?? throw new InvalidOperationException($"Missing callable starter: {problem.Id}/{language}"));
    var selected = starters.GetValueOrDefault(selectedLanguage) ?? starters["csharp"];
    return new
    {
        problem.Id, problem.Title, problem.Topic, problem.Difficulty, problem.Description,
        problem.Constraints,
        problem.Collection, problem.Position, problem.Diagram, problem.DiagramAlt,
        problem.SourceUrl, problem.SourceAttribution,
        Signature = selected.Signature,
        StarterCode = selected.StarterCode,
        CodeFormat = "callable-v1",
        selected.References,
        JsSignature = starters["javascript"].Signature,
        JsStarterCode = starters["javascript"].StarterCode,
        PySignature = starters["python"].Signature,
        PyStarterCode = starters["python"].StarterCode,
        Starters = starters.ToDictionary(pair => pair.Key, pair => (object)new
        {
            signature = pair.Value.Signature,
            starterCode = pair.Value.StarterCode,
            filename = pair.Value.Filename,
            runtime = pair.Key switch
            {
                "csharp" => "C# .NET 10", "javascript" => "JavaScript Node.js 24",
                "python" => "Python 3.14", "cpp" => "C++17", _ => "Java 21"
            },
            codeFormat = "callable-v1",
            references = pair.Value.References,
            contract = CallableContractCatalog.Find(problem.Id, pair.Key)
        }),
        problem.Examples, problem.TestCount
    };
}));
app.MapGet("/api/problems/{problemId}/solution", (string problemId, string? language, SolutionCatalog solutions) =>
{
    language ??= "csharp";
    if (!SolutionCatalog.Languages.Contains(language, StringComparer.Ordinal))
        return Results.BadRequest(new { message = "Choose a supported solution language." });
    if (solutions.Find(problemId, language) is not { } solution)
        return Results.NotFound(new { message = "No solution is available for this question." });
    var callable = CallableCodeCatalog.Find(problemId, language)
        ?? throw new InvalidOperationException($"Missing callable solution: {problemId}/{language}");
    return Results.Ok(new
    {
        solution.ProblemId, solution.Collection, solution.Language,
        Code = callable.SolutionCode, CodeFormat = "callable-v1", callable.References,
        solution.Explanation, solution.TimeComplexity, solution.SpaceComplexity,
        solution.Attribution, solution.Correctness, solution.Walkthrough, solution.EdgeCases
    });
});
app.MapGet("/api/health", () => new { status = "ready", languages = new[] { "C#", "JavaScript", "Python", "C++", "Java" }, execution = "trusted-local-only" });
app.MapPractice();
app.MapPost("/api/submissions", async (SubmissionRequest request, HttpContext context,
    ProblemCatalog catalog, SubmissionService submissions) =>
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
    var language = request.Language switch { null => "csharp", "js" => "javascript", "py" => "python", _ => request.Language };
    var codeFormat = request.CodeFormat ?? "legacy-v1";
    if (!PracticeEndpoints.ValidCodeFormat(codeFormat))
        return Results.BadRequest(new { message = "Choose a supported code format." });
    var outcome = await submissions.Execute(problem, language, request.Code, request.Mode, context.RequestAborted, codeFormat);
    return outcome.Failure switch
    {
        null => Results.Ok(outcome.Result),
        SubmissionFailure.Busy => Results.Json(new { message = "The runner is busy. Try again in a moment." }, statusCode: 429),
        SubmissionFailure.Interrupted => Results.StatusCode(499),
        SubmissionFailure.Storage => Results.Problem("Could not save the submission or its result. Your browser recovery copy is retained; retry saving.", statusCode: 503),
        _ => Results.Problem("The local runner could not start. Check the server output and runtime dependencies.")
    };
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

public sealed record SubmissionRequest(string? ProblemId, string? Code, string? Mode, string? Language = "csharp",
    string? CodeFormat = "legacy-v1");

public sealed record FormatRequest(string? Language, string? Code, string? CodeFormat);
