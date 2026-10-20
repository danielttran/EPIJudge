using System.Diagnostics;
using System.Reflection;
using System.Text.Json;
using EpiJudge.Runner;
using EpiJudge.TestFramework;

var root = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
var catalog = new ProblemCatalog();
var epiProblems = catalog.Problems.Where(p => p.Collection == "epi").ToArray();
var failures = new List<string>();
var equal = typeof(SubmissionRunner).GetMethod("Equal", BindingFlags.NonPublic | BindingFlags.Static)!;
bool Equal(JsonElement left, JsonElement right, string mode = "ordered") => (bool)equal.Invoke(null, [left, right, mode])!;
void Require(bool condition, string message) { if (!condition) throw new Exception(message); }
void Check(string label, Action action)
{
    try { action(); Console.WriteLine("PASS " + label); }
    catch (Exception ex) { var error = label + ": " + ex.GetBaseException().Message; failures.Add(error); Console.WriteLine("FAIL " + error); }
}
var protocols = JsonDocument.Parse(File.ReadAllText(Path.Combine(root,"scripts/problem_catalog.json")))
    .RootElement.GetProperty("problems").EnumerateArray().ToDictionary(x => x.GetProperty("id").GetString()!);
Check("Catalog completeness", () => {
    Require(catalog.Problems.Count == 293 && Blind75Catalog.Problems.Count == 75, "Expected 218 EPI plus 75 Blind entries.");
    Require(epiProblems.Length == 218 && epiProblems.Select(p => p.Id).Distinct().Count() == 218, "Expected 218 unique IDs.");
    Require(protocols.Keys.Order().SequenceEqual(epiProblems.Select(p => p.Id).Order()), "Catalog IDs differ from canonical IDs.");
    Require(epiProblems.All(p => p.Examples.Length > 0 && p.TestCount > 0 && !string.IsNullOrWhiteSpace(p.Description)), "Incomplete problem metadata.");
});
long rows = 0, arguments = 0;
foreach (var problem in epiProblems)
{
    Check("Corpus " + problem.Id, () => {
        var protocol = protocols[problem.Id];
        var types = protocol.GetProperty("argumentTypes").EnumerateArray().Select(x => Resolve(x.GetString()!)).ToArray();
        var resultType = protocol.GetProperty("resultType").GetString()!;
        var tests = ProblemCatalog.LoadTests(root, problem.Id, false);
        Require(tests.Count == problem.TestCount, $"Metadata count {problem.TestCount} differs from {tests.Count} rows.");
        foreach (var test in tests)
        {
            Require(test.Arguments.Length == types.Length, "Argument count mismatch.");
            for (int i = 0; i < types.Length; i++) { test.Arguments[i].Deserialize(types[i], JudgeJson.Options); arguments++; }
            if (resultType != "void")
            {
                var type = Resolve(resultType);
                var result = test.Expected.Deserialize(type, JudgeJson.Options);
                var roundtrip = JsonSerializer.SerializeToElement(result, type, JudgeJson.Options);
                Require(Equal(test.Expected, roundtrip), "Expected output does not survive its declared C# type.");
            }
            rows++;
        }
    });
}
Console.WriteLine($"Corpus totals: {rows} rows, {arguments} typed arguments.");

Check("Ordered and unordered comparisons", () => {
    JsonElement J(string json) => JsonSerializer.Deserialize<JsonElement>(json);
    Require(!Equal(J("[[1,2]]"),J("[[2,1]]"),"unordered"), "Permutation order was ignored.");
    Require(Equal(J("[[1,2],[3]]"),J("[[3],[2,1]]"),"nested"), "Nested sets should match.");
    Require(!Equal(J("[1,1]"),J("[1,2]"),"unordered"), "Multiplicities were ignored.");
    Require(Equal(J("1.25"),J("1.2500000001")), "Float tolerance failed.");
    Require(!Equal(J("9007199254740992"),J("9007199254740993")), "Large integer precision lost.");
});

var custom = epiProblems.Where(p => p.Invocation.StartsWith("JudgeAdapters.Invoke")).ToArray();
foreach (var problem in custom)
{
    Check("Adapter " + problem.Id, () => {
        object solution = problem.Id switch {
            "adding_credits" => new CreditsFixture(), "lru_cache" => new LruFixture(),
            "circular_queue" or "queue_from_stacks" or "queue_with_max" => new QueueFixture(),
            "stack_with_max" => new StackFixture(), _ => new AlgorithmFixture()
        };
        var tests = ProblemCatalog.LoadTests(root, problem.Id, false);
        foreach (var test in tests)
        {
            object? output;
            try { output = JudgeAdapters.Invoke(problem.Id, test.Arguments, solution); }
            catch (Exception ex) { throw new Exception($"Input {string.Join(",",test.Arguments.Select(x=>x.GetRawText()[..Math.Min(200,x.GetRawText().Length)]))}: {ex.Message}",ex); }
            var actual = JsonSerializer.SerializeToElement(output, JudgeJson.Options);
            Require(Equal(test.Expected, actual), $"Correct fixture was rejected for {string.Join(",",test.Arguments.Select(x=> x.GetRawText()[..Math.Min(120,x.GetRawText().Length)]))}.");
        }
    });
}
foreach (var (id,input) in new[] {
    ("pivot_list", "[[1,2,3],2]"), ("copy_posting_list", "[[[1,-1],[2,1]]]"),
    ("graph_clone", "[2,[[0,1],[1,0]]]"), ("sudoku_solve", "[[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]"),
    ("alternating_array", "[[1,2,3,4]]"), ("search_maze", "[[[0,1],[1,0]],[0,0],[1,1]]"),
    ("random_permutation", "[3]"), ("random_subset", "[5,2]"),
    ("offline_sampling", "[2,[1,2,3,4]]"), ("online_sampling", "[[1,2,3,4],2]"),
    ("uniform_random_number", "[0,10]"), ("nonuniform_random_number", "[[1,2],[0.5,0.5]]")
})
{
    Check("Reject broken " + id, () => {
        var args = JsonSerializer.Deserialize<JsonElement[]>(input)!;
        try { JudgeAdapters.Invoke(id,args,new BrokenFixture()); }
        catch (JudgeValidationException) { return; }
        throw new Exception("Broken solution passed validation.");
    });
}
Check("Reject posting copy after corrupting original values", () => {
    var args=JsonSerializer.Deserialize<JsonElement[]>("[[[1,-1],[2,1]]]")!;
    try { JudgeAdapters.Invoke("copy_posting_list",args,new MutatingPostingFixture()); }
    catch(JudgeValidationException) { return; }
    throw new Exception("Mutated input was used as the expected result.");
});

Check("Compile every real starter and generated harness", () => {
    var directory = Path.Combine(root,".epi-runs","audit-compile"); Directory.CreateDirectory(directory);
    var harness = typeof(SubmissionRunner).GetMethod("CreateHarness",BindingFlags.NonPublic|BindingFlags.Static)!;
    var project = (string)typeof(SubmissionRunner).GetMethod("CreateProject",BindingFlags.NonPublic|BindingFlags.Static)!.Invoke(null,null)!;
    project = project.Replace("<OutputType>Exe</OutputType>","<OutputType>Library</OutputType>")
        .Replace("<StartupObject>JudgeEntryPoint</StartupObject>","");
    File.WriteAllText(Path.Combine(directory,"Submission.csproj"),project);
    File.WriteAllText(Path.Combine(directory,"NuGet.Config"),"<configuration><packageSources><clear /></packageSources></configuration>");
    File.WriteAllText(Path.Combine(directory,"Solution.cs"),string.Join("\n",epiProblems.Select(p => $"namespace Audit_{p.Id} {{\n{p.StarterCode}\n}}")));
    File.WriteAllText(Path.Combine(directory,"Harness.cs"),string.Join("\n",epiProblems.Select(p => $"namespace Audit_{p.Id} {{\n{harness.Invoke(null,[p])}\n}}")));
    using var process = Process.Start(new ProcessStartInfo("dotnet", "build Submission.csproj --configuration Release --verbosity quiet --disable-build-servers --maxcpucount:1") {
        WorkingDirectory = directory, UseShellExecute=false, RedirectStandardOutput=true, RedirectStandardError=true, CreateNoWindow=true
    })!;
    var stdout=process.StandardOutput.ReadToEndAsync(); var stderr=process.StandardError.ReadToEndAsync();
    if (!process.WaitForExit(90_000)) { process.Kill(true); throw new Exception("Compilation timed out."); }
    Require(process.ExitCode==0,stdout.GetAwaiter().GetResult()+stderr.GetAwaiter().GetResult());
});

Check("Real runner rejects invalid output when expected is false", () => {
    var fixtureRoot = Path.Combine(root,".epi-runs","audit-fixture-root");
    Directory.CreateDirectory(Path.Combine(fixtureRoot,"test_data"));
    File.WriteAllText(Path.Combine(fixtureRoot,"test_data","search_maze.tsv"),
        "array(array(int))\ttuple(int,int)\ttuple(int,int)\tbool\n[[0,1],[1,0]]\t[0,0]\t[1,1]\tfalse\n");
    var runner=new SubmissionRunner(fixtureRoot);var maze=catalog.Find("search_maze")!;
    const string invalid="public class Solution { public List<(int,int)> SearchMaze(List<List<int>> maze,(int,int) start,(int,int) end) => [start,end]; }";
    const string valid="public class Solution { public List<(int,int)> SearchMaze(List<List<int>> maze,(int,int) start,(int,int) end) => []; }";
    var rejected=runner.RunAsync(maze,invalid,true,CancellationToken.None).GetAwaiter().GetResult();
    Require(rejected?.Status=="Wrong answer" && rejected.Passed==0, "Invalid path was accepted: "+JsonSerializer.Serialize(rejected));
    var accepted=runner.RunAsync(maze,valid,true,CancellationToken.None).GetAwaiter().GetResult();
    Require(accepted?.Status=="Accepted" && accepted.Passed==1, "Valid no-path result was rejected: "+JsonSerializer.Serialize(accepted));
});

Console.WriteLine($"Audit complete: {failures.Count} failures.");
if (failures.Count > 0) { foreach(var failure in failures) Console.Error.WriteLine(failure); return 1; }
return 0;

static Type Resolve(string grammar)
{
    var primitives = new Dictionary<string,Type> { ["int"]=typeof(int), ["long"]=typeof(long), ["float"]=typeof(double), ["bool"]=typeof(bool), ["string"]=typeof(string) };
    if (primitives.TryGetValue(grammar,out var primitive)) return primitive;
    int open=grammar.IndexOf('('); string name=grammar[..open], inner=grammar[(open+1)..^1];
    var parts=new List<string>(); int depth=0,start=0;
    for(int i=0;i<inner.Length;i++) { if(inner[i]=='(') depth++; if(inner[i]==')') depth--; if(inner[i]==',' && depth==0) { parts.Add(inner[start..i].Trim()); start=i+1; } }
    parts.Add(inner[start..].Trim());
    var args=parts.Select(Resolve).ToArray();
    Type generic=name switch { "array"=>typeof(List<>), "set"=>typeof(HashSet<>), "binary_tree"=>typeof(BinaryTreeNode<>), "linked_list"=>typeof(ListNode<>), "tuple"=> args.Length switch { 2=>typeof(ValueTuple<,>),3=>typeof(ValueTuple<,,>),4=>typeof(ValueTuple<,,,>),_=>throw new Exception(grammar) }, _=>throw new Exception(grammar) };
    return generic.MakeGenericType(args);
}
