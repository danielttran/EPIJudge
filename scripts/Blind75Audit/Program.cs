using System.Text.Json;
using System.Security.Cryptography;
using System.Text;
using System.Reflection;
using EpiJudge.Runner;

var root=ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
ToolchainConfiguration.ApplyLocalOverrides(root);
var runner=new SubmissionRunner(root);
var languages=new[]{"csharp","javascript","python","cpp","java"};
var kind=args.FirstOrDefault()??"all";
var chosen=args.Skip(1).FirstOrDefault();
var selected=args.ElementAtOrDefault(2)?.Split(',').ToHashSet();
string Sha(string text)=>Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text)));
var harnessMethod=typeof(Blind75Catalog).GetMethod("Harness",BindingFlags.NonPublic|BindingFlags.Static)!;
if (kind == "describe")
{
    Directory.CreateDirectory(Path.Combine(root, ".epi-runs"));
    var files = Directory.GetFiles(Path.Combine(root, "EpiJudge.Runner"), "*.cs")
        .Concat(Directory.GetFiles(Path.Combine(root, "blind75", "runtime")))
        .Append(Path.Combine(root, "blind75", "catalog.json"));
    var sourceFiles = files.ToDictionary(p => Path.GetRelativePath(root, p).Replace('\\', '/'), p => Sha(File.ReadAllText(p)));
    var harnesses = Blind75Catalog.Definitions.SelectMany(d => languages.Select(language => new {
        problem=d.Id, language, harnessSha256=Sha((string)harnessMethod.Invoke(null, [d,language])!)
    }));
    File.WriteAllText(Path.Combine(root, ".epi-runs", "blind75-harnesses.json"), JsonSerializer.Serialize(new {sourceFiles,harnesses}));
    Console.WriteLine("Wrote current compiled harness and source fingerprints.");
    return 0;
}
var rows=new List<object>();
var failures=0;
foreach(var language in languages.Where(l=>chosen is null||l==chosen))
foreach(var def in Blind75Catalog.Definitions.Where(d=>selected is null||selected.Contains(d.Id)))
{
    var problem=Blind75Catalog.Problems.Single(p=>p.Id==def.Id);
    foreach(var variant in new[]{"starter","correct","incorrect","adversarial"}.Where(v=>kind=="all"?v!="adversarial":v==kind))
    {
        var filename=def.Starters[language].Filename;
        var path=Path.Combine(root,"scripts","blind75","fixtures",variant,language,def.Id,filename);
        if (variant=="adversarial" && !File.Exists(path)) continue;
        var code=variant=="starter"?def.Starters[language].StarterCode:File.ReadAllText(path);
        var result=await runner.RunAsync(problem,code,false,language,CancellationToken.None);
        var success=variant switch
        {
            "starter"=>result?.Status is "Accepted" or "Wrong answer",
            "correct"=>result?.Status=="Accepted"&&result.Passed==problem.TestCount,
            _=>result?.Status=="Wrong answer"&&result.Passed<problem.TestCount
        };
        if(!success)failures++;
        var row=new{language,problem=problem.Id,variant,success,result,codeSha256=Sha(code),corpusSha256=Sha(File.ReadAllText(Path.Combine(root,"blind75","cases",def.Id+".json"))),harnessSha256=Sha((string)harnessMethod.Invoke(null,[def,language])!)};rows.Add(row);
        Console.WriteLine($"{(success?"PASS":"FAIL")} {language} {variant} {problem.Id} {result?.Status} {result?.Passed}/{result?.Total}");
        if(!success)Console.WriteLine(result?.Diagnostics??JsonSerializer.Serialize(result));
        var report=Path.Combine(root,".epi-runs","blind75-audit-"+kind+(chosen is null?"":"-"+chosen)+(selected is null?"":"-"+Sha(string.Join(",",selected.Order()))[..8])+".json");
        Directory.CreateDirectory(Path.GetDirectoryName(report)!);
        File.WriteAllText(report,JsonSerializer.Serialize(rows,new JsonSerializerOptions{WriteIndented=true}));
    }
}
Console.WriteLine($"Completed {rows.Count} executions; {failures} failures.");
return failures==0?0:1;
