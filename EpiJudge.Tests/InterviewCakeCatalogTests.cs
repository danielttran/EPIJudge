using System.Reflection;
using System.Text.Json;
using System.Text.Json.Nodes;
using EpiJudge.Runner;
namespace EpiJudge.Tests;

public sealed class InterviewCakeCatalogTests
{
    private static string Root=>ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
    private static bool Matches(string slug,string arguments,string expected,string actual,string? fixture=null)
    {
        var def=InterviewCakeCatalog.Find("interviewcake_"+slug)!;
        var method=typeof(SubmissionRunner).Assembly.GetType("EpiJudge.Runner.InterviewCakeSubmissionRunner")!.GetMethod("Matches",BindingFlags.NonPublic|BindingFlags.Static)!;
        var args=JsonSerializer.Deserialize<JsonElement[]>(arguments)!;
        var test=new TestCase(args,JsonSerializer.SerializeToElement(JsonNode.Parse(expected)));
        return (bool)method.Invoke(null,[test,JsonSerializer.SerializeToElement(JsonNode.Parse(actual)),def,fixture is null?args:new[]{JsonSerializer.SerializeToElement(fixture)}])!;
    }

    [Fact]
    public void FrozenInventoryContainsOnlyTheFortyOneVerifiedCodingTasks()
    {
        var all=new ProblemCatalog();Assert.Equal(218,all.Problems.Count(p=>p.Collection=="epi"));Assert.Equal(75,all.Problems.Count(p=>p.Collection=="blind75"));
        Assert.Equal(41,InterviewCakeCatalog.Problems.Count);Assert.Equal(334,all.Problems.Count);
        Assert.Equal(Enumerable.Range(1,41),InterviewCakeCatalog.Problems.Select(p=>p.Position));
        foreach(var omitted in new[]{"js-scope","js-whats-wrong","ticket-sales-site","url-shortener","two-egg-problem"})Assert.Null(InterviewCakeCatalog.Find("interviewcake_"+omitted));
        Assert.NotEqual(all.Find("blind75_best_time_to_buy_and_sell_stock")!.Id,all.Find("interviewcake_stock-price")!.Id);
        Assert.Contains("global",all.Find("interviewcake_balanced-binary-tree")!.Description,StringComparison.OrdinalIgnoreCase);
        Assert.Contains("negative",all.Find("interviewcake_stock-price")!.Description,StringComparison.OrdinalIgnoreCase);
        Assert.All(InterviewCakeCatalog.Definitions,d=>Assert.StartsWith("https://www.interviewcake.com/question/csharp/",d.SourceUrl,StringComparison.Ordinal));
    }
    [Fact]
    public void EveryQuestionHasFiveTypedSelfContainedStartersAndThreeVerifiedExamples()
    {
        var native=new NativeProblemCatalog(Root);
        foreach(var d in InterviewCakeCatalog.Definitions)
        {
            Assert.Equal(SolutionCatalog.Languages.Order(),d.Starters.Keys.Order());Assert.NotEmpty(d.Description);Assert.NotEmpty(d.BankConventions);Assert.NotEmpty(d.Constraints);
            var tests=InterviewCakeCatalog.LoadTests(Root,d.Id,false);Assert.Equal(d.TestCount,tests.Count);Assert.True(tests.Count>=7);Assert.Equal(3,d.Examples.Length);
            for(int i=0;i<3;i++)Assert.True(JsonNode.DeepEquals(JsonNode.Parse(d.Examples[i].Output),JsonNode.Parse(tests[i].Expected.GetRawText())));
            foreach(var language in SolutionCatalog.Languages)
            {
                var starter=d.Starters[language];Assert.NotEmpty(starter.Signature);Assert.NotEmpty(starter.StarterCode);Assert.InRange(starter.StarterCode.Length,100,40000);
                if(language is "cpp" or "java")Assert.Equal(starter,native.GetStarter(language,d.Id));
            }
        }
    }
    [Fact]
    public void SanitizedProvenanceContainsAllSevenTransfersWithoutPrivatePaths()
    {
        var source=File.ReadAllText(Path.Combine(Root,"interviewcake/provenance/contracts.json"));using var doc=JsonDocument.Parse(source);
        Assert.Equal("aa6eb202de3cb17f7c034e2c86723005646908be774843da181acfd53b62d787",doc.RootElement.GetProperty("archiveSha256").GetString());
        Assert.Equal(Enumerable.Range(1,7),doc.RootElement.GetProperty("transferBatchesComplete").EnumerateArray().Select(v=>v.GetInt32()));
        Assert.Equal(41,doc.RootElement.GetProperty("questions").EnumerateArray().Select(v=>v.GetProperty("id").GetString()).Distinct().Count());
        Assert.DoesNotContain("/workspace/",source,StringComparison.Ordinal);Assert.DoesNotContain("source_archive_entry",source,StringComparison.Ordinal);
    }
    [Theory]
    [InlineData("2",true)][InlineData("3",true)][InlineData("1",false)][InlineData("null",false)][InlineData("\"2\"",false)][InlineData("[]",false)]
    public void DuplicatePropertyAcceptsEveryRepeatedValueAndRejectsMalformedTypes(string actual,bool expected)
    {
        Assert.Equal(expected,Matches("find-duplicate-optimize-for-space","[[1,2,3,2,3]]","2",actual));
    }
    [Theory]
    [InlineData("[\"a\",\"b\",\"d\"]",true)][InlineData("[\"a\",\"c\",\"d\"]",true)]
    [InlineData("[\"a\",\"b\",\"a\",\"c\",\"d\"]",false)][InlineData("null",false)][InlineData("[1,2]",false)]
    public void PathPropertyAcceptsTiedShortestRoutesAndRejectsInvalidShapes(string actual,bool expected)
    {
        Assert.Equal(expected,Matches("mesh-message","[{\"a\":[\"b\",\"c\"],\"b\":[\"a\",\"d\"],\"c\":[\"a\",\"d\"],\"d\":[\"b\",\"c\"]},\"a\",\"d\"]","[\"a\",\"b\",\"d\"]",actual));
    }
    [Theory]
    [InlineData("[null,null,3,5.5]",true)][InlineData("[null,null,8,5.5]",true)][InlineData("[null,null,5,5.5]",false)]
    [InlineData("[null,null,\"3\",5.5]",false)][InlineData("[null,null,null,5.5]",false)][InlineData("[null,null,3,5]",false)]
    public void TemperaturePropertyAcceptsAnyTiedModeAndFloatingMean(string actual,bool expected)
    {
        Assert.Equal(expected,Matches("temperature-tracker","[[\"Insert\",\"Insert\",\"GetMode\",\"GetMean\"],[[3],[8],[],[]]]","[null,null,3,5.5]",actual));
    }
    [Fact]
    public void SampledFilesystemCollisionsRemainCandidatesAndPathsAreValidated()
    {
        string a=new('x',512);string b=a[..90]+"Y"+a[91..];
        var entries=new[]{new{path="a",content=a,modified=10},new{path="nested/b",content=b,modified=20}};
        var arguments=JsonSerializer.Serialize(new object[]{entries});var fixture=Path.Combine(Path.GetTempPath(),"ic-property");
        string actual=JsonSerializer.Serialize(new[]{new[]{Path.Combine(fixture,"a"),Path.Combine(fixture,"nested","b")}});
        Assert.True(Matches("find-duplicate-files",arguments,"[]",actual,fixture));
        Assert.False(Matches("find-duplicate-files",arguments,"[]","[[\"a\",\"nested/b\"]]",fixture));
        Assert.False(Matches("find-duplicate-files",arguments,"[]","[[null,null]]",fixture));
        Assert.False(Matches("find-duplicate-files",arguments,"[]","{\"unexpected\":1}",fixture));
    }
}
