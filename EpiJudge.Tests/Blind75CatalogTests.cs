using System.Text.Json.Nodes;
using System.Text.Json;
using System.Reflection;
using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class Blind75CatalogTests
{
    [Fact]
    public void CollectionContainsExactlyTheFrozenCrackrOrderWithoutEpiAliases()
    {
        var catalog = new ProblemCatalog();
        var root = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
        var titles = File.ReadAllLines(Path.Combine(root, "blind75", "source-order.txt"));
        Assert.Equal(titles, Blind75Catalog.Definitions.Select(d => d.Title));
        Assert.Equal(75, titles.Length);
        Assert.Equal(218, catalog.Problems.Count(p => p.Collection == "epi"));
        Assert.Equal(334, catalog.Problems.Select(p => p.Id).Distinct().Count());
        Assert.Equal(Enumerable.Range(1, 75), Blind75Catalog.Problems.Select(p => p.Position));
        Assert.Contains("Combination Sum", titles);
        Assert.Contains("Combination Sum IV", titles);
        Assert.DoesNotContain("Longest Common Subsequence", titles);
        Assert.Contains("same array element twice", catalog.Find("two_sum")!.Description);
        Assert.Contains("different positions", catalog.Find("blind75_two_sum")!.Description);
        Assert.Contains("only groups", catalog.Find("anagrams")!.Description);
        Assert.Contains("singleton", catalog.Find("blind75_group_anagrams")!.Description);
    }

    [Theory]
    [InlineData("zabc", true)]
    [InlineData("azbc", true)]
    [InlineData("abzc", true)]
    [InlineData("zbac", false)]
    [InlineData("zab", false)]
    [InlineData("zabcx", false)]
    [InlineData("zzab", false)]
    [InlineData("", false)]
    public void AlienOrderAcceptsEveryValidOrderAndRejectsConstraintViolations(string order, bool expected)
    {
        var type = typeof(SubmissionRunner).Assembly.GetType("EpiJudge.Runner.Blind75SubmissionRunner")!;
        var method = type.GetMethod("AlienOrder", BindingFlags.NonPublic | BindingFlags.Static)!;
        var input = JsonSerializer.SerializeToElement(new[] { "za", "zb", "ca", "cb" });
        var test = new TestCase([input], JsonSerializer.SerializeToElement("zabc"));
        var actual = (bool)method.Invoke(null, [test, JsonSerializer.SerializeToElement(order)])!;
        Assert.Equal(expected, actual);
    }

    [Fact]
    public void EveryLanguageHasItsOwnTypedStarterAndEveryExampleHasACorpusCase()
    {
        var root = ProblemCatalog.FindRepositoryRoot(AppContext.BaseDirectory);
        var languages = new[] { "csharp", "javascript", "python", "cpp", "java" };
        var native = new NativeProblemCatalog(root);
        foreach (var definition in Blind75Catalog.Definitions)
        {
            Assert.Equal(languages.Order(), definition.Starters.Keys.Order());
            var tests = Blind75Catalog.LoadTests(root, definition.Id, false);
            Assert.Equal(definition.TestCount, tests.Count);
            Assert.True(tests.Count >= 15);
            Assert.NotEmpty(definition.Description);
            Assert.NotEmpty(definition.Constraints);
            foreach (var language in languages)
            {
                var starter = definition.Starters[language];
                Assert.Contains("Write your solution", starter.StarterCode);
                Assert.NotEmpty(starter.Signature);
                Assert.NotEmpty(starter.Filename);
                if (language is "cpp" or "java") Assert.Equal(starter, native.GetStarter(language, definition.Id));
            }
            for (var i = 0; i < definition.Examples.Length; i++)
                Assert.True(JsonNode.DeepEquals(JsonNode.Parse(definition.Examples[i].Output), JsonNode.Parse(tests[i].Expected.GetRawText())));
            var visible = Blind75Catalog.LoadTests(root, definition.Id, true);
            Assert.Equal(3, visible.Count);
        }
    }
}
