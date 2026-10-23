using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using EpiJudge.Runner;

var root=ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
ToolchainConfiguration.ApplyLocalOverrides(root);
var catalog=new ProblemCatalog();
var native=new NativeProblemCatalog(root);
var languages=SolutionCatalog.Languages;
var extensions=new Dictionary<string,string>{{"csharp","cs"},{"javascript","js"},{"python","py"},{"cpp","cpp"},{"java","java"}};
var json=new JsonSerializerOptions{WriteIndented=true,PropertyNameCaseInsensitive=true};
string Sha(string text)=>Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text)));
string FileSha(string path)=>Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
var coveragePath=Path.Combine(root,"solutions","coverage.json");
if(args.Contains("inventory"))
{
    var entries=catalog.Problems.SelectMany(p=>languages.Select(language=>new {
        problemId=p.Id,collection=p.Collection,language,testCount=p.TestCount,
        codePath=$"solutions/{language}/{p.Id}.{extensions[language]}",
        notesPath=language=="csharp"?$"solutions/notes/{p.Id}.json":$"solutions/notes/{language}/{p.Id}.json",
        filename=language is "cpp" or "java"?native.GetStarter(language,p.Id).Filename:language=="csharp"?"Solution.cs":language=="python"?"solution.py":"solution.js"
    }));
    Directory.CreateDirectory(Path.GetDirectoryName(coveragePath)!);
    File.WriteAllText(coveragePath,JsonSerializer.Serialize(new {schemaVersion=2,baseCommit="2b5d19f2361a9199b2b46406c17bb8b9f71305eb",
        questionCount=catalog.Problems.Count,languages,collections=catalog.Problems.GroupBy(p=>p.Collection).ToDictionary(g=>g.Key,g=>g.Count()),
        pendingSources=Array.Empty<object>(),entries},json)+"\n");
    Console.WriteLine($"Recorded {catalog.Problems.Count} questions and {catalog.Problems.Count*languages.Length} language combinations.");return 0;
}
var files=args.Contains("--files");
var callable=args.Contains("--callable");
var starters=args.Contains("--starters");
if(starters&&!callable)throw new ArgumentException("Starter acceptance requires the explicit callable contract.");
if(files&&callable)throw new ArgumentException("Callable acceptance must use embedded displayed metadata.");
var chosen=args.FirstOrDefault(a=>a.StartsWith("--ids="))?[6..].Split(',').ToHashSet();
var batch=args.FirstOrDefault(a=>a.StartsWith("--batch="))?[8..];
if(batch is not null)chosen=JsonSerializer.Deserialize<string[]>(File.ReadAllText(Path.Combine(root,"scripts","solutions",$"batch-{batch}.json")))!.ToHashSet();
var selectedLanguage=args.FirstOrDefault(a=>a.StartsWith("--language="))?[11..];
if(selectedLanguage is not null&&!languages.Contains(selectedLanguage))throw new ArgumentException("Unknown language.");
var selectedCollection=args.FirstOrDefault(a=>a.StartsWith("--collection="))?[13..];
var reportName=args.FirstOrDefault(a=>a.StartsWith("--report="))?[9..]??(batch is null?"all":"batch-"+batch)+(selectedLanguage is null?"":"-"+selectedLanguage);
if(reportName.Any(c=>!char.IsLetterOrDigit(c)&&c!='-'&&c!='_'))throw new ArgumentException("Invalid report name.");
var manifest=JsonSerializer.Deserialize<Coverage>(File.ReadAllText(coveragePath),json)!;
var expected=catalog.Problems.SelectMany(p=>languages.Select(language=>(p.Id,language))).ToHashSet();
if(manifest.Entries.Length!=expected.Count||!manifest.Entries.Select(e=>(e.ProblemId,e.Language)).ToHashSet().SetEquals(expected))
    throw new InvalidOperationException("Coverage must enumerate every live question/language combination exactly once.");
if(chosen is not null&&chosen.Except(catalog.Problems.Select(p=>p.Id)).Any())throw new ArgumentException("Unknown requested problem ID.");
var sourcePaths=Directory.GetFiles(Path.Combine(root,"EpiJudge.Runner"),"*",SearchOption.AllDirectories)
    .Where(p=>!p.Split(Path.DirectorySeparatorChar).Any(s=>s is "obj" or "bin")&&Path.GetExtension(p) is ".cs" or ".csproj" or ".json" or ".js" or ".h" or ".txt")
    .Concat(Directory.GetFiles(Path.Combine(root,"EpiJudge.TestFramework"),"*.cs",SearchOption.AllDirectories).Where(p=>!p.Split(Path.DirectorySeparatorChar).Any(s=>s is "obj" or "bin")))
    .Concat(Directory.GetFiles(Path.Combine(root,"blind75","runtime"))).Append(Path.Combine(root,"blind75","catalog.json"))
    .Concat(Directory.GetFiles(Path.Combine(root,"interviewcake","runtime"))).Append(Path.Combine(root,"interviewcake","catalog.json"))
    .Append(Path.Combine(root,"ctci6","catalog.json")).Append(Path.Combine(root,"ctci6","practice","catalog.json")).Append(Path.Combine(root,"ctci6","practice","coverage.json"));
if(callable)sourcePaths=sourcePaths.Append(Path.Combine(root,"workspace-code","catalog.json"));
var sourceHashes=sourcePaths.Distinct().Order().ToDictionary(p=>Path.GetRelativePath(root,p).Replace('\\','/'),FileSha);
string Harness(Problem p,string language)
{
    if(Blind75Catalog.Find(p.Id) is {} blind)return (string)typeof(Blind75Catalog).GetMethod("Harness",BindingFlags.NonPublic|BindingFlags.Static)!.Invoke(null,[blind,language])!;
    if(InterviewCakeCatalog.Find(p.Id) is {} cake)return (string)typeof(InterviewCakeCatalog).GetMethod("Harness",BindingFlags.NonPublic|BindingFlags.Static)!.Invoke(null,[cake,language])!;
    if(CtciCatalog.Find(p.Id) is {} ctci)return ctci.Languages[language].Harness;
    if(language is "cpp" or "java")
    {
        var name=language=="cpp"?"web_test.h":"java_run_tests.txt";
        using var stream=typeof(SubmissionRunner).Assembly.GetManifestResourceStream("EpiJudge.Runner.NativeHarnesses."+name)!;
        using var reader=new StreamReader(stream);return reader.ReadToEnd();
    }
    var method=language switch{"javascript"=>"CreateJsHarness","python"=>"CreatePyHarness",_=>"CreateHarness"};
    return (string)typeof(SubmissionRunner).GetMethod(method,BindingFlags.NonPublic|BindingFlags.Static)!.Invoke(null,language=="python"?[p,root,false]:[p])!;
}
var artifactRoot=Path.Combine(root,".epi-runs");Directory.CreateDirectory(artifactRoot);
if(args.Contains("describe"))
{
    var harnesses=catalog.Problems.SelectMany(p=>languages.Select(language=>new{problemId=p.Id,language,harnessSha256=Sha(Harness(p,language))}));
    File.WriteAllText(Path.Combine(artifactRoot,"solutions-harnesses.json"),JsonSerializer.Serialize(new{sourceHashes,harnesses},json)+"\n");
    Console.WriteLine("Recorded all current compiled harness fingerprints.");return 0;
}
var embedded=files?null:new SolutionCatalog(catalog);
var callableEntries=callable?JsonSerializer.Deserialize<CallableSource>(File.ReadAllText(Path.Combine(root,"workspace-code","catalog.json")),json)!.Entries:null;
string VisibleCode(Problem problem,string language)
{
    if(!callable)return embedded!.Find(problem.Id,language)!.Code;
    var entry=CallableCodeCatalog.Find(problem.Id,language)??throw new InvalidOperationException("Missing callable contract.");
    var source=callableEntries!.Single(e=>e.ProblemId==problem.Id&&e.Language==language);
    if(entry!=source&&!JsonSerializer.Serialize(entry).Equals(JsonSerializer.Serialize(source),StringComparison.Ordinal))
        throw new InvalidOperationException("Embedded callable code differs from checked-in source; rebuild the audit.");
    return starters?entry.StarterCode:entry.SolutionCode;
}
PreparedCode PrepareCode(Problem problem,string language,string code)=>CallableCodeCatalog.Prepare(problem.Id,language,code,callable?CallableCodeCatalog.CallableFormat:CallableCodeCatalog.LegacyFormat);
var failures=0;
var rows=new List<object>();
var walkthroughs=args.Contains("walkthroughs");
if(args.Contains("boundaries")||walkthroughs)
{
    if(files)throw new ArgumentException("Boundary acceptance must use displayed embedded code.");
    string WalkthroughPath(Problem p) => Path.Combine(root,"solutions","notes",
        selectedLanguage is null or "csharp" ? "" : selectedLanguage,p.Id+".json");
    var walkthroughProblems=catalog.Problems.Where(p=>chosen is null||chosen.Contains(p.Id)).ToArray();
    var paths=walkthroughs?walkthroughProblems.Select(WalkthroughPath).ToArray():Directory.GetFiles(Path.Combine(root,"scripts","solutions"),"boundaries-*.json").Order().ToArray();
    var cases=walkthroughs?walkthroughProblems.Select(p=>
    {
        using var notes=JsonDocument.Parse(File.ReadAllText(WalkthroughPath(p)));
        var example=notes.RootElement.GetProperty("walkthroughCase");
        return new Boundary(p.Id,example.GetProperty("arguments").EnumerateArray().Select(a=>a.Clone()).ToArray(),example.GetProperty("expected").Clone(),"Original solution walkthrough");
    }).ToArray():paths.SelectMany(path=>JsonSerializer.Deserialize<Boundary[]>(File.ReadAllText(path),json)!).ToArray();
    var diagnosticLabel=(callable?"callable-":"")+(walkthroughs?"walkthroughs":"boundaries");
    var temporaryRoot=Path.Combine(artifactRoot,"solutions-boundaries-"+Guid.NewGuid().ToString("N"));
    Directory.CreateDirectory(Path.Combine(temporaryRoot,"test_data"));Directory.CreateDirectory(Path.Combine(temporaryRoot,"blind75","cases"));Directory.CreateDirectory(Path.Combine(temporaryRoot,"interviewcake","cases"));Directory.CreateDirectory(Path.Combine(temporaryRoot,"ctci6","cases"));
    void CopyDirectory(string source,string destination)
    {
        Directory.CreateDirectory(destination);
        foreach(var path in Directory.GetFiles(source))File.Copy(path,Path.Combine(destination,Path.GetFileName(path)));
        foreach(var path in Directory.GetDirectories(source).Where(p=>Path.GetFileName(p)!="__pycache__"))CopyDirectory(path,Path.Combine(destination,Path.GetFileName(path)));
    }
    if(selectedLanguage!="csharp")foreach(var folder in new[]{"epi_judge_cpp","epi_judge_java","epi_judge_python"})CopyDirectory(Path.Combine(root,folder),Path.Combine(temporaryRoot,folder));
    var runner=new SubmissionRunner(temporaryRoot);
    try
    {
        foreach(var group in cases.Where(c=>chosen is null||chosen.Contains(c.ProblemId)).GroupBy(c=>c.ProblemId))
        {
            var problem=catalog.Find(group.Key)??throw new InvalidOperationException("Unknown boundary ID.");var subset=group.ToArray();
            if(problem.Collection is "blind75" or "interviewcake" or "ctci6")
                File.WriteAllText(Path.Combine(temporaryRoot,problem.Collection,"cases",problem.Id+".json"),JsonSerializer.Serialize(subset.Select(c=>new{arguments=c.Arguments,expected=c.Expected}),json));
            else
            {
                var header=File.ReadLines(Path.Combine(root,"test_data",problem.Id+".tsv")).First();
                File.WriteAllLines(Path.Combine(temporaryRoot,"test_data",problem.Id+".tsv"),new[]{header}.Concat(subset.Select(c=>string.Join('\t',c.Arguments.Select(a=>JsonSerializer.Serialize(a)).Concat(problem.ResultType=="void"?["boundary"]:[JsonSerializer.Serialize(c.Expected),"boundary"])))));
            }
            foreach(var language in languages.Where(l=>selectedLanguage is null?(!walkthroughs||l=="csharp"):l==selectedLanguage))
            {
                var code=VisibleCode(problem,language);SubmissionResult? outcome=null;string? error=null;
                try{var prepared=PrepareCode(problem,language,code);outcome=await runner.RunAsync(problem with{TestCount=subset.Length},prepared.Code,false,language,CancellationToken.None);if(outcome is not null)outcome=CallableCodeCatalog.MapResult(outcome,prepared);}catch(Exception ex){error=ex.ToString();}
                var success=outcome?.Status=="Accepted"&&outcome.Passed==subset.Length&&outcome.Total==subset.Length;
                if(!success)failures++;
                rows.Add(new{problemId=problem.Id,language,success,codeFormat=callable?CallableCodeCatalog.CallableFormat:CallableCodeCatalog.LegacyFormat,codeSha256=Sha(code),composedCodeSha256=Sha(PrepareCode(problem,language,code).Code),cases=subset,result=outcome,failure=error});
                Console.WriteLine($"{(success?"PASS":"FAIL")} {diagnosticLabel} {language} {problem.Id} {outcome?.Status} {outcome?.Passed}/{subset.Length}");
                if(!success)Console.WriteLine(error??JsonSerializer.Serialize(outcome,json));
                File.WriteAllText(Path.Combine(artifactRoot,"solutions-"+diagnosticLabel+(selectedLanguage is null?"":"-"+selectedLanguage)+".json"),JsonSerializer.Serialize(new{sourceHashes,fixtureHashes=paths.ToDictionary(p=>Path.GetRelativePath(root,p).Replace('\\','/'),FileSha),executions=rows,totalCases=cases.Count(c=>chosen is null||chosen.Contains(c.ProblemId))*languages.Count(l=>selectedLanguage is null?(!walkthroughs||l=="csharp"):l==selectedLanguage),failures},json)+"\n");
            }
        }
    }
    finally{Directory.Delete(temporaryRoot,true);}
    Console.WriteLine($"Completed {rows.Count} boundary question/language executions; {failures} failures.");return failures==0?0:1;
}
var liveRunner=new SubmissionRunner(root);
foreach(var problem in catalog.Problems.Where(p=>(chosen is null||chosen.Contains(p.Id))&&(selectedCollection is null||p.Collection==selectedCollection)))
foreach(var language in languages.Where(l=>selectedLanguage is null||l==selectedLanguage))
{
    var entry=manifest.Entries.Single(e=>e.ProblemId==problem.Id&&e.Language==language);
    var codePath=Path.Combine(root,entry.CodePath);var notesPath=Path.Combine(root,entry.NotesPath);
    SubmissionResult? result=null;string? failure=null;var code="";
    try
    {
        code=files?File.ReadAllText(codePath):VisibleCode(problem,language);
        if(!callable&&code!=File.ReadAllText(codePath))throw new InvalidOperationException("Displayed embedded code differs from source; rebuild the audit.");
        if(!files)
        {
            var displayed=embedded!.Find(problem.Id,language)!;
            using var notes=JsonDocument.Parse(File.ReadAllText(notesPath));var metadata=notes.RootElement;
            string? Text(string key)=>metadata.TryGetProperty(key,out var field)&&field.ValueKind==JsonValueKind.String?field.GetString():null;
            var edges=metadata.TryGetProperty("edgeCases",out var edgeCases)&&edgeCases.ValueKind==JsonValueKind.Array?edgeCases.EnumerateArray().Select(v=>v.GetString()!).ToArray():null;
            if(displayed.Explanation!=Text("explanation")||displayed.TimeComplexity!=Text("timeComplexity")||displayed.SpaceComplexity!=Text("spaceComplexity")||
                displayed.Attribution!=Text("attribution")||displayed.Correctness!=Text("correctness")||displayed.Walkthrough!=Text("walkthrough")||
                (displayed.EdgeCases is null)!=(edges is null)||(edges is not null&&!displayed.EdgeCases!.SequenceEqual(edges)))
                throw new InvalidOperationException("Displayed explanation differs from source notes; rebuild the resource and audit.");
        }
        if(code.Length>40_000)throw new InvalidOperationException("Solution exceeds the submission API code limit.");
        var prepared=PrepareCode(problem,language,code);
        result=await liveRunner.RunAsync(problem,prepared.Code,false,language,CancellationToken.None);
        if(result is not null)result=CallableCodeCatalog.MapResult(result,prepared);
        var successStatus=starters
            ? result?.Status=="Accepted"&&result.Passed==problem.TestCount || result is {Status:"Wrong answer" or "Runtime error",Cases.Count:>0}
            : result?.Status=="Accepted"&&result.Passed==problem.TestCount;
        if(!successStatus||result?.Total!=problem.TestCount)failure=result?.Diagnostics??JsonSerializer.Serialize(result);
    }
    catch(Exception ex){failure=ex.ToString();}
    var success=failure is null;if(!success)failures++;
    var corpus=problem.Collection is "blind75" or "interviewcake" or "ctci6"?Path.Combine(root,problem.Collection,"cases",problem.Id+".json"):Path.Combine(root,"test_data",problem.Id+".tsv");
    rows.Add(new{problemId=problem.Id,collection=problem.Collection,language,success,displayedEmbeddedCode=!files,codeFormat=callable?CallableCodeCatalog.CallableFormat:CallableCodeCatalog.LegacyFormat,role=starters?"starter":"solution",codeSha256=Sha(code),composedCodeSha256=Sha(PrepareCode(problem,language,code).Code),notesSha256=File.Exists(notesPath)?FileSha(notesPath):null,corpusSha256=FileSha(corpus),harnessSha256=Sha(Harness(problem,language)),result,failure});
    File.WriteAllText(Path.Combine(artifactRoot,"solutions-audit-"+reportName+".json"),JsonSerializer.Serialize(new{schemaVersion=2,sourceHashes,executions=rows},json)+"\n");
    Console.WriteLine($"{(success?"PASS":"FAIL")} {language} {problem.Id} {result?.Status} {result?.Passed}/{result?.Total}");if(failure is not null)Console.WriteLine(failure);
}
Console.WriteLine($"Recorded {rows.Count} complete-corpus executions; {failures} failures.");return failures==0?0:1;
internal sealed record Coverage(CoverageEntry[] Entries);
internal sealed record CoverageEntry(string ProblemId,string Collection,string Language,int TestCount,string CodePath,string NotesPath,string Filename);
internal sealed record Boundary(string ProblemId,JsonElement[] Arguments,JsonElement Expected,string Reason);
internal sealed record CallableSource(CallableCodeDefinition[] Entries);
