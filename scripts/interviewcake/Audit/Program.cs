using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using EpiJudge.Runner;
var root=ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
ToolchainConfiguration.ApplyLocalOverrides(root);
var language=args.ElementAtOrDefault(0);if(language=="all")language=null;
var kind=args.ElementAtOrDefault(1)??"all";var selected=args.ElementAtOrDefault(2)?.Split(',').ToHashSet();
if(language is not null&&!SolutionCatalog.Languages.Contains(language))throw new ArgumentException("Choose one of the five supported languages or all.");
if(kind is not ("all" or "starter" or "correct" or "incorrect"))throw new ArgumentException("Choose all, starter, correct or incorrect.");
if(selected is not null&&selected.Any(id=>InterviewCakeCatalog.Find(id) is null))throw new ArgumentException("Unknown Interview Cake problem ID.");
var evidence=new List<object>();int failures=0;
string Sha(string text)=>Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text)));
var runnerMethod=typeof(SubmissionRunner).Assembly.GetType("EpiJudge.Runner.InterviewCakeSubmissionRunner")!.GetMethod("RunAsync",BindingFlags.NonPublic|BindingFlags.Static)!;
var harness=typeof(InterviewCakeCatalog).GetMethod("Harness",BindingFlags.NonPublic|BindingFlags.Static)!;
var directory=Path.Combine(root,".epi-runs");Directory.CreateDirectory(directory);
var runId=DateTime.UtcNow.ToString("yyyyMMddTHHmmss",System.Globalization.CultureInfo.InvariantCulture)+"-"+Guid.NewGuid().ToString("N")[..8];
string Resource(string name){using var stream=typeof(SubmissionRunner).Assembly.GetManifestResourceStream(name)??throw new InvalidOperationException("Missing audit resource "+name);using var reader=new StreamReader(stream);return reader.ReadToEnd();}
var runnerSha256=Sha(Resource("EpiJudge.Runner.InterviewCakeSubmissionRunner.source"));
var catalogSha256=Sha(Resource("EpiJudge.Runner.interviewcake.json"));
if(runnerSha256!=Sha(File.ReadAllText(Path.Combine(root,"EpiJudge.Runner/InterviewCakeSubmissionRunner.cs"))))throw new InvalidOperationException("The compiled Interview Cake runner is stale; rebuild the audit project.");
if(catalogSha256!=Sha(File.ReadAllText(Path.Combine(root,"interviewcake/catalog.json"))))throw new InvalidOperationException("The compiled Interview Cake catalog is stale; rebuild the audit project.");
foreach(var lang in SolutionCatalog.Languages.Where(l=>language is null||l==language))
foreach(var def in InterviewCakeCatalog.Definitions.Where(d=>selected is null||selected.Contains(d.Id)))
foreach(var variant in new[]{"starter","correct","incorrect"}.Where(v=>kind=="all"||v==kind))
{
    var extension=lang switch{"csharp"=>"cs","javascript"=>"js","python"=>"py","cpp"=>"cpp",_=>"java"};
    var code=variant=="starter"?def.Starters[lang].StarterCode:File.ReadAllText(Path.Combine(root,variant=="correct"?"solutions":"interviewcake/fixtures/incorrect",lang,def.Id+"."+extension));
    var problem=InterviewCakeCatalog.Problems.Single(p=>p.Id==def.Id);
    var attemptId=Guid.NewGuid().ToString("N");var attemptDirectory=Path.Combine(directory,attemptId);
    // Invoke the same typed runner used by public submissions, retaining its report
    // until this audit checks every executed row. Public runner cleanup is tested separately.
    var result=await (Task<SubmissionResult>)runnerMethod.Invoke(null,[root,attemptDirectory,attemptId,problem,def,code,false,lang,CancellationToken.None])!;
    var executionPath=Path.Combine(attemptDirectory,"results.json");var executionReportRows=0;string? executionReportSha256=null;
    if(File.Exists(executionPath))
    {
        var text=File.ReadAllText(executionPath);using var report=JsonDocument.Parse(text);
        if(report.RootElement.ValueKind==JsonValueKind.Array)executionReportRows=report.RootElement.GetArrayLength();
        executionReportSha256=Sha(text);
        var archive=Path.Combine(directory,"interviewcake-executions",runId,lang);Directory.CreateDirectory(archive);File.WriteAllText(Path.Combine(archive,def.Id+"-"+variant+".json"),text);
    }
    var success=variant switch{
        "correct"=>result is{Status:"Accepted"}&&result.Passed==problem.TestCount,
        "starter"=>result is not null&&result.Total==problem.TestCount&&result.Cases.Count>0&&result.Status is "Accepted" or "Wrong answer" or "Runtime error",
        _=>result is not null&&result.Passed<problem.TestCount&&result.Status is "Wrong answer" or "Runtime error"
    };
    success=success&&executionReportRows==problem.TestCount;
    if(!success)failures++;
    evidence.Add(new{problemId=problem.Id,language=lang,variant,success,result,executionReportRows,executionReportSha256,codeSha256=Sha(code),corpusSha256=Sha(File.ReadAllText(Path.Combine(root,"interviewcake/cases",def.Id+".json"))),harnessSha256=Sha((string)harness.Invoke(null,[def,lang])!)});
    Console.WriteLine($"{(success?"PASS":"FAIL")} {lang} {variant} {problem.Id} {result?.Status} {result?.Passed}/{result?.Total}");
    if(!success)Console.WriteLine(result?.Diagnostics??JsonSerializer.Serialize(result));
    File.WriteAllText(Path.Combine(directory,$"interviewcake-audit-{language??"all"}-{kind}-{runId}.json"),JsonSerializer.Serialize(new{runId,runnerSha256,catalogSha256,entryPoint="InterviewCakeSubmissionRunner.RunAsync (the public submission route uses this same implementation)",evidence,failures},new JsonSerializerOptions{WriteIndented=true}));
    try{if(Directory.Exists(attemptDirectory))Directory.Delete(attemptDirectory,true);}catch(IOException){}catch(UnauthorizedAccessException){}
}
Console.WriteLine($"Completed {evidence.Count} executions; {failures} failures.");return failures==0?0:1;
