using System.Net;
using EpiJudge.Runner;
using EpiJudge.Web;
using Yarp.ReverseProxy.Configuration;

var builder = WebApplication.CreateBuilder(args);
if (builder.Configuration["urls"] is null) builder.WebHost.UseUrls("http://localhost:5178");
builder.WebHost.ConfigureKestrel(options => options.Limits.MaxRequestBodySize = 100_000);
var repositoryRoot = ProblemCatalog.FindRepositoryRoot(builder.Environment.ContentRootPath);
builder.Services.AddSingleton<ProblemCatalog>();
builder.Services.AddSingleton(new SubmissionRunner(repositoryRoot));
var serveReact = builder.Environment.IsDevelopment() && builder.Configuration.GetValue("Frontend:Enabled", true);
if (serveReact)
{
    var vitePort = builder.Configuration.GetValue("Frontend:Port", 5173);
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
app.UseDefaultFiles();
app.UseStaticFiles();

app.MapGet("/api/problems", (ProblemCatalog catalog) => catalog.Problems.Select(problem => new
{
    problem.Id, problem.Title, problem.Topic, problem.Difficulty, problem.Description,
    problem.Constraints, problem.Signature, problem.StarterCode, problem.Examples
}));
app.MapGet("/api/health", () => new { status = "ready", language = "C#", runtime = ".NET 10", execution = "trusted-local-only" });
app.MapPost("/api/submissions", async (SubmissionRequest request, HttpContext context,
    ProblemCatalog catalog, SubmissionRunner runner, ILogger<Program> logger) =>
{
    if (!app.Environment.IsDevelopment()) return Results.Problem("Local code execution requires the Development environment.", statusCode: 503);
    if (context.Request.Headers["X-EpiJudge-Client"] != "local-editor") return Results.StatusCode(403);
    var problem = catalog.Find(request.ProblemId ?? "");
    if (problem is null) return Results.BadRequest(new { message = "Choose a supported problem." });
    if (request.Mode is not ("run" or "submit")) return Results.BadRequest(new { message = "Mode must be run or submit." });
    if (string.IsNullOrWhiteSpace(request.Code) || request.Code.Length > 40_000)
        return Results.BadRequest(new { message = "Code must contain between 1 and 40,000 characters." });
    try
    {
        var result = await runner.RunAsync(problem, request.Code, request.Mode == "run", context.RequestAborted);
        return result is null ? Results.Json(new { message = "The runner is busy. Try again in a moment." }, statusCode: 429) : Results.Ok(result);
    }
    catch (OperationCanceledException) when (context.RequestAborted.IsCancellationRequested) { return Results.StatusCode(499); }
    catch (Exception exception)
    {
        logger.LogError(exception, "Submission execution failed");
        return Results.Problem("The local runner could not start. Check the server output and that the .NET 10 SDK is installed.");
    }
});
// Unknown API routes must not be forwarded back through Vite's API proxy.
app.MapMethods("/api/{**path}", ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"], () => Results.NotFound());
if (serveReact) app.MapReverseProxy();
else app.MapFallbackToFile("index.html");
app.Run();

public sealed record SubmissionRequest(string? ProblemId, string? Code, string? Mode);
